import uuid

from fastapi.testclient import TestClient

from app.constants.common import ROLE_USER, ROLE_AI
from app.enums.document_status import DocumentStatus
from app.main import app
from app.models.conversation import Conversation
from app.models.document import Document
from app.models.message import Message
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

    def test_show_conversation(self):
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
        self.session.flush()
        self.session.refresh(doc)

        conv = Conversation()
        conv.document_id = doc.id
        self.session.add(conv)
        self.session.flush()
        self.session.refresh(conv)

        message1 = Message()
        message1.conversation_id = conv.id
        message1.content = 'Who created Python?'
        message1.role = ROLE_USER
        self.session.add(message1)

        message2 = Message()
        message2.conversation_id = conv.id
        message2.content = 'Guido van Rossum'
        message2.role = ROLE_AI
        self.session.add(message2)
        self.session.commit()

        response = client.get(
            f'/conversations/{conv.id}',
            headers={'Authorization': f'Bearer {user.id}'},
        )
        conversation_resp = response.json()

        assert response.status_code == 200
        assert conversation_resp['document_id'] == doc.id
        assert len(conversation_resp['messages']) == 2
