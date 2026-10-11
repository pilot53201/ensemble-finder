from sqlalchemy import BigInteger, Column, ForeignKey, Table

from app.db.base import Base

user_instruments = Table(
    "user_instruments",
    Base.metadata,
    Column(
        "user_id",
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "instrument_id",
        BigInteger,
        ForeignKey("instruments.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


user_repertoire = Table(
    "user_repertoire",
    Base.metadata,
    Column(
        "user_id",
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "piece_id",
        BigInteger,
        ForeignKey("pieces.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
