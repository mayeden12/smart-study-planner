from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..schemas.task_schema import StudyTopicCreate, StudyTopicUpdate, StudyTopicResponse
from ..core.ai_services import generate_study_hack
from ..models.task_db import StudyTopicDB
from ..database import get_db

router = APIRouter(prefix="/topics", tags=["Study Topics"])


@router.post("/", response_model=StudyTopicResponse)
def create_topic(topic: StudyTopicCreate, db: Session = Depends(get_db)):
    db_topic = StudyTopicDB(**topic.model_dump())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


@router.get("/", response_model=List[StudyTopicResponse])
def list_topics(db: Session = Depends(get_db)):
    return db.query(StudyTopicDB).order_by(StudyTopicDB.created_at.desc()).all()


@router.patch("/{topic_id}", response_model=StudyTopicResponse)
def update_topic(topic_id: int, topic: StudyTopicUpdate, db: Session = Depends(get_db)):
    db_topic = db.query(StudyTopicDB).filter(StudyTopicDB.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    update_data = topic.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_topic, key, value)
    db.commit()
    db.refresh(db_topic)
    return db_topic


@router.patch("/{topic_id}/generate-hack", response_model=StudyTopicResponse)
def generate_hack(topic_id: int, db: Session = Depends(get_db)):
    db_topic = db.query(StudyTopicDB).filter(StudyTopicDB.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db_topic.study_hack = generate_study_hack(db_topic.title)
    db.commit()
    db.refresh(db_topic)
    return db_topic


@router.delete("/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    db_topic = db.query(StudyTopicDB).filter(StudyTopicDB.id == topic_id).first()
    if db_topic:
        db.delete(db_topic)
        db.commit()
    return {"message": "Deleted successfully"}
