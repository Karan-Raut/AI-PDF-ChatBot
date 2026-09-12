# AI PDF Chatbot

A complete, production-ready AI PDF Chatbot built with FastAPI, LangChain, ChromaDB, and OpenAI.

## Features
- Clean, modern, dark-mode glassmorphism UI.
- Secure PDF upload and parsing.
- Intelligent text chunking and vector embeddings.
- RAG (Retrieval-Augmented Generation) question answering strictly based on the PDF context.
- Dockerized setup and comprehensive error handling.

## Prerequisites
- Python 3.12+
- Docker (optional, for containerized run)
- OpenAI API Key

## Setup Instructions (Windows)

1. **Clone or Extract the Project**
   Navigate to the project directory:
   ```powershell
   cd pdf-chatbot
   ```

2. **Create a Virtual Environment**
   ```powershell
   python -m venv venv
   ```

3. **Activate the Virtual Environment**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   *(If you get an execution policy error, run: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`)*

4. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**
   Rename `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
   Open `.env` in your editor and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## Running the Application Locally

Start the FastAPI server using Uvicorn:
```powershell
uvicorn app.main:app --reload
```

- **Frontend Application**: Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000/)
- **Swagger Documentation**: Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## How to Test

### 1. Uploading a PDF
- Open the web interface at `http://127.0.0.1:8000`.
- Click "Select PDF" and choose a valid PDF file.
- Click "Upload & Process".
- You will see a success message indicating the number of chunks processed.

### 2. Asking Questions
- Once uploaded, the chat input at the bottom will unlock.
- Ask a question like "What is the main topic of this document?".
- The AI will respond strictly using the context of the uploaded PDF.

## Running with Docker

If you prefer to run using Docker:
```powershell
docker-compose up --build
```
This maps the internal data volumes to your host machine so uploads and vector databases persist.

## Architecture & Code Quality
- **Separation of Concerns**: FastAPI routes are in `api/routes.py`, business logic is strictly separated into `services/` (PDF, Vector, Embeddings, Chat).
- **Modern Langchain**: Uses `langchain-openai` and `langchain-chroma` (resolving old deprecation warnings).
- **Security**: The backend never exposes the raw `.env` variables or API keys. Uploads are strictly validated to `.pdf`.
- **Validation**: Strict Pydantic v2 schemas.
