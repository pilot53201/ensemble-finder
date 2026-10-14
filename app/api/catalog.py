from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Instrument, Piece
from app.schemas.catalog import InstrumentRead, PieceRead

instruments_router = APIRouter()
pieces_router = APIRouter()


@instruments_router.get("/", response_model=list[InstrumentRead])
async def list_instruments(
    session: AsyncSession = Depends(get_db),  # noqa: B008,
) -> list[Instrument]:
    response = await session.execute(select(Instrument).order_by(Instrument.name))
    return list(response.scalars().all())


@pieces_router.get("/", response_model=list[PieceRead])
async def list_pieces(
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> list[Piece]:
    response = await session.execute(select(Piece).order_by(Piece.composer, Piece.title))
    return list(response.scalars().all())
