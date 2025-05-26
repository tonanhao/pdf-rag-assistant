import { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../api/authApi';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Check for existing session on mount
  useEffect(() => {
    const checkAuth = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        console.log('Kiểm tra xác thực - Token hiện tại:', token ? 'Có token' : 'Không có token');
        
        if (token) {
          // Verify token with backend
          try {
            console.log('Đang kiểm tra token với API...');
            const userData = await authApi.getCurrentUser();
            console.log('Token hợp lệ, thông tin người dùng:', userData);
            setUser(userData);
          } catch (err) {
            console.error('Token không hợp lệ hoặc hết hạn:', err);
            localStorage.removeItem('token');
            setUser(null);
          }
        } else {
          console.log('Không tìm thấy token, đặt user = null');
          setUser(null);
        }
      } catch (err) {
        console.error('Lỗi khi kiểm tra xác thực:', err);
        localStorage.removeItem('token');
        setUser(null);
      } finally {
        console.log('Hoàn thành kiểm tra xác thực');
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      setError(null);
      console.log('AuthContext: Bắt đầu đăng nhập...');
      const response = await authApi.login(email, password);
      console.log('AuthContext: API đăng nhập thành công:', response);
      // authApi.login đã lưu token vào localStorage
      
      // Lấy thông tin người dùng
      const userData = await authApi.getCurrentUser();
      console.log('AuthContext: Lấy thông tin người dùng thành công:', userData);
      
      // Đảm bảo lưu trạng thái user trước
      setUser(userData);
      
      console.log('AuthContext: Đã cập nhật trạng thái user, isAuthenticated =', !!userData);
      
      return { success: true, userData };
    } catch (err) {
      console.error('AuthContext: Lỗi đăng nhập:', err);
      const message = err.detail || 'Login failed. Please try again.';
      setError(message);
      return { success: false, error: message };
    }
  };

  const register = async (userData) => {
    try {
      setError(null);
      // Đăng ký người dùng mới
      const registerResponse = await authApi.register(userData);
      console.log('Register API response:', registerResponse);
      
      // Đăng nhập sau khi đăng ký
      const loginResponse = await authApi.login(userData.email, userData.password);
      console.log('Auto-login after register response:', loginResponse);
      
      // Lấy thông tin người dùng
      const userInfo = await authApi.getCurrentUser();
      console.log('User data after register:', userInfo);
      setUser(userInfo);
      
      return { success: true, userData: userInfo };
    } catch (err) {
      console.error('Registration error:', err);
      const message = err.detail || 'Registration failed. Please try again.';
      setError(message);
      return { success: false, error: message };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    // Không sử dụng navigate nữa
    return { success: true };
  };

  const forgotPassword = async (email) => {
    try {
      setError(null);
      await axios.post('/api/auth/forgot-password', { email });
      return { success: true };
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to send reset email. Please try again.';
      setError(message);
      return { success: false, error: message };
    }
  };

  const resetPassword = async (token, newPassword) => {
    try {
      setError(null);
      await axios.post('/api/auth/reset-password', { token, newPassword });
      return { success: true };
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to reset password. Please try again.';
      setError(message);
      return { success: false, error: message };
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}; 