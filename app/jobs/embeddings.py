import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings

from app.constants.common import COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP
from app.enums.document_status import DocumentStatus
from app.logger import logger
from app.models import SessionLocal

from app.models import Base
from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation
from app.models.message import Message


def create(doc_id: int, doc_path: str):
    db = SessionLocal()
    try:
        db.query(Document).filter(Document.id == doc_id).update({
            Document.status: DocumentStatus.PROCESSING.value,
        })

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        loader = PyPDFLoader(doc_path)
        docs = loader.load_and_split(text_splitter)

        for doc in docs:
            doc.metadata = {
                'doc_id': doc_id,
                'page': doc.metadata['page'],
                'text': doc.page_content,
            }

        embeddings = OpenAIEmbeddings()
        PGVector.from_documents(
            embedding=embeddings,
            documents=docs,
            collection_name=COLLECTION_NAME,
            connection_string=os.getenv('DB_URL'),
        )

        db.query(Document).filter(Document.id == doc_id).update({
            Document.status: DocumentStatus.COMPLETED.value,
        })
    except Exception as e:
        logger.error('create embeddings: %s', e, exc_info=True)
        db.query(Document).filter(Document.id == doc_id).update({
            Document.status: DocumentStatus.FAILED.value,
        })
        raise
    finally:
        db.commit()
        db.close()
