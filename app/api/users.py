from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import User
from app.schemas.user import UserCreate, UserRead

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
