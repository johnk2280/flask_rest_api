from app import db
from datetime import datetime


class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True)
    short_url = db.Column(db.Text, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, url, short_url):
        super(Urls, self).__init__(self,)