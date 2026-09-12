from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.services.vector_service import get_vectorstore
from app.config import settings

def get_chat_response(question: str) -> str:
    """
    Executes the RAG pipeline to answer the user's question.
    """
    llm = ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        temperature=0,
        google_api_key=settings.GOOGLE_API_KEY
    )
    
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.TOP_K})
    
    # Prompt instructing the model to rely solely on the context
    system_prompt = (
        "You are a PDF question-answering assistant. "
        "Answer using the supplied PDF context. "
        "If the answer cannot be found in the supplied context, clearly state that "
        "the information is not available in the uploaded PDF. Do not invent information.\n\n"
        "Context: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    try:
        response = rag_chain.invoke(question)
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        raise e
