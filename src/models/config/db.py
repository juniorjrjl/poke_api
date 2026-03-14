import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

load_dotenv()

database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url, echo=True)

Base = declarative_base()
