from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import User
from app.schemas.matching import MatchBreakdown, MatchItem, MatchRequest, MatchResponse
from app.services.matching import MatchCandidate, rank_candidates

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
    db: AsyncSession = Depends(get_db), # noqa: B008
) -> MatchResponse:
    response = await db.execute(select(User))
    users = response.scalars().all()

    target = next((u for u in users if u.id == payload.user_id), None)
    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    target_candidate = _to_candidate(target)
    candidates_pool = [_to_candidate(usr) for usr in users if usr.id != payload.user_id]

    ranked = rank_candidates(target_candidate, candidates_pool, payload.top_k)

    return MatchResponse(
        target_user_id=payload.user_id,
        results=[
            MatchItem(
                user_id=r.another_user_id,
                score=r.score,
                common_pieces=sorted(r.common_pieces),
                breakdown=MatchBreakdown(**r.breakdown),
            )
            for r in ranked
        ],
    )
