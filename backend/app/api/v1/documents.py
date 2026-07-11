from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.auth.current_user import get_current_user
from app.models.user import User

from app.services.document_service import (
    upload_document,
    document_history,
    get_single_document,
    search_document,
    download_document,
    delete_document_service
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# -------------------------------------------------
# Upload Document
# -------------------------------------------------

@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await upload_document(
        file=file,
        db=db,
        current_user=current_user
    )


# -------------------------------------------------
# Document History
# -------------------------------------------------

@router.get("/history")
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return document_history(
        db=db,
        current_user=current_user
    )


# -------------------------------------------------
# Search Documents
# -------------------------------------------------

@router.get("/search")
def search(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return search_document(
        db=db,
        current_user=current_user,
        query=q
    )


# -------------------------------------------------
# Download PDF
# -------------------------------------------------

@router.get("/download/{document_id}")
def download(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return download_document(
        db=db,
        current_user=current_user,
        document_id=document_id
    )


# -------------------------------------------------
# Get Single Document
# -------------------------------------------------

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_single_document(
        db=db,
        current_user=current_user,
        document_id=document_id
    )


# -------------------------------------------------
# Delete Document
# -------------------------------------------------

@router.delete("/{document_id}")
def delete(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_document_service(
        db=db,
        current_user=current_user,
        document_id=document_id
    )