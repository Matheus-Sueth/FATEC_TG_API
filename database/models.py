from sqlalchemy import Column, ForeignKey, Integer, String, TIME
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True)

    messages = relationship("Message", back_populates="owner")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    hora = Column(TIME)
    owner_name = Column(String, ForeignKey("users.nome"))

    owner = relationship("User", back_populates="messages")