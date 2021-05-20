from app import client
from models import Urls
import pytest


def test_get_url():
    a = client.get('/test_task_api/v1.0')

    assert a.status_code == 200
