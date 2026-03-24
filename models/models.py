from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from db.database import Base

class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"

class PlanEnum(str, enum.Enum):
    basic = "basic"
    gold = "gold"
    platinum = "platinum"

class User(Base):
    __tablename__ = "users"

    # Use Firebase UID as the primary key
    id = Column(String(128), primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), default="")
    avatar_url = Column(String(500), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile = relationship("Profile", back_populates="user", uselist=False)
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(128), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String(255), default="")
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    location = Column(String(255), nullable=True)
    profession = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    looking_for = Column(String(20), nullable=True)
    plan = Column(String(20), default="basic")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="profile")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = Column(String(128), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(String(128), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

