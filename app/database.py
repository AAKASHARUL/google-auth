from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# --- CHANGE IS HERE ---
# Use the pymysql dialect for MySQL connection
engine = create_engine(
    settings.DATABASE_URL, 
    # Optional: MySQL often requires a limit on the pool size
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Helper to create tables
def init_db():
    # Make sure your MySQL database (e.g., 'your_db_name') is already created 
    # before running this.
    Base.metadata.create_all(bind=engine)