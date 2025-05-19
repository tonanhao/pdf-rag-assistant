# RAG with LangChain Demo

A demonstration of Retrieval Augmented Generation using LangChain with PDF document storage and chat history.

## Setup

### Backend (FastAPI with Conda)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a Conda environment:
```bash
conda create -n rag-demo python=3.10
conda activate rag-demo
```

3. Install dependencies:
```bash
conda install -c conda-forge fastapi uvicorn
pip install python-multipart python-dotenv pydantic
```

4. Run the backend server:
```bash
python run.py
```

The backend API will be available at http://localhost:8000.

### Frontend (React)

1. Install npm dependencies:
```bash
npm install
```

2. Run the frontend development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173.

## Features

- Upload and process PDF documents
- Chat with documents using RAG
- Save and browse conversation history with PDF attachments
