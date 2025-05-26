import uvicorn
from app import app
from app.core.database import Base, engine

# Tạo bảng trong database
Base.metadata.create_all(bind=engine)

def start():
    """Hàm khởi động ứng dụng"""
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )

if __name__ == "__main__":
    start()
