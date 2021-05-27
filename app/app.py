from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

# from datetime import datetime
# from datetime import timedelta
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


def get_all_urls():
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

    return jsonify(urls_list)


@app.route('/')
def hello():
    name = 'Evgen'
    return render_template('index.html', name=name)


@app.route('/my.test_api/<short_url>', methods=['GET'])
def get_url(short_url):
    if short_url != 'get-all-urls':
        url = 'https://my.test_api/' + short_url
        base_url = Urls.query.filter(Urls.short_url == url).first()

        if base_url:
            serialized = {
                'id': base_url.id,
                'url': base_url.url,
                'short_url': base_url.short_url,
                'created_at': base_url.created_at,
                'expiry_at': base_url.expiry_at
            }

            if base_url.expiry_at > datetime.now():
                return render_template("url_detail.html", serialized=serialized), 302
            else:
                return f'<h1>Token expired</h1>\n{render_template("url_detail.html", serialized=serialized)}', 498

        return '<h1> 404 Page not found </h1>', 404

    if short_url == 'get-all-urls':
        all_urls = get_all_urls()
        return render_template('urls.html', all_urls=all_urls.json), 200  #


@app.route('/add_url', methods=['GET', 'POST'])
def insert_url():
    if request.method == 'POST':
        new_one = request.form.to_dict().get('url')

        base_url = Urls.query.filter(Urls.url == new_one).all()[-1]

        if base_url and base_url.expiry_at > datetime.now():
            short_url = base_url.short_url
            http_code = 200
        else:
            short_url = create_short_url(new_one)
            new_entry = Urls(url=new_one, short_url=short_url)
            session.add(new_entry)
            session.commit()
            base_url = Urls.query.filter(Urls.url == new_one).all()[-1]
            http_code = 201

        serialized = {
            'id': base_url.id,
            'url': base_url.url,
            'short_url': short_url,
            'created_at': base_url.created_at,
            'expiry_at': base_url.expiry_at
        }

        return render_template('add_url.html', short_url=short_url), http_code

    return render_template('add_url.html')


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
        'short_url': item.short_url,
        'created_at': item.created_at,
        'expiry_at': item.expiry_at
    }

    return jsonify(serialized)


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
