from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.catalog import InstrumentRead, PieceRead


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    city: str | None = None
    level: int = Field(default=1, ge=1, le=4)
    bio: str | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str | None
    level: int
    bio: str | None
    created_at: datetime

    pieces: list[PieceRead] = []
    instruments: list[InstrumentRead] = []


class RepertoireUpdate(BaseModel):
    piece_ids: list[int]
