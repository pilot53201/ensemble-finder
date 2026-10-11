from sqlalchemy import SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, BigIntPK, CreatedAtMixin


class User(BigIntPK, CreatedAtMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    city: Mapped[str | None] = mapped_column(Text)
    level: Mapped[int] = mapped_column(SmallInteger, default=1)
    bio: Mapped[str | None] = mapped_column(Text)
