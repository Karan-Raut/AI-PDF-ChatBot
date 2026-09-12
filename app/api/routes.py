from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from pathlib import Path
from app.models import QuestionRequest, QuestionResponse, UploadResponse
from app.config import settings
from app.services.pdf_service import extract_text_from_pdf
from app.services.embedding_service import chunk_text
from app.services.vector_service import add_documents_to_vectorstore
from app.services.chat_service import get_chat_response

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
        
    try:
        # Save file securely
        file_path = os.path.join(settings.UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Extract text
        text = extract_text_from_pdf(file_path)
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF. It might be empty or scanned.")
            
        # Chunk text
        chunks = chunk_text(text)
        
        # Add to vector store
        add_documents_to_vectorstore(chunks)
        
        return UploadResponse(
            message="PDF uploaded successfully",
            filename=file.filename,
            chunks=len(chunks)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        answer = get_chat_response(request.question)
        return QuestionResponse(answer=answer)
    except Exception as e:
        # In a real app we might not expose raw stack traces, but providing error details for debugging
        raise HTTPException(status_code=500, detail="Failed to retrieve an answer from the LLM or Vector store.")
