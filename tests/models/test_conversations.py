import uuid

from app.enums.document_status import DocumentStatus
from app.models.conversation import Conversation
from app.models.document import Document
from app.models.message import Message
from app.models.user import User
from tests.models import BaseTest


class TestConversations(BaseTest):
    def test_document(self):
        new_user = User()
        new_user.uuid = uuid.uuid4()
        self.session.add(new_user)
        self.session.commit()

        new_document = Document()
        new_document.user_id = new_user.id
        new_document.title = 'my document'
        new_document.status = DocumentStatus.PENDING.value
        self.session.add(new_document)
        self.session.commit()

        new_conversation = Conversation(document_id=new_document.id)
        self.session.add(new_conversation)
        self.session.commit()

        document = self.session.query(Document).first()

        assert document is not None
        assert document.id == new_document.id
        assert document.user.uuid == new_user.uuid
        assert len(document.conversations) == 1
        assert document.conversations[0].id == new_conversation.id

    def test_messages(self):
        new_user = User()
        new_user.uuid = uuid.uuid4()
        self.session.add(new_user)
        self.session.commit()

        new_document = Document()
        new_document.user_id = new_user.id
        new_document.title = 'my document'
        new_document.status = DocumentStatus.PENDING.value
        self.session.add(new_document)
        self.session.commit()

        new_conversation = Conversation(document_id=new_document.id)
        self.session.add(new_conversation)
        self.session.commit()

        new_message_1 = Message(conversation_id=new_conversation.id)
        new_message_1.content = 'my assistant content'
        new_message_1.role = 'assistant'
        self.session.add(new_message_1)

        new_message_2 = Message(conversation_id=new_conversation.id)
        new_message_2.content = 'my user content'
        new_message_2.role = 'user'
        self.session.add(new_message_2)

        self.session.commit()

        conversation = self.session.query(Conversation).first()

        assert conversation is not None
        assert conversation.id == new_document.id
        assert conversation.document.user.uuid == new_user.uuid
        assert len(conversation.messages) == 2
        assert conversation.messages[0].role == new_message_2.role
        assert conversation.messages[1].role == new_message_1.role
