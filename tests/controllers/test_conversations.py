import uuid

from fastapi.testclient import TestClient

from app.enums.document_status import DocumentStatus
from app.main import app
from app.models.document import Document
from app.models.user import User
from tests.models import BaseTest

client = TestClient(app)


class TestConversations(BaseTest):
    def test_store_conversation(self):
        user = User()
        user.uuid = uuid.uuid4()
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)

        doc = Document()
        doc.user_id = user.id
        doc.title = 'my document'
        doc.status = DocumentStatus.PENDING.value
        self.session.add(doc)
        self.session.commit()
        self.session.refresh(doc)

        response = client.post(
            f'/conversations/?doc_id={doc.id}',
            headers={'Authorization': f'Bearer {user.id}'},
        )

        assert response.status_code == 200
        assert response.json()['document_id'] == doc.id
