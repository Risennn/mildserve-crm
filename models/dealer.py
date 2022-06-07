from dataclasses import dataclass
from sqlalchemy.sql import func

from ..extensions import db


@dataclass
class Dealer(db.Model):
    id: int
    name: str
    email: str
    created_at: str
    desc: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    desc = db.Column(db.Text)
    cars = db.relationship('Car', backref='dealer')

    def __repr__(self):
        return f'<Dealer {self.name}>'
