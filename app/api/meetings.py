from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..schemas.meeting_schema import SummarizeRequest, MeetingResponse
from ..core.ai_services import summarize_meeting_text
from ..models.meeting_db import MeetingDB
from ..database import get_db

router = APIRouter(prefix="/meetings", tags=["Meetings"])

@router.post("/summarize", response_model=MeetingResponse)
def create_summary(request: SummarizeRequest, db: Session = Depends(get_db)):
    # Create Summary using AI
    summary_text = summarize_meeting_text(request.text)
    
    # Save to Database (Create)
    db_meeting = MeetingDB(original_text=request.text, summary_text=summary_text)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

@router.get("/", response_model=List[MeetingResponse])
def list_meetings(db: Session = Depends(get_db)):
    # List all summaries (Read)
    return db.query(MeetingDB).order_by(MeetingDB.created_at.desc()).all()

@router.patch("/{meeting_id}/favorite", response_model=MeetingResponse)
def toggle_favorite(meeting_id: int, db: Session = Depends(get_db)):
    # Update a summary
    meeting = db.query(MeetingDB).filter(MeetingDB.id == meeting_id).first()
    meeting.is_favorite = not meeting.is_favorite
    db.commit()
    db.refresh(meeting)
    return meeting

@router.delete("/{meeting_id}")
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    # Delete a summary
    db.query(MeetingDB).filter(MeetingDB.id == meeting_id).delete()
    db.commit()
    return {"message": "Meeting deleted"}