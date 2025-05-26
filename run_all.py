import subprocess
import os
import sys
import time
import signal

# Đường dẫn đến các thư mục server
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
auth_api_path = os.path.join(backend_path, "auth_api")

# Biến để lưu trữ các tiến trình
processes = []

def signal_handler(sig, frame):
    print("\nĐang dừng tất cả các server...")
    for process in processes:
        if process.poll() is None:  # Nếu tiến trình vẫn đang chạy
            process.terminate()
    sys.exit(0)

# Đăng ký xử lý tín hiệu Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def start_servers():
    # Chạy main API server
    print("Khởi động Main API server...")
    main_server = subprocess.Popen(
        [sys.executable, "run.py"], 
        cwd=backend_path
    )
    processes.append(main_server)
    
    # Đợi main server khởi động
    time.sleep(2)
    
    # Chạy auth API server
    print("Khởi động Auth API server...")
    auth_server = subprocess.Popen(
        [sys.executable, "run.py"], 
        cwd=auth_api_path
    )
    processes.append(auth_server)
    
    print("\nCả hai server đã được khởi động:")
    print(f"- Main API đang chạy (PID: {main_server.pid})")
    print(f"- Auth API đang chạy (PID: {auth_server.pid})")
    print("\nNhấn Ctrl+C để dừng tất cả các server.")
    
    # Đợi cho đến khi cả hai tiến trình kết thúc
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    start_servers()
