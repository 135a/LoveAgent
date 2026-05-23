import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.graph.graph import chat_graph
from app.graph.state import RelationshipState
from app.memory.summarizer import generate_summary, SlidingWindowMemory
from app.models import UserCharacter, Conversation, Message
from app.middleware.jwt import decode_access_token, require_user_id
from app.services.deepseek import chat_completion_stream

router = APIRouter()

# Per-user sliding window
_sliding_windows: dict[int, SlidingWindowMemory] = {}


def get_sliding_window(user_id: int) -> SlidingWindowMemory:
    if user_id not in _sliding_windows:
        _sliding_windows[user_id] = SlidingWindowMemory()
    return _sliding_windows[user_id]


@router.websocket("/api/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()

    # Authenticate via first message
    try:
        data = await websocket.receive_json()
        token = data.get("token", "")
        user_id = decode_access_token(token)
        if user_id is None:
            await websocket.send_json({"error": "未授权"})
            await websocket.close()
            return
    except Exception:
        await websocket.send_json({"error": "认证失败"})
        await websocket.close()
        return

    # Get or create database session
    from app.database import SessionLocal
    db = SessionLocal()

    try:
        # Get user character
        char = db.query(UserCharacter).filter(UserCharacter.user_id == user_id).first()
        if char is None:
            await websocket.send_json({"error": "请先选择角色"})
            await websocket.close()
            return

        # Create conversation record
        conv = Conversation(user_id=user_id)
        db.add(conv)
        db.commit()
        db.refresh(conv)

        sliding = get_sliding_window(user_id)
        messages_history = []

        await websocket.send_json({"type": "connected", "conversation_id": conv.id})

        while True:
            data = await websocket.receive_json()
            user_input = data.get("message", "").strip()

            if not user_input:
                await websocket.send_json({"type": "error", "message": "说点什么吧～"})
                continue

            # Save user message
            db_msg = Message(
                conversation_id=conv.id,
                user_id=user_id,
                role="user",
                content=user_input,
            )
            db.add(db_msg)
            db.commit()

            # Update sliding window
            messages_history = sliding.append(messages_history, "user", user_input)

            # Run the LangGraph
            try:
                initial_state: RelationshipState = {
                    "user_id": user_id,
                    "character_id": char.gender + "_" + char.personality,
                    "personality": char.personality,
                    "messages": messages_history,
                    "current_input": user_input,
                    "relationship_stage": char.relationship_stage,
                    "intimacy_score": char.intimacy_score,
                    "stage_name": "",
                    "stage_description": "",
                    "custom_name": char.custom_name,
                    "retrieved_memories": "",
                    "user_knowledge": "",
                    "character_knowledge": "",
                    "user_emotion": "",
                    "system_prompt": "",
                    "response": "",
                }

                final_state = await chat_graph.ainvoke(initial_state)

                # Update relationship in database
                char.relationship_stage = final_state.get("relationship_stage", char.relationship_stage)
                char.intimacy_score = final_state.get("intimacy_score", char.intimacy_score)
                db.commit()

                response_text = final_state.get("response", "")

            except Exception as e:
                response_text = f"嗯…我在呢。刚才有点走神，你再说一遍好不好？"
                print(f"LangGraph error: {e}")

            # Save AI message
            ai_msg = Message(
                conversation_id=conv.id,
                user_id=user_id,
                role="ai",
                content=response_text,
            )
            db.add(ai_msg)
            db.commit()

            # Update sliding window
            messages_history = sliding.append(messages_history, "assistant", response_text)

            # Send response with relationship info
            await websocket.send_json({
                "type": "message",
                "role": "ai",
                "content": response_text,
                "relationship": {
                    "stage": char.relationship_stage,
                    "intimacy_score": round(char.intimacy_score, 4),
                },
            })

            # TODO: emit streaming via chat_completion_stream for typing effect
            # For now, full response is sent at once. The frontend can simulate typing.

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Generate summary and close conversation
        try:
            conv_summary = await generate_summary(messages_history)
            conv.summary = conv_summary
            conv.ended_at = datetime.utcnow()
            conv.message_count = len(messages_history) // 2
            db.commit()
        except Exception:
            pass
        db.close()
