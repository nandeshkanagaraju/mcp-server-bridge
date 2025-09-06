# core/database/connection_manager.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config.settings import settings

DATABASE_URL = (
    f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Create the SQLAlchemy engine for asynchronous operation.
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a configured "Session" class. Instances of this class will be actual database sessions.
# This object is the main entry point to the database for all queries.
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)