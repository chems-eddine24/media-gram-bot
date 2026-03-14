from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from bot.config import settings


engine = create_async_engine(settings.DB_ASYNC_URL, echo=True)
sessionlocal = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
metadata = MetaData()
Base = declarative_base()



async def get_db():
    async with sessionlocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()