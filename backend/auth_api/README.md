# Hướng dẫn Cài đặt và Sử dụng

## Backend Authentication API

### Cài đặt thư viện
```bash
cd backend/auth_api
pip install -r requirements.txt
```

### Chạy backend
```bash
cd backend/auth_api
python run.py
```

Server sẽ chạy tại địa chỉ http://localhost:8002

## API Endpoints

### Authentication
- `POST /auth/login/json` - Đăng nhập (JSON)
- `POST /auth/login` - Đăng nhập (Form)
- `POST /auth/forgot-password` - Quên mật khẩu
- `POST /auth/reset-password` - Đặt lại mật khẩu

### Users
- `POST /users` - Đăng ký tài khoản mới
- `GET /users/me` - Lấy thông tin người dùng hiện tại

## Frontend React

### Cài đặt thư viện
```bash
npm install axios
```

### Mô tả chức năng
- **Đăng nhập**: Người dùng có thể đăng nhập bằng email và mật khẩu
- **Đăng ký**: Tạo tài khoản mới với thông tin cá nhân
- **Quên mật khẩu**: Yêu cầu đặt lại mật khẩu qua email

### Lưu ý
- API backend sử dụng SQLite làm cơ sở dữ liệu đơn giản
- Trong môi trường thực tế, bạn nên:
  - Sử dụng HTTPS
  - Giới hạn CORS origins
  - Thiết lập email service để gửi email xác thực
  - Sử dụng cơ sở dữ liệu mạnh mẽ hơn (PostgreSQL, MySQL)
