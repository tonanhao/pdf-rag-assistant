print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!! EXECUTING backend/app/config.py NOW !!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

from pathlib import Path
import os
from dotenv import load_dotenv

# Get the absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
dotenv_path = BASE_DIR / ".env"
print(f"[Config Main API] Attempting to load .env file from: {dotenv_path}")
loaded_successfully = load_dotenv(dotenv_path=dotenv_path, verbose=True)
print(f"[Config Main API] .env loaded successfully: {loaded_successfully}")

# DEBUG: Print a specific value directly after loading to confirm
print(f"[Config Main API] SECRET_KEY from os.environ after load_dotenv: {os.environ.get('SECRET_KEY')}")
print(f"[Config Main API] ALGORITHM from os.environ after load_dotenv: {os.environ.get('ALGORITHM')}")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Create conversations directory if it doesn't exist
CONVERSATION_DIR = BASE_DIR / "conversations"
CONVERSATION_DIR.mkdir(parents=True, exist_ok=True)

# JWT settings
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecret")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

print(f"[Config Main API] Final SECRET_KEY in use: {SECRET_KEY}")