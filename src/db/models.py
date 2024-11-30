from sqlalchemy import Column, Integer, String, Float, Date
from db.connection import Base

class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True)
    cargo_type = Column(String)
    rate = Column(Float)
    date = Column(Date)
