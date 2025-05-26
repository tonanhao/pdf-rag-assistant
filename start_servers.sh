#!/bin/bash
# Script để chạy cả hai server API

echo "Bắt đầu khởi động các server API..."

# Đường dẫn đến thư mục chứa các server
BACKEND_PATH="/home/phongle/RAGvLangChain_demov1/backend"
AUTH_API_PATH="/home/phongle/RAGvLangChain_demov1/backend/auth_api"

# Chạy API chính trong background
cd $BACKEND_PATH
python run.py &
MAIN_PID=$!

# Chờ một chút để server đầu tiên khởi động
sleep 2

# Chạy auth API trong background
cd $AUTH_API_PATH
python run.py &
AUTH_PID=$!

echo "Cả hai server đã được khởi động!"
echo "- Main API server đang chạy (PID: $MAIN_PID)"
echo "- Auth API server đang chạy (PID: $AUTH_PID)"
echo "Nhấn Ctrl+C để dừng tất cả các server."

# Xử lý tín hiệu SIGINT (Ctrl+C) để dừng các server
function cleanup {
    echo "Đang dừng các server..."
    kill $MAIN_PID
    kill $AUTH_PID
    exit 0
}

trap cleanup SIGINT

# Giữ script chạy
wait
