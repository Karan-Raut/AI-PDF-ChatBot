from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document
from app.config import settings

def chunk_text(text: str) -> List[Document]:
    """
    Splits the extracted text into manageable chunks for embeddings.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # We wrap the text in a Document for consistency with LangChain
    chunks = splitter.create_documents([text])
    return chunks
