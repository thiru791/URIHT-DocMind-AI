from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.db.database import SessionLocal
from app.models.document import Document
from app.services.pdf_service import extract_text
from app.services.ai_service import generate_summary, answer_question
from app.services.embedding_service import (
    create_vector_store,
    split_document,
    search_document
)


# --------------------------------------------------
# Router
# --------------------------------------------------

router = APIRouter()


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class SummaryRequest(BaseModel):
    id: int


class ChatRequest(BaseModel):
    question: str


# --------------------------------------------------
# Upload configuration
# --------------------------------------------------

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_text(str(file_path))

    # Split document
    chunks = split_document(text)

    # Save document information
    db = SessionLocal()

    document = Document(
        filename=file.filename,
        filepath=str(file_path),
        characters=len(text)
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Create vector store
    vector_count = create_vector_store(
        document.id,
        chunks
    )

    db.close()

    return {
        "id": document.id,
        "filename": document.filename,
        "characters": document.characters,
        "chunks": len(chunks),
        "vectors": vector_count,
        "preview": chunks[0][:250] if chunks else ""
    }


# --------------------------------------------------
# Generate Summary
# --------------------------------------------------

@router.post("/summary")
def summary(request: SummaryRequest):

    try:

        db = SessionLocal()

        document = db.query(Document).filter(
            Document.id == request.id
        ).first()

        db.close()

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        print("Document found:", document.filename)

        text = extract_text(document.filepath)

        print("Text extracted:", len(text))

        summary_text = generate_summary(text)

        print("Summary generated successfully")

        return {
            "id": document.id,
            "summary": summary_text
        }

    except HTTPException:
        raise

    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# Chat with document
# --------------------------------------------------

@router.post("/chat")
def chat(request: ChatRequest):

    try:

        context = search_document(request.question)

        context = "\n\n".join(context)

        answer = answer_question(
            request.question,
            context
        )

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )