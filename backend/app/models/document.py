from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=True)

    original_filename = Column(String(255), nullable=False)

    saved_filename = Column(String(255), nullable=False)

    extracted_text = Column(Text)

    ai_analysis = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())