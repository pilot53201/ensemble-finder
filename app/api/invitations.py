from typing import Literal

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Invitation, InvitationStatus, User
from app.schemas.invitation import InvitationCreate, InvitationRead, InvitationUpdate

router = APIRouter()


@router.post("/", response_model=InvitationRead, status_code=status.HTTP_201_CREATED)
async def create_invitation(
    payload: InvitationCreate,
    session: AsyncSession = Depends(get_db),  # noqa: B008
    current_user_id: int = Header(alias="X-User-Id"),  # noqa: B008
) -> Invitation:
    if payload.to_user_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot invite yourself",
        )

    to_user = await session.get(User, payload.to_user_id)
    if to_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {payload.to_user_id} is not found",
        )

    actual_inv = await session.execute(
        select(Invitation).where(
            Invitation.from_user_id == current_user_id,
            Invitation.to_user_id == payload.to_user_id,
            Invitation.status == InvitationStatus.PENDING,
        )
    )

    if actual_inv.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pending invitation to this user already exists",
        )

    invitation = Invitation(
        from_user_id=current_user_id,
        to_user_id=payload.to_user_id,
        message=payload.message,
    )
    session.add(invitation)
    await session.commit()
    await session.refresh(invitation)
    return invitation


@router.get("/", response_model=list[InvitationRead])
async def list_invitations(
    session: AsyncSession = Depends(get_db),  # noqa: B008
    current_user_id: int = Header(alias="X-User-Id"),  # noqa: B008
    box: Literal["incoming", "outgoing"] = Query(default="incoming"),
) -> list[Invitation]:
    if box == "incoming":
        condition = Invitation.to_user_id == current_user_id
    else:
        condition = Invitation.from_user_id == current_user_id

    response = await session.execute(
        select(Invitation).where(condition).order_by(Invitation.created_at.desc())
    )
    return list(response.scalars().all())


@router.patch("/{invitation_id}", response_model=InvitationRead)
async def update_invitation_status(
    invitation_id: int,
    payload: InvitationUpdate,
    session: AsyncSession = Depends(get_db),  # noqa: B008
    current_user_id: int = Header(alias="X-User-ID"),  # noqa: B008
) -> Invitation:
    if payload.status == InvitationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot set status back to PENDING",
        )

    invitation = await session.get(Invitation, invitation_id)
    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation {invitation_id} is not found",
        )
    if invitation.to_user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recipient can update invitation status",
        )

    if invitation.status != InvitationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invitation is already resolved",
        )
    invitation.status = payload.status
    await session.commit()
    return invitation
