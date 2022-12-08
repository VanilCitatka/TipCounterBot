from typing import Dict, Any
from datetime import date

from sqlalchemy.orm import Session
from .models import TipDay


def create_tip_day(db: Session, data: Dict[str, Any]):
    km, nm, cash = data['km_tips'], data['nm_tips'], data['cash_tips']
    tip_sum = str(sum(map(int, (km, nm, cash))))
    tip_day = TipDay(
        date=date.today(),
        kate_media=km,
        net_monet=nm,
        cash=cash,
        tip_sum=tip_sum
    )
    db.merge(tip_day)
    db.commit()
    return tip_day


def get_decade_statistic(db: Session):
    return db.query(TipDay).limit(10)
