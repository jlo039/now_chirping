from sqlmodel import Session, create_engine, SQLModel
from app.config import settings
from app.models.user import User  # Ensure models are registered

engine = create_engine(
    settings.DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
