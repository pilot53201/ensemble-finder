from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.invitation import InvitationStatus


class InvitationCreate(BaseModel):
    to_user_id: int
    message: str | None = Field(default=None, max_length=1000)


class InvitationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    from_user_id: int
    to_user_id: int
    status: InvitationStatus
    message: str | None
    created_at: datetime


class InvitationUpdate(BaseModel):
    status: InvitationStatus
