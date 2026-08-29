from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.config import DATABASE_URL, SQLITE_FALLBACK_URL

def init_engine():
    connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    try:
        eng = create_engine(DATABASE_URL, connect_args=connect_args)
        with eng.connect() as conn:
            pass
        print(f"[DATABASE] Connected successfully to PostgreSQL: {DATABASE_URL}")
        return eng
    except Exception as e:
        print(f"[DATABASE NOTICE] PostgreSQL connection ({DATABASE_URL}) not available yet.")
        print(f"[DATABASE NOTICE] Active fallback session: {SQLITE_FALLBACK_URL}")
        return create_engine(SQLITE_FALLBACK_URL, connect_args={"check_same_thread": False})

engine = init_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """FastAPI Dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
