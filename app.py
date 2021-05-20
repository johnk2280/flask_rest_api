from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

client = app.test_client()

db = SQLAlchemy(app)


def create_short_url(url):
    pass


def check_url():
    pass


@app.route('/test_task_api/v1.0', methods=['GET'])
def get_url():
    return 'Hello, Evgen'


@app.route('/test_task_api/v1.0', methods=['POST'])
def insert_url():
    pass


@app.route('/test_task_api/v1.0/<int:id>', methods=['PUT'])
def update_url():
    pass


@app.route('/test_task_api/v1.0/<int:id>', methods=['DELETE'])
def delete_url():
    pass
