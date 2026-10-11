from sqlalchemy import SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, BigIntPK


class Piece(BigIntPK, Base):
    __tablename__ = "pieces"

    title: Mapped[str] = mapped_column(Text, nullable=False)
    composer: Mapped[str | None] = mapped_column(Text)
    difficulty: Mapped[int | None] = mapped_column(SmallInteger)
