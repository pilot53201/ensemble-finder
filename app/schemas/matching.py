from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    user_id: int
    top_k: int = Field(default=10, ge=1, le=100)


class MatchBreakdown(BaseModel):
    repertoire: float
    level: float
    city: float
    instruments: float
    total: float


class MatchItem(BaseModel):
    user_id: int
    score: float
    common_pieces: list[int]
    breakdown: MatchBreakdown


class MatchResponse(BaseModel):
    target_user_id: int
    results: list[MatchItem]
