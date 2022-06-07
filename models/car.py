from dataclasses import dataclass
from sqlalchemy.sql import func

from ..extensions import db


@dataclass
class Car(db.Model):
    id: int
    model_name: str
    color: str
    created_at: str
    dealer_id: int

    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'))

    def __repr__(self):
        return f'<Car {self.model_name}>'
