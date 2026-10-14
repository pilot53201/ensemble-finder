from typing import TYPE_CHECKING

from sqlalchemy import SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BigIntPK, CreatedAtMixin
from app.models.instrument import Instrument
from app.models.piece import Piece

if TYPE_CHECKING:
    from app.models.invitation import Invitation


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

    sent_invitations: Mapped[list[Invitation]] = relationship(
        foreign_keys="Invitation.from_user_id",
        back_populates="from_user",
        cascade="all, delete-orphan",
    )

    received_invitations: Mapped[list[Invitation]] = relationship(
        foreign_keys="Invitation.to_user_id",
        back_populates="to_user",
        cascade="all, delete-orphan",
    )
