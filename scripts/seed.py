"""Seed the database with demo data: instruments, pieces, users.

Usage:
    uv run python -m scripts.seed
"""

import asyncio

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory
from app.models.associations import user_instruments, user_repertoire
from app.models.instrument import Instrument
from app.models.piece import Piece
from app.models.user import User

INSTRUMENTS = [
    "Piano",
    "Violin",
    "Viola",
    "Cello",
    "Flute",
    "Clarinet",
    "Guitar",
    "Trumpet",
    "Saxophone",
    "Harp",
]

PIECES = [
    ("Moonlight Sonata", "Beethoven", 3),
    ("Für Elise", "Beethoven", 2),
    ("Nocturne Op. 9 No. 2", "Chopin", 3),
    ("Prelude in C Major", "Bach", 1),
    ("Toccata and Fugue in D Minor", "Bach", 4),
    ("The Four Seasons: Spring", "Vivaldi", 3),
    ("Symphony No. 5", "Beethoven", 4),
    ("Clair de Lune", "Debussy", 3),
    ("Gymnopédie No. 1", "Satie", 2),
    ("Liebestraum No. 3", "Liszt", 4),
    ("Hungarian Dance No. 5", "Brahms", 3),
    ("Canon in D", "Pachelbel", 2),
    ("Ave Maria", "Schubert", 2),
    ("Bolero", "Ravel", 4),
    ("Rhapsody in Blue", "Gershwin", 4),
    ("Carmen: Habanera", "Bizet", 3),
    ("Swan Lake Theme", "Tchaikovsky", 3),
    ("The Nutcracker: Waltz of the Flowers", "Tchaikovsky", 3),
    ("Adagio for Strings", "Barber", 3),
    ("Pavane pour une infante défunte", "Ravel", 3),
]


USERS = [
    {
        "name": "Alice",
        "city": "Moscow",
        "level": 3,
        "instruments": ["Piano"],
        "pieces": ["Moonlight Sonata", "Nocturne Op. 9 No. 2", "Clair de Lune"],
    },
    {
        "name": "Bob",
        "city": "Moscow",
        "level": 3,
        "instruments": ["Piano", "Violin"],
        "pieces": ["Moonlight Sonata", "Für Elise", "Clair de Lune"],
    },
    {
        "name": "Carol",
        "city": "SPb",
        "level": 2,
        "instruments": ["Violin"],
        "pieces": ["The Four Seasons: Spring", "Canon in D", "Ave Maria"],
    },
    {
        "name": "Dave",
        "city": "Moscow",
        "level": 4,
        "instruments": ["Cello"],
        "pieces": ["Symphony No. 5", "Adagio for Strings", "Bolero"],
    },
    {
        "name": "Eve",
        "city": "Kazan",
        "level": 1,
        "instruments": ["Flute"],
        "pieces": ["Für Elise", "Gymnopédie No. 1"],
    },
]


async def seed(session: AsyncSession) -> None:
    await session.execute(delete(user_repertoire))
    await session.execute(delete(user_instruments))
    await session.execute(delete(User))
    await session.execute(delete(Piece))
    await session.execute(delete(Instrument))
    await session.commit()

    instruments = [Instrument(name=n) for n in INSTRUMENTS]
    pieces = [Piece(title=t, composer=c, difficulty=d) for t, c, d in PIECES]
    session.add_all(instruments + pieces)
    await session.flush()

    inst_by_name = {i.name: i for i in instruments}
    piece_by_title = {p.title: p for p in pieces}

    for spec in USERS:
        user = User(name=spec["name"], city=spec["city"], level=spec["level"])
        user.instruments = [inst_by_name[n] for n in spec["instruments"]]
        user.pieces = [piece_by_title[t] for t in spec["pieces"]]
        session.add(user)

    await session.commit()


async def main() -> None:
    async with async_session_factory() as session:
        await seed(session)
    print("Seed done: 10 instruments, 20 pieces, 5 users.")


if __name__ == "__main__":
    asyncio.run(main())
