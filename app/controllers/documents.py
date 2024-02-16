import os
import uuid

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session, selectinload

from app import database
from app.dtos.common import NotFoundResponse
from app.enums.document_status import DocumentStatus
from app.jobs import embeddings
from app.logger import logger
from app.middlewares.auth import get_current_user
from app.models.document import Document
from app.models.user import User
from app.queuer import q

router = APIRouter(
    prefix='/documents',
    tags=['Document'],
    responses=NotFoundResponse,
)


@router.get('/')
async def index(
        db: Session = Depends(database.connection),
        current_user: User = Depends(get_current_user),
):
    documents = db.query(Document).options(
        selectinload(Document.conversations),
    ).filter(
        Document.user_id == int(current_user.id),
    ).all()

    return documents


@router.post('/uploads')
async def store(
        doc: UploadFile = File(...),
        db: Session = Depends(database.connection),
        current_user: User = Depends(get_current_user),
):
    current_file_path = os.path.abspath(__file__)
    current_dir_path = os.path.dirname(current_file_path)
    root_dir_path = os.path.abspath(os.path.join(current_dir_path, '..', '..'))
    uploads_path = os.path.join(root_dir_path, 'uploads', 'documents')

    file_name = uuid.uuid4()
    file_path = os.path.join(uploads_path, f'{file_name}.pdf')

    try:
        document = Document()
        document.user_id = current_user.id
        document.title = doc.filename
        document.status = DocumentStatus.PENDING.value

        db.add(document)
        db.flush()
        db.refresh(document)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error('store the document: %s', e, exc_info=True)
        return {'message': 'there was an error saving the document metadata'}

    try:
        with open(file_path, 'wb') as f:
            while contents := doc.file.read(1024 * 1024):
                f.write(contents)
    except Exception as e:
        logger.error('upload the document: %s', e, exc_info=True)
        return {'message': 'there was an error uploading the file'}
    finally:
        doc.file.close()

    q.enqueue(embeddings.create, document.id, file_path)

    return {'message': 'successfully uploaded'}
