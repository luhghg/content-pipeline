from pydantic import BaseModel, Field, ConfigDict
from app.models.db_models import (ContentType, Status,
                                  ApprovalType)
from typing import Optional
from datetime import datetime



class ContentItemResponse(BaseModel):
    id: int
    topic_id: int
    content_type: ContentType
    status: Status
    title: Optional[str] = Field(max_length=255)
    body: Optional[str]
    scheduled_for: Optional[datetime]
    approval_type: Optional[ApprovalType]
    approved_by_id: Optional[int]
    approved_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
