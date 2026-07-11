from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id"))

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())