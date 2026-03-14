from sqlalchemy import Column, Integer, String, DateTime, Date, Enum as SQLEnum, Boolean
from datetime import datetime, timezone
from app.schemas.task_schema import TopicStatus
from app.database import Base


class StudyTopicDB(Base):
    __tablename__ = "study_topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(SQLEnum(TopicStatus), default=TopicStatus.TODO)
    due_date = Column(Date)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    category = Column(String, default="General")
    study_hack = Column(String, nullable=True)
