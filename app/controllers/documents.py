import os
import uuid

from fastapi import APIRouter, UploadFile, File

from app.dtos.common import NotFoundResponse

router = APIRouter(
    prefix='/documents',
    tags=['Document'],
    responses=NotFoundResponse,
)


@router.post('/uploads')
async def store(doc: UploadFile = File(...)):
    current_file_path = os.path.abspath(__file__)
    current_dir_path = os.path.dirname(current_file_path)
    root_dir_path = os.path.abspath(os.path.join(current_dir_path, '..', '..'))
    uploads_path = os.path.join(root_dir_path, 'uploads', 'documents')

    file_name = uuid.uuid4()
    file_path = os.path.join(uploads_path, f'{file_name}.pdf')

    try:
        with open(file_path, 'wb') as f:
            while contents := doc.file.read(1024 * 1024):
                f.write(contents)
    except Exception as e:
        return {'message': f'there was an error uploading the file: {e}'}
    finally:
        doc.file.close()

    return {'message': 'successfully uploaded'}
