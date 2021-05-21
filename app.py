from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime
from datetime import timedelta
import random
from hashids import Hashids

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
    egg = sum([ord(el) for el in url])
    salt = chr(random.randint(0, 1000))
    hashids = Hashids(salt=salt)
    hash_id = hashids.encode(egg)

    return f'https://my.test_api/{hash_id}'


@app.route('/my.test_api/<short_url>', methods=['GET'])
def get_url(short_url):
    if short_url:
        if short_url != 'get-all-urls':
            short_url = 'https://my.test_api/' + short_url
            base_short_url = Urls.query.filter(Urls.short_url == short_url).first()

            if base_short_url and base_short_url.expiry_at > datetime.now():
                return jsonify({'short_url': base_short_url.url}), 302

            return 'token expired\n', 498

        if short_url == 'get-all-urls':
            urls = Urls.query.all()
            urls_list = []

            for url in urls:
                urls_list.append({
                    'id': url.id,
                    'url': url.url,
                    'short_url': url.short_url,
                    'created_at': url.created_at,
                    'expiry_at': url.expiry_at
                })

            return jsonify(urls_list), 200

    return '', 404


@app.route('/test_task_api/v1.0', methods=['POST'])
def insert_url():
    new_one = Urls(**request.json)
    if new_one.url:
        base_url = Urls.query.filter(Urls.url == new_one.url).first()

        if base_url and base_url.expiry_at > datetime.now():
            return jsonify({'url': new_one.url, 'short_url': base_url.short_url})

        else:
            short_url = create_short_url(new_one.url)

        new_entry = Urls(url=new_one.url, short_url=short_url)
        session.add(new_entry)
        session.commit()

        return jsonify({'url': new_one.url, 'short_url': short_url}), 201

    return '', 400


@app.route('/test_task_api/v1.0/<int:url_id>', methods=['PUT'])
def update_url(url_id):
    item = Urls.query.filter(Urls.id == url_id).first()
    params = request.json
    if not item:
        return {'message': 'No url for this id'}, 400

    for key, value in params.items():
        setattr(item, key, value)

    session.commit()
    serialized = {
        'id': item.id,
        'url': item.url,
        'short_url': item.short_url
    }

    return serialized


@app.route('/test_task_api/v1.0/<int:url_id>', methods=['DELETE'])
def delete_url(url_id):
    item = Urls.query.filter(Urls.id == url_id).first()
    if not item:
        return {'message': 'No url for this id'}, 400

    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
