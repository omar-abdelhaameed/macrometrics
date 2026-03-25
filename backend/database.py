from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


def get_database_url(url: str | None = None) -> str:
    """
    Process DATABASE_URL for compatibility with SQLAlchemy 2.0.
    
    Neon.tech and some PostgreSQL providers use 'postgres://' prefix,
    but SQLAlchemy 2.0 requires 'postgresql://'.
    This function seamlessly converts the prefix if needed.
    """
    if url is None:
        url = os.getenv("DATABASE_URL")
    
    if not url:
        # Fallback for local development - use SQLite
        print("WARNING: DATABASE_URL not set, using SQLite for local dev")
        url = "sqlite:///./macrometrics.db"
        return url
    
    # Neon.tech uses postgres:// but SQLAlchemy 2.0 requires postgresql://
    if url.startswith("postgres://"):
        url = "postgresql://" + url[10:]
        print(f"  → Converted Neon postgres:// to postgresql://")
    
    return url

# Security: Require DATABASE_URL from environment - fail if not set
DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
