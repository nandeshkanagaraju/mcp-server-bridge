from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config.settings import settings

DATABASE_URL = (
    f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Create the SQLAlchemy engine for asynchronous operation.
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Create a configured "Session" class for database interactions.
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)