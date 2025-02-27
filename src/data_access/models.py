from datetime import datetime
import asyncio
from sqlalchemy import JSON, Integer, DateTime, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base

from src.data_access.db_connector import engine


Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'

    query_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    city = mapped_column(String)
    date_time = mapped_column(DateTime, default=datetime.utcnow)
    json_data = mapped_column(JSON)
