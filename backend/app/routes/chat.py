# 导入 json 模块，用于处理 JSON 数据的序列化和反序列化
import json
# 导入 asyncio 模块，用于异步编程，支持超时等待和并发任务
import asyncio
# 导入 datetime，用于获取当前时间戳，标记会话结束时间
from datetime import datetime

# 导入 FastAPI 路由和 WebSocket 工具：APIRouter 创建路由，WebSocket 处理 WebSocket 连接，WebSocketDisconnect 捕获断开事件
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# 导入 SQLAlchemy 的会话类型（在本文件中未直接使用，保留为可能的依赖注入）
from sqlalchemy.orm import Session

# 导入数据库会话工厂（用于手动创建数据库会话，因为 WebSocket 生命周期长于普通请求）
from app.database import get_db
# 导入 LangGraph 聊天图，是消息处理的核心引擎
from app.graph.graph import chat_graph
# 导入关系状态类型定义，用于构建初始状态字典
from app.graph.state import RelationshipState
# 导入对话摘要生成器和滑动窗口记忆类
from app.memory.summarizer import generate_summary, SlidingWindowMemory
# 导入 ORM 模型：UserCharacter 用户角色，Conversation 会话，Message 消息
from app.models import UserCharacter, Conversation, Message
# 导入 JWT 工具：decode_access_token 解析令牌获取用户 ID，require_user_id 依赖注入获取用户 ID
from app.middleware.jwt import decode_access_token, require_user_id
# 导入 DeepSeek 聊天补全流式接口（本文件中未直接使用，但路由模块需要可用）
from app.services.deepseek import chat_completion_stream

# 创建路由实例（没有 prefix，因为 WebSocket 路由不能像 HTTP 路由那样自动加前缀，所以路径直接在装饰器中写完整路径）
router = APIRouter()

# 每个用户的滑动窗口缓存字典，键为用户 ID，值为滑动窗口记忆对象
# 滑动窗口用于在对话历史过长时，截取最近的部分消息并生成摘要，避免超出 LLM 上下文限制
_sliding_windows: dict[int, SlidingWindowMemory] = {}


def get_sliding_window(user_id: int) -> SlidingWindowMemory:
    """获取指定用户的滑动窗口记忆对象，如果不存在则创建一个新的"""
    if user_id not in _sliding_windows:
        _sliding_windows[user_id] = SlidingWindowMemory()  # 创建新的滑动窗口对象
    return _sliding_windows[user_id]  # 返回用户的滑动窗口


@router.websocket("/api/chat")
async def chat_websocket(websocket: WebSocket):
    """WebSocket 聊天端点，处理实时双向通信
    整个方法相当于一个长连接的生命周期，从接受到关闭"""
    # 接受 WebSocket 连接，必须调用此方法后客户端才能开始通信
    await websocket.accept()

    # ===== 第一步：通过第一条消息进行身份认证 =====
    try:
        # 接收客户端发送的第一条 JSON 消息，期望包含 JWT 令牌
        data = await websocket.receive_json()
        token = data.get("token", "")  # 从消息中提取 token，默认为空字符串
        user_id = decode_access_token(token)  # 解码 JWT 令牌，获取用户 ID，失败返回 None
        if user_id is None:  # 如果令牌无效或已过期
            await websocket.send_json({"error": "未授权"})  # 发送错误消息给客户端
            await websocket.close()  # 关闭 WebSocket 连接
            return  # 结束连接处理
    except Exception:  # 捕获所有异常（如 JSON 解析失败、连接异常断开等）
        await websocket.send_json({"error": "认证失败"})  # 发送通用认证失败消息
        await websocket.close()  # 关闭连接
        return  # 结束处理

    # ===== 第二步：创建数据库会话 =====
    # 注意：这里没有使用 Depends(get_db)，因为 WebSocket 生命周期比普通 HTTP 请求长
    # 使用 SessionLocal 手动创建和管理数据库会话的生命周期
    from app.database import SessionLocal
    db = SessionLocal()

    try:
        # ===== 第三步：获取用户的活跃角色 =====
        char = db.query(UserCharacter).filter(
            UserCharacter.user_id == user_id,     # 匹配当前用户
            UserCharacter.is_active == True        # 只取当前活跃的角色
        ).first()                                  # 取第一个（用户同时只能有一个活跃角色）
        if char is None:                           # 如果用户还没有选择角色
            await websocket.send_json({"error": "请先选择角色"})  # 通知前端引导用户选角色
            await websocket.close()                # 关闭连接
            return                                 # 结束处理

        # ===== 第四步：创建新的会话记录 =====
        conv = Conversation(user_id=user_id, character_id=char.id)  # 创建会话对象，关联用户和角色
        db.add(conv)                                                 # 添加到数据库会话
        db.commit()                                                  # 写入数据库
        db.refresh(conv)                                             # 刷新获取最新数据（如自增 id）

        # ===== 第五步：初始化滑动窗口和历史消息 =====
        sliding = get_sliding_window(user_id)  # 获取或创建用户的滑动窗口对象

        # 查询该用户和该角色的历史消息（跨会话），用于提供上下文给 LLM
        recent_msgs = db.query(Message).join(Conversation).filter(  # 联合查询 Message + Conversation
            Conversation.user_id == user_id,       # 只查当前用户的
            Conversation.character_id == char.id   # 只查当前角色的
        ).order_by(Message.created_at.desc()).limit(20).all()  # 按时间倒序，最多 20 条

        # 反转历史消息（从最早的到最新的），组装成 LLM 需要的消息格式
        messages_history = []
        for m in reversed(recent_msgs):  # reversed 将倒序的查询结果反转回正序
            messages_history.append({"role": m.role, "content": m.content})  # 构建消息字典列表

        # 发送连接成功消息给客户端，携带新创建的会话 ID
        await websocket.send_json({"type": "connected", "conversation_id": conv.id})

        # ===== 第六步：启动接收任务 =====
        # 使用 asyncio.create_task 创建一个后台任务来异步等待客户端消息
        # 这样可以在等待消息的同时，支持超时（用于 AI 主动发起对话）
        receive_task = asyncio.create_task(websocket.receive_json())

        # ===== 第七步：主循环 —— 处理用户消息和 AI 主动对话 =====
        while True:
            # 等待用户输入 OR 超时（用于主动对话）
            # 300 秒（5分钟）无用户消息会触发 AI 主动说话
            done, pending = await asyncio.wait(
                [receive_task],        # 等待的 task 列表
                timeout=300.0,         # 超时时间（秒），即 5 分钟无响应触发主动对话
                return_when=asyncio.FIRST_COMPLETED  # 任一任务完成或超时即返回
            )

            is_proactive = False  # 标记本次是否是 AI 主动发起的对话
            if receive_task in done:
                # === 分支 A：收到了用户的消息 ===
                try:
                    data = receive_task.result()  # 获取消息结果
                    user_input = data.get("message", "").strip()  # 提取消息内容并去除首尾空白
                    # 创建新的接收任务，准备接收下一条用户消息
                    receive_task = asyncio.create_task(websocket.receive_json())

                    if not user_input:  # 如果消息内容为空（只有空白字符）
                        await websocket.send_json({"type": "error", "message": "说点什么吧～"})
                        continue  # 跳过本轮处理，继续等待用户输入
                except Exception:
                    # 捕获异常（如 JSON 格式错误、连接关闭），跳出主循环
                    break
            else:
                # === 分支 B：超时 —— 用户沉默了 300 秒 ===
                # 只有上一条消息是 AI 发送的才触发主动对话（避免 AI 一直自说自话）
                if not messages_history or messages_history[-1].get("role") == "user":
                    continue  # 如果上一条是用户消息或没有历史，不触发主动对话，重新等待

                print(f"[DEBUG] Proactive trigger for user {user_id}")  # 打印调试日志
                is_proactive = True  # 标记为主动对话
                user_input = "[SYSTEM_PROACTIVE_TRIGGER]"  # 使用特殊标记作为"用户输入"，LangGraph 会识别并返回主动消息

            # ===== 第八步：保存用户消息（非主动对话时才保存） =====
            if not is_proactive:
                # 创建用户消息记录并写入数据库
                db_msg = Message(
                    conversation_id=conv.id,  # 关联当前会话
                    user_id=user_id,           # 当前用户
                    role="user",               # 角色为"user"（用户）
                    content=user_input,        # 消息内容
                )
                db.add(db_msg)  # 添加到数据库会话
                db.commit()    # 写入数据库

                # 更新滑动窗口（如果历史消息过长，自动摘要压缩）
                messages_history = sliding.append(messages_history, "user", user_input)

            # ===== 第九步：调用 LangGraph 引擎生成 AI 回复 =====
            try:
                # 构建初始状态：包含所有上下文信息，传递给 LangGraph 处理
                initial_state: RelationshipState = {
                    "user_id": user_id,                                         # 用户 ID
                    "character_id": char.gender + "_" + char.personality,       # 角色 ID，格式如"female_文静"
                    "personality": char.personality,                            # 角色性格
                    "messages": messages_history,                               # 对话历史
                    "current_input": user_input,                                # 当前用户输入（或主动触发标记）
                    "relationship_stage": char.relationship_stage,              # 当前关系阶段
                    "intimacy_score": char.intimacy_score,                      # 当前亲密度
                    "stage_name": "",                                           # 阶段名称（由 LangGraph 填充）
                    "stage_description": "",                                    # 阶段描述（由 LangGraph 填充）
                    "custom_name": char.custom_name,                            # 用户给角色取的自定义名字
                    "retrieved_memories": "",                                   # 检索到的记忆（由 LangGraph 填充）
                    "user_knowledge": "",                                       # 用户知识（由 LangGraph 填充）
                    "character_knowledge": "",                                  # 角色知识（由 LangGraph 填充）
                    "user_emotion": "",                                         # 用户情绪（由 LangGraph 填充）
                    "system_prompt": "",                                        # 系统提示词（由 LangGraph 填充）
                    "response": "",                                             # 最终回复（由 LangGraph 填充）
                }

                # 异步调用 LangGraph 图，传入初始状态，得到最终状态
                final_state = await chat_graph.ainvoke(initial_state)

                # 将 LangGraph 计算出的新关系状态更新到数据库
                char.relationship_stage = final_state.get("relationship_stage", char.relationship_stage)
                char.intimacy_score = final_state.get("intimacy_score", char.intimacy_score)
                db.commit()  # 提交更新

                response_text = final_state.get("response", "")  # 提取 AI 回复文本

                # 发送 AI 回复给客户端，附带当前关系状态信息，供前端展示
                await websocket.send_json({
                    "type": "message",
                    "role": "ai",
                    "content": response_text,                             # 回复内容
                    "relationship": {
                        "stage": char.relationship_stage,                   # 更新后的关系阶段
                        "intimacy_score": round(char.intimacy_score, 4),   # 更新后的亲密度（保留 4 位小数）
                    },
                })

            except Exception as e:
                # LangGraph 调用失败时的降级处理：使用预设的回复，保证用户体验不中断
                response_text = f"嗯…我在呢。刚才有点走神，你再说一遍好不好？"
                print(f"LangGraph error: {e}")  # 打印错误日志便于排查
                await websocket.send_json({
                    "type": "message",
                    "role": "ai",
                    "content": response_text,  # 发送降级回复
                })

            # ===== 第十步：保存 AI 回复消息 =====
            ai_msg = Message(
                conversation_id=conv.id,  # 关联当前会话
                user_id=user_id,           # 当前用户
                role="ai",                 # 角色为"ai"（AI）
                content=response_text,     # AI 回复内容
            )
            db.add(ai_msg)  # 添加到数据库会话
            db.commit()    # 写入数据库

            # 更新滑动窗口，将 AI 回复加入历史
            messages_history = sliding.append(messages_history, "assistant", response_text)

    # ===== 异常处理 =====
    except WebSocketDisconnect:
        # WebSocket 正常断开，不做额外处理，直接进入 finally 块
        pass
    except Exception as e:
        # 其他未预料的异常，打印日志但不影响 finally 块的清理工作
        print(f"WebSocket error: {e}")
    finally:
        # ===== 最终清理：生成摘要并关闭会话 =====
        try:
            # 调用 LLM 为这次对话生成摘要
            conv_summary = await generate_summary(messages_history)
            conv.summary = conv_summary                      # 保存摘要到会话记录
            conv.ended_at = datetime.utcnow()                # 记录会话结束时间
            conv.message_count = len(messages_history) // 2  # 计算消息条数（用户+AI 算一对）
            db.commit()                                      # 提交所有更新
        except Exception:
            # 摘要生成失败不阻塞关闭流程，静默忽略
            pass
        db.close()  # 关闭数据库会话，释放连接
