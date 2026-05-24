import os  # 操作系统接口，用于文件路径和目录操作
import hashlib  # 哈希库，用于生成内容的 MD5 指纹，避免重复导入
from pathlib import Path  # 面向对象的文件路径操作库

# 知识库文件根目录路径
# 在 Docker 容器中，当前文件位于 /app/app/knowledge/ingestion.py
# 向上三级到 /app，再加 knowledge 目录
KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "knowledge"


def load_text_files(directory: Path) -> list[tuple[str, str]]:
    """Load all .txt and .md files from a directory, return list of (filename, content)."""
    chunks = []  # 存储所有读取到的文本块，每个元素是 (文件名, 段落内容)
    if not directory.exists():  # 如果目录不存在，直接返回空列表
        return chunks
    for f in directory.iterdir():  # 遍历目录中的所有文件和子目录
        if f.suffix in (".txt", ".md") and f.is_file():  # 只处理 .txt 和 .md 文件
            content = f.read_text(encoding="utf-8").strip()  # 读取文件内容并去除首尾空白
            if content:  # 如果文件非空
                # Split into paragraphs as chunks
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]  # 按两个换行符分割成段落
                for para in paragraphs:  # 遍历每个段落
                    if len(para) > 10:  # 跳过太短的片段（少于10个字符的认为是无效内容）
                        chunks.append((f.name, para))  # 保存为 (文件名, 段落内容)
    return chunks  # 返回所有文本块列表


async def load_all_knowledge():
    """Load all knowledge files into vector store with personality-level isolation."""
    # 延迟导入，避免循环依赖
    from app.memory.vector_store import get_global_collection

    # 获取全局角色知识库集合（ChromaDB 集合）
    char_coll = get_global_collection("global_character")
    # 获取集合中已有文档的 ID，用于去重，避免重复导入相同内容
    existing_ids = set(char_coll.get()["ids"])

    # 文件夹名称到数据库中存储的性格名称的映射表
    p_map = {
        "healing": "治愈", "quiet": "文静", "tsundere": "傲娇",  # 女性角色性格
        "sunny": "阳光", "funny": "风趣", "warm": "暖男"  # 男性角色性格
    }

    base_char_dir = KNOWLEDGE_DIR / "character"  # 角色知识根目录
    for gender in ("female", "male"):  # 分别处理女性和男性角色
        gender_dir = base_char_dir / gender  # 性别子目录路径
        if not gender_dir.exists():  # 如果该性别目录不存在则跳过
            continue

        # Walk through personality subfolders
        for p_dir in gender_dir.iterdir():  # 遍历性格子目录（如 healing/, sunny/）
            if p_dir.is_dir():  # 只处理目录，跳过文件
                p_id_folder = p_dir.name  # 获取文件夹名称（如 "healing"）
                personality_name = p_map.get(p_id_folder, "unknown")  # 映射为中文性格名，未知则标记为 unknown

                chunks = load_text_files(p_dir)  # 读取该性格目录下的所有 .txt 和 .md 文件
                for i, (fname, content) in enumerate(chunks):  # 遍历所有文本块，i 为块序号
                    # Granular ID: gender + personality + filename + index + content hash
                    # 生成细粒度的唯一 ID，包含：性别、性格、文件名、序号、内容哈希
                    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]  # 取 MD5 前 8 位作为内容指纹
                    chunk_id = f"char_{gender}_{p_id_folder}_{fname}_{i}_{content_hash}"

                    if chunk_id not in existing_ids:  # 如果该块尚未导入过（去重）
                        char_coll.add(  # 添加到 ChromaDB 向量数据库
                            documents=[content],  # 文档原始文本内容
                            metadatas=[{  # 元数据，用于后续过滤检索
                                "source": fname,  # 来源文件名
                                "gender": gender,  # 角色性别
                                "personality": personality_name,  # 性格类型（中文）
                                "type": "character"  # 数据类型标记
                            }],
                            ids=[chunk_id],  # 唯一 ID
                        )
                        print(f"  ✓ Loaded {personality_name} knowledge: {fname} [{i}]")  # 打印导入成功日志

    print("✓ Knowledge base loaded successfully")  # 知识库全量导入完成
