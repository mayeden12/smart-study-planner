from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, timezone
from app.database import Base

class MeetingDB(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String, nullable=False)
    summary_text = Column(String, nullable=False)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))