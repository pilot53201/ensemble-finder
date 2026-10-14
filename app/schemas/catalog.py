from pydantic import BaseModel, ConfigDict


class PieceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    composer: str | None
    difficulty: int | None


class InstrumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
