from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BigIntPK:
    """
    Mixin: Primary key BIGINT.
    """

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class CreatedAtMixin:
    """Mixin: created_at with server-side timestamp."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
