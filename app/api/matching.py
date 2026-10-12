from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.matching import MatchResponse, MatchRequest
from app.services.matching import MatchCandidate

router = APIRouter()

def _to_candidate(user: User) -> MatchCandidate:
    return MatchCandidate(
        user_id=user.id,
        level=user.level,
        city=user.city,
        piece_ids={p.id for p in user.pieces},
        instrument_ids={i.id for i in user.instruments},
    )


@router.post("/", response_model=MatchResponse)
async def find_matches(
        payload: MatchRequest,
        db: AsyncSession = Depends
)
