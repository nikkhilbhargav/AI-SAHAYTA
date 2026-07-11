from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.services.document_service import upload_document
from app.database.session import get_db

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await upload_document(
        file=file,
        db=db
    )