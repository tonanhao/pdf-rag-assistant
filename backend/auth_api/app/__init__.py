from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RAGvLangChain Auth API",
    description="API xác thực cho ứng dụng RAGvLangChain",
    version="0.1.0",
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường production, cần giới hạn nguồn gốc
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import các routes
from app.routes import auth, users

# Đăng ký các routes
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Chào mừng đến với RAGvLangChain Auth API!"}
