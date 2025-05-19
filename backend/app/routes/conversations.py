from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Body
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import json
import os
from pathlib import Path
import uuid
from datetime import datetime
import shutil

from ..models import Conversation, ConversationCreate, ConversationUpdate, Message
from ..config import BASE_DIR, UPLOAD_DIR, CONVERSATION_DIR

router = APIRouter(prefix="/conversations", tags=["conversations"])

# Helper function to check if a conversation is empty
def is_conversation_empty(conversation):
    # A conversation is considered empty if it has no messages
    # or all messages are empty strings
    if not conversation.get("messages"):
        return True
    
    return all(
        not msg.get("content") or msg.get("content").strip() == "" 
        for msg in conversation.get("messages", [])
    )

# Helper function to load conversations
def load_conversations():
    conversations = []
    for file_path in CONVERSATION_DIR.glob("*.json"):
        try:
            with open(file_path, "r") as f:
                conversation = json.load(f)
                
                # Skip empty conversations
                if is_conversation_empty(conversation) and not conversation.get("pdf_file"):
                    continue
                
                # Ensure message IDs are strings for compatibility
                if "messages" in conversation and conversation["messages"]:
                    for msg in conversation["messages"]:
                        if "id" in msg and not isinstance(msg["id"], str):
                            msg["id"] = str(msg["id"])
                
                conversations.append(conversation)
        except Exception as e:
            print(f"Error loading conversation {file_path}: {e}")
    return conversations

@router.get("/", response_model=List[Conversation])
async def get_conversations():
    return load_conversations()

@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    file_path = CONVERSATION_DIR / f"{conversation_id}.json"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    with open(file_path, "r") as f:
        conversation = json.load(f)
        
        # Ensure message IDs are strings for compatibility
        if "messages" in conversation and conversation["messages"]:
            for msg in conversation["messages"]:
                if "id" in msg and not isinstance(msg["id"], str):
                    msg["id"] = str(msg["id"])
        
        return conversation

@router.post("/", response_model=Conversation)
async def create_conversation(
    title: str = Form(...),
    last_message: str = Form(...),
    pdf_file: Optional[UploadFile] = File(None)
):
    # Skip empty conversations without PDF
    if not pdf_file and not title.strip() and not last_message.strip():
        return JSONResponse(status_code=400, content={"detail": "Cannot create empty conversation without PDF"})
    
    conversation_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    conversation = {
        "id": conversation_id,
        "title": title,
        "lastMessage": last_message,
        "timestamp": timestamp,
        "messages": [],
        "pdf_file": None
    }
    
    # Handle PDF file upload if present
    if pdf_file:
        # Save the file
        file_extension = os.path.splitext(pdf_file.filename)[1]
        file_name = f"{conversation_id}{file_extension}"
        file_path = UPLOAD_DIR / file_name
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(pdf_file.file, f)
        
        conversation["pdf_file"] = str(file_path)
    
    # Save conversation
    with open(CONVERSATION_DIR / f"{conversation_id}.json", "w") as f:
        json.dump(conversation, f)
    
    return conversation

@router.put("/{conversation_id}")
async def update_conversation(
    conversation_id: str,
    update_data: Dict[str, Any] = Body(...)
):
    file_path = CONVERSATION_DIR / f"{conversation_id}.json"
    
    # Check if conversation exists, create it if not
    if not file_path.exists():
        print(f"Creating new conversation with ID: {conversation_id}")
        timestamp = datetime.now().isoformat()
        
        # Create a new conversation with the given ID
        conversation = {
            "id": conversation_id,
            "title": update_data.get("title", f"Conversation {conversation_id}"),
            "lastMessage": update_data.get("lastMessage", ""),
            "timestamp": update_data.get("timestamp", timestamp),
            "messages": update_data.get("messages", []),
            "pdf_file": update_data.get("pdf_file", None)
        }
        
        # Check if the new conversation is empty without PDF
        if is_conversation_empty(conversation) and not conversation.get("pdf_file"):
            return JSONResponse(content={"detail": "Skipping empty conversation"})
    else:
        # Load existing conversation
        with open(file_path, "r") as f:
            conversation = json.load(f)
    
    # Update fields
    if "title" in update_data:
        conversation["title"] = update_data["title"]
    
    if "lastMessage" in update_data:
        conversation["lastMessage"] = update_data["lastMessage"]
    
    if "messages" in update_data:
        conversation["messages"] = update_data["messages"]
        
    if "timestamp" in update_data:
        conversation["timestamp"] = update_data["timestamp"]
    
    # Check if the updated conversation is empty
    if is_conversation_empty(conversation) and not conversation.get("pdf_file"):
        # If the file exists, we might want to delete it since it's now empty
        if file_path.exists():
            file_path.unlink()
        return JSONResponse(content={"detail": "Conversation is empty, not saving"})
    
    # Save updated conversation
    with open(file_path, "w") as f:
        json.dump(conversation, f)
    
    return conversation

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    file_path = CONVERSATION_DIR / f"{conversation_id}.json"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Load conversation to check if there's an associated PDF
    with open(file_path, "r") as f:
        conversation = json.load(f)
    
    # Delete the PDF file if it exists
    if conversation.get("pdf_file"):
        pdf_path = Path(conversation["pdf_file"])
        if pdf_path.exists():
            pdf_path.unlink()
    
    # Delete the conversation file
    file_path.unlink()
    
    return JSONResponse(content={"message": "Conversation deleted successfully"}) 