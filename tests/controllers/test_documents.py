import os
import uuid
from unittest import mock

from fastapi.testclient import TestClient

from app.jobs import embeddings
from app.main import app
from app.models.user import User
from tests.models import BaseTest

client = TestClient(app)


class TestDocuments(BaseTest):
    @mock.patch('app.queuer.q.enqueue')
    def test_store_document(self, mock_enqueue):
        user = User()
        user.uuid = uuid.uuid4()
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        test_file_path = os.path.join(os.path.dirname(__file__), 'testdata', 'sample.pdf')

        with open(test_file_path, 'rb') as file:
            response = client.post(
                '/documents/uploads/',
                files={'doc': ('sample.pdf', file, 'multipart/form-data')},
                headers={'Authorization': f'Bearer {user.id}'},
            )

        assert response.status_code == 200
        assert response.json() == {'message': 'successfully uploaded'}
        mock_enqueue.assert_called_once_with(embeddings.create, mock.ANY, mock.ANY)
