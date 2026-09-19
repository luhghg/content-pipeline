from pydantic import BaseModel, ConfigDict
from app.models.db_models import ContentType
from datetime import datetime
from typing import Optional



class TopicBase(BaseModel):
    title: str
    content_type: ContentType


class TopicCreate(TopicBase):
    prompt_hint: Optional[str]


class TopicResponse(TopicBase):
    id: int
    is_active: bool = True
    last_used_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
