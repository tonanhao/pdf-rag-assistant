from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

# Import shared configuration
from .config import BASE_DIR, UPLOAD_DIR, CONVERSATION_DIR

app = FastAPI(title="Chat History API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from .routes import conversations, documents

app.include_router(conversations.router)
app.include_router(documents.router)

@app.get("/")
async def root():
    return {"message": "Chat History API is running on port 8001"} 