from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.database import Base



class User(Base):
    __tablename__ = "users"  # 指定表名为"users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 用户ID，主键，自增
    username = Column(String(50), unique=True, nullable=False, index=True)  # 用户名，唯一，非空，建立索引
    password_hash = Column(String(255), nullable=False)  # 密码哈希值，非空
    created_at = Column(DateTime, default=datetime.utcnow)  # 创建时间，默认为当前UTC时间



    # 关系定义
    characters = relationship("UserCharacter", back_populates="user", cascade="all, delete-orphan")  # 用户角色关系级联删除
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")  # 用户对话关系级联删除
    milestones = relationship("Milestone", back_populates="user", cascade="all, delete-orphan")  # 用户里程碑关系级联删除


# 用户角色模型
class UserCharacter(Base):
    __tablename__ = "user_characters"  # 指定表名为"user_characters"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 角色ID，主键，自增
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 关联用户ID，外键，非空
    gender = Column(String(10), nullable=False)  # female / male
    personality = Column(String(20), nullable=False)  # 文静/治愈/傲娇/阳光/风趣/暖男
    custom_name = Column(String(50), nullable=True)
    relationship_stage = Column(Integer, default=0)  # 0-5
    intimacy_score = Column(Float, default=0.0)  # 0.0-1.0
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="characters", uselist=False)
    conversations = relationship("Conversation", back_populates="character", cascade="all, delete-orphan")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("user_characters.id"), nullable=True)
    summary = Column(Text, nullable=True)
    message_count = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="conversations")
    character = relationship("UserCharacter", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(10), nullable=False)  # user / ai
    content = Column(Text, nullable=False)
    emotion_tag = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    intimacy_change = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="milestones")
