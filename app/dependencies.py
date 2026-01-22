import aiosqlite
from typing import AsyncGenerator
from app.config import settings
from app.utils.logger import logger

async def get_db_connection() -> AsyncGenerator[aiosqlite.Connection, None]:
    async with aiosqlite.connect(settings.DATABASE_URL.replace("sqlite+aiosqlite:///", "")) as db:
        db.row_factory = aiosqlite.Row
        yield db

async def init_db():
    logger.info("Initializing database...")
    db_path = settings.DATABASE_URL.replace("sqlite+aiosqlite:///", "")
    async with aiosqlite.connect(db_path) as db:
        with open("data/seed_data.sql", "r") as f:
            await db.executescript(f.read())
        await db.commit()
    logger.info("Database initialized.")
