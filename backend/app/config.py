from pathlib import Path

# Get the absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Create uploads directory if it doesn't exist
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Create conversations directory if it doesn't exist
CONVERSATION_DIR = BASE_DIR / "conversations"
CONVERSATION_DIR.mkdir(parents=True, exist_ok=True)