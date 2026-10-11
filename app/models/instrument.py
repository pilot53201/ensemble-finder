from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, BigIntPK


class Instrument(BigIntPK, Base):
    __tablename__ = "instruments"

    name: Mapped[str] = mapped_column(Text, unique=True)
