"""API endpoints for document management, including uploading text files."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import os
from week7.db.session import get_db
from week7.models.user import User
from week9.models.document import Document 
from week7.api.dependencies import roles_required 
from week9.constants import HUGGINGFACE_EMBEDDING_MODEL, HUGGINGFACE_COLLECTION_NAME
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.schema import Document as LangDocument
from typing import Dict, Any

router = APIRouter()

POSTGRES_URL = os.getenv("DATABASE_URL")
if not POSTGRES_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(roles_required("GET")),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Upload a text document and store its embeddings in the vector store."""

    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")

    if file.content_type not in ("text/plain", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Invalid content type")

    try:
        raw_content = await file.read()
        content = raw_content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be UTF-8 encoded text"
        )

    if not content.strip():
        raise HTTPException(status_code=400, detail="Empty file not allowed")

    document = Document(
        user_id=current_user.id,
        filename=file.filename,
        content=content,
        content_type="text/plain",
        created_at=datetime.utcnow()
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    langchain_doc = LangDocument(
        page_content=content,
        metadata={
            "user_id": current_user.id,
            "document_id": document.id,
            "filename": file.filename
        }
    )

    embeddings = HuggingFaceEmbeddings(
        model_name=HUGGINGFACE_EMBEDDING_MODEL
    )

    vectorstore = PGVector(
        collection_name=HUGGINGFACE_COLLECTION_NAME,
        embedding_function=embeddings,
        connection_string=POSTGRES_URL,
        use_jsonb=True
    )

    vectorstore.add_documents([langchain_doc])

    return {
        "message": "Document uploaded successfully",
        "document_id": document.id
    }
