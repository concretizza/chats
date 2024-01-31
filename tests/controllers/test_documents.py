import os
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_store_document():
    test_file_path = os.path.join(os.path.dirname(__file__), 'testdata', 'sample.pdf')

    with open(test_file_path, 'rb') as file:
        response = client.post(
            '/documents/uploads',
            files={'doc': ('sample.pdf', file, 'multipart/form-data')},
        )

    assert response.status_code == 200
    assert response.json() == {'message': 'successfully uploaded'}
