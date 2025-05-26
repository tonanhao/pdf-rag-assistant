# Script PowerShell để chạy cả hai server API
# Lưu file này với tên start_servers.ps1

Write-Host "Bắt đầu khởi động các server API..." -ForegroundColor Green

# Đường dẫn đến thư mục chứa các server
$backendPath = "\\wsl.localhost\Ubuntu\home\phongle\RAGvLangChain_demov1\backend"
$authApiPath = "\\wsl.localhost\Ubuntu\home\phongle\RAGvLangChain_demov1\backend\auth_api"

# Chạy API chính trong tiến trình thứ nhất
Start-Process -FilePath "powershell.exe" -ArgumentList "-Command `"cd '$backendPath'; python run.py`"" -NoNewWindow

# Chờ một chút để server đầu tiên khởi động
Start-Sleep -Seconds 2

# Chạy auth API trong tiến trình thứ hai
Start-Process -FilePath "powershell.exe" -ArgumentList "-Command `"cd '$authApiPath'; python run.py`"" -NoNewWindow

Write-Host "Cả hai server đã được khởi động!" -ForegroundColor Green
Write-Host "- Main API server đang chạy"
Write-Host "- Auth API server đang chạy"
Write-Host "Nhấn Ctrl+C để dừng tất cả các server." -ForegroundColor Yellow

# Giữ script chạy để dễ dàng dừng cả hai server cùng lúc
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "Đang dừng các server..." -ForegroundColor Red
}
