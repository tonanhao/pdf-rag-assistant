import axios from 'axios';

// Cấu hình API client
const API_URL = 'http://localhost:8002'; // URL của FastAPI backend

// Tạo instance axios với URL cơ sở
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Thêm interceptor để xử lý token xác thực
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Thêm interceptor để xử lý lỗi response
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API auth
export const authApi = {  // Đăng nhập
  login: async (email, password) => {
    try {
      console.log('API: Đang gọi API đăng nhập với email:', email);
      const response = await apiClient.post('/auth/login/json', { email, password });
      console.log('API: Đăng nhập thành công, response:', response.data);
      localStorage.setItem('token', response.data.access_token);
      console.log('API: Token đã được lưu:', response.data.access_token);
      return response.data;
    } catch (error) {
      console.error('API: Lỗi đăng nhập:', error.response?.data || error.message);
      throw error.response?.data || { detail: 'Đã xảy ra lỗi khi đăng nhập' };
    }
  },

  // Đăng ký
  register: async (userData) => {
    try {
      const response = await apiClient.post('/users', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Đã xảy ra lỗi khi đăng ký' };
    }
  },

  // Quên mật khẩu
  forgotPassword: async (email) => {
    try {
      const response = await apiClient.post('/auth/forgot-password', { email });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Đã xảy ra lỗi khi xử lý yêu cầu quên mật khẩu' };
    }
  },
  // Lấy thông tin người dùng hiện tại
  getCurrentUser: async () => {
    try {
      console.log('API: Đang lấy thông tin người dùng hiện tại...');
      const response = await apiClient.get('/users/me');
      console.log('API: Lấy thông tin thành công:', response.data);
      return response.data;
    } catch (error) {
      console.error('API: Lỗi khi lấy thông tin người dùng:', error.response?.data || error.message);
      throw error.response?.data || { detail: 'Không thể lấy thông tin người dùng' };
    }
  },

  // Đăng xuất
  logout: () => {
    localStorage.removeItem('token');
  }
};

export default apiClient;
