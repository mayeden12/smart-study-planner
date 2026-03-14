from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SummarizeRequest(BaseModel):
    """Schema for the input text to be summarized."""
    text: str = Field(..., min_length=2, description="The raw text from a meeting.")

class MeetingResponse(BaseModel):
    """Schema for returning a saved meeting summary."""
    id: int
    original_text: str
    summary_text: str
    is_favorite: bool
    created_at: datetime
    class Config:
        from_attributes = True