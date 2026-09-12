from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from typing import List
from app.config import settings
import os

# We initialize embeddings and vector store instances
_embeddings = None
_vectorstore = None

def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2", 
            google_api_key=settings.GOOGLE_API_KEY
        )
    return _embeddings

def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=settings.VECTOR_DB_PATH,
            embedding_function=get_embeddings()
        )
    return _vectorstore

def add_documents_to_vectorstore(documents: List[Document]) -> None:
    """
    Adds document chunks to the Chroma vector store.
    """
    vs = get_vectorstore()
    vs.add_documents(documents)

def search_similar_documents(query: str, k: int = None) -> List[Document]:
    """
    Searches for similar documents based on the query.
    """
    if k is None:
        k = settings.TOP_K
        
    vs = get_vectorstore()
    return vs.similarity_search(query, k=k)

def clear_vectorstore() -> None:
    """
    (Optional) Clears the vector store. Useful if you want to support
    only the latest uploaded PDF. Currently, this resets the collection.
    """
    global _vectorstore
    if _vectorstore is not None:
        _vectorstore.delete_collection()
        _vectorstore = None
