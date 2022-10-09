from sqlalchemy import Integer, String, Column, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from db.db_setup import Base
from datetime import datetime


class Thread(Base):
    __tablename__ = "thread"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column(Text)
    pic = Column(String)
    messages = relationship("Message", back_populates="thread")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column(Text)
    pic = Column(String)
    thread_id = Column(Integer, ForeignKey("thread.id"))
    thread = relationship("Thread", back_populates="messages")
    reply_id = Column(Integer)
    replies = Column(MutableList.as_mutable(ARRAY(Integer)))
