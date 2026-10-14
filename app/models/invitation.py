from enum import IntEnum
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BigIntPK, CreatedAtMixin

if TYPE_CHECKING:
    from app.models import User


class InvitationStatus(IntEnum):
    """
    Enumerate for invitation statuses.
    """

    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2


class Invitation(BigIntPK, CreatedAtMixin, Base):
    __tablename__ = "invitations"

    __table_args__ = (CheckConstraint("status IN (0, 1, 2)", name="ck_invitation_status"),)

    from_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    to_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    status: Mapped[InvitationStatus] = mapped_column(SmallInteger, default=InvitationStatus.PENDING)
    message: Mapped[str | None] = mapped_column(Text)

    from_user: Mapped[User] = relationship(
        foreign_keys=[from_user_id],
        back_populates="sent_invitations",
    )

    to_user: Mapped[User] = relationship(
        foreign_keys=[to_user_id],
        back_populates="received_invitations",
    )
