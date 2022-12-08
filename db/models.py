from sqlalchemy import Column, Integer, Date

from .database import Base


class TipDay(Base):
    __tablename__ = 'tips'

    date = Column(Date, primary_key=True, index=True, unique=True)
    kate_media = Column(Integer)
    net_monet = Column(Integer)
    cash = Column(Integer)
    tip_sum = Column(Integer)
