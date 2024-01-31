import os
import uuid

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

import app.database
from app.dtos.common import NotFoundResponse
from app.models.document import Document
from app.models.user import User

router = APIRouter(
    prefix='/documents',
    tags=['Document'],
    responses=NotFoundResponse,
)


@router.post('/uploads')
async def store(doc: UploadFile = File(...), db: Session = Depends(app.database.connection)):
    current_file_path = os.path.abspath(__file__)
    current_dir_path = os.path.dirname(current_file_path)
    root_dir_path = os.path.abspath(os.path.join(current_dir_path, '..', '..'))
    uploads_path = os.path.join(root_dir_path, 'uploads', 'documents')

    file_name = uuid.uuid4()
    file_path = os.path.join(uploads_path, f'{file_name}.pdf')

    try:
        user = User()
        user.uuid = uuid.uuid4()
        db.add(user)
        db.commit()

        document = Document()
        document.user_id = user.id
        document.title = doc.filename
        document.status = 'processing'

        db.add(document)
        db.commit()
        db.refresh(document)
    except Exception as e:
        db.rollback()
        return {'message': f'there was an error saving the document metadata: {e}'}

    try:
        with open(file_path, 'wb') as f:
            while contents := doc.file.read(1024 * 1024):
                f.write(contents)
    except Exception as e:
        return {'message': f'there was an error uploading the file: {e}'}
    finally:
        doc.file.close()

    return {'message': 'successfully uploaded'}
