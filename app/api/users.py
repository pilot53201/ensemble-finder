from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Piece, User
from app.schemas.user import RepertoireUpdate, UserCreate, UserRead

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> User:
    user = User(**payload.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} is not found",
        )
    return user


@router.put("/{user_id}/repertoire", response_model=UserRead)
async def update_repertoire(
    user_id: int,
    payload: RepertoireUpdate,
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} is not found",
        )
    if payload.piece_ids:
        response = await session.execute(select(Piece).where(Piece.id.in_(payload.piece_ids)))
        pieces = list(response.scalars().all())

        missing = set(payload.piece_ids) - {p.id for p in pieces}
        if missing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pieces not found: {sorted(missing)}",
            )
    else:
        pieces = []
    user.pieces = pieces
    await session.commit()
    return user
