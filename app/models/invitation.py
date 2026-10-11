from enum import IntEnum

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, BigIntPK, CreatedAtMixin


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
