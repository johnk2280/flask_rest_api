from app import db
from app import session
from app import Base

from datetime import datetime
from datetime import timedelta


class Urls(Base):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=False)
    short_url = db.Column(db.Text, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    expiry_at = db.Column(db.DateTime, default=datetime.now() + timedelta(minutes=10))

