from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask about the PDF.")

class QuestionResponse(BaseModel):
    answer: str

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks: int
