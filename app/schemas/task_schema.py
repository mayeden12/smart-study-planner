from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class TopicStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class StudyTopicBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TopicStatus = TopicStatus.TODO
    due_date: Optional[date] = None
    study_hack: Optional[str] = None


class StudyTopicCreate(StudyTopicBase):
    pass


class StudyTopicUpdate(BaseModel):
    status: Optional[TopicStatus] = None
    is_favorite: Optional[bool] = None


class StudyTopicResponse(StudyTopicBase):
    id: int
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True
