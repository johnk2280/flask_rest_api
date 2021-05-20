from flask import Flask
from flask import jsonify
from flask import request

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


def create_short_url(url):
    pass


def check_url():
    pass


@app.route('/test_task_api/v1.0', methods=['GET'])
def get_url():
    urls = Urls.query.all()
    urls_list = []
    for url in urls:
        urls_list.append({
            'id': url.id,
            'url': url.url,
            'short_url': url.short_url,
            'created_at': url.created_at,
            'updated_at': url.updated_at
        })

    return jsonify(urls_list)


@app.route('/test_task_api/v1.0', methods=['POST'])
def insert_url():
    new_one = Urls(**request.json)
    session.add(new_one)
    session.commit()
    url = {
        'url': new_one.url,
        'short_url': new_one.short_url
    }

    return jsonify(url)


@app.route('/test_task_api/v1.0/<int:id>', methods=['PUT'])
def update_url():
    pass


@app.route('/test_task_api/v1.0/<int:id>', methods=['DELETE'])
def delete_url():
    pass


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
