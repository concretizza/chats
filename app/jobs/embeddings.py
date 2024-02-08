import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings

from app.constants.common import COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP
from app.logger import logger


def create(doc_id: int, doc_path: str):
    try:
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
    except Exception as e:
        logger.error('create embeddings: %s', e, exc_info=True)
        raise
