from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL connection URL
# DATABASE_URL = "postgresql://postgres:9899@localhost/delivery_db"#db instead of localhost

# SQLite connection URL
script_dir = os.path.dirname(__file__)
DATABASE_URL = f"sqlite:///{os.path.join(script_dir, 'delivery_db.db')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


