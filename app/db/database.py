from tortoise import Tortoise

from app.config.settings import settings


async def init_db() -> None:
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["app.db.models"]},
    )
    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()
