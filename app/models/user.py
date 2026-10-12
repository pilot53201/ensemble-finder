from sqlalchemy import SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BigIntPK, CreatedAtMixin
from app.models.instrument import Instrument
from app.models.piece import Piece


class User(BigIntPK, CreatedAtMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    city: Mapped[str | None] = mapped_column(Text)
    level: Mapped[int] = mapped_column(SmallInteger, default=1)
    bio: Mapped[str | None] = mapped_column(Text)

    instruments: Mapped[list[Instrument]] = relationship(
        secondary="user_instruments",
        lazy="selectin",
    )
    pieces: Mapped[list[Piece]] = relationship(
        secondary="user_repertoire",
        lazy="selectin",
    )
