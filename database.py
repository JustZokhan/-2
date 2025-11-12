# database.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# если есть переменная окружения DB_FILE (например, /data/employee_stats.db) — используем её
db_file = os.getenv("DB_FILE", "employee_stats.db")
DB_PATH = Path(db_file)
if not DB_PATH.is_absolute():
    DB_PATH = BASE_DIR / DB_PATH
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS teams (
                key TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        """))
        conn.execute(text("""
            INSERT OR IGNORE INTO teams (key, name) VALUES
            ('left','Левая команда'),
            ('right','Правая команда')
        """))
        info = conn.execute(text("PRAGMA table_info(employees)")).fetchall()
        cols = [r[1] for r in info]
        if "team_key" not in cols:
            conn.execute(text("ALTER TABLE employees ADD COLUMN team_key TEXT DEFAULT 'left'"))
            conn.execute(text("UPDATE employees SET team_key = COALESCE(team_key, 'left')"))
