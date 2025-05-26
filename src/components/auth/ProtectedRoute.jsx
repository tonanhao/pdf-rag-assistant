import { Navigate, useLocation, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContextNoNavigate';
import { useEffect, useState } from 'react';

const ProtectedRoute = () => {
  const { isAuthenticated, loading, user } = useAuth();
  const location = useLocation();
  const [hasChecked, setHasChecked] = useState(false);

  useEffect(() => {
    // Kiểm tra xem đã hoàn thành quá trình kiểm tra xác thực chưa
    if (!loading) {
      console.log('Protected Route - Auth Status:', { 
        isAuthenticated, 
        user, 
        loading,
        token: localStorage.getItem('token')
      });
      setHasChecked(true);
    }
  }, [isAuthenticated, user, loading]);

  // Nếu đang tải hoặc chưa kiểm tra xong, hiển thị trạng thái tải
  if (loading || !hasChecked) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  // Nếu không xác thực, chuyển hướng đến trang đăng nhập
  if (!isAuthenticated) {
    console.log('Chưa xác thực, chuyển hướng đến trang đăng nhập');
    return <Navigate to="/auth?mode=login" state={{ from: location }} replace />;
  }

  // Nếu đã auth, render tiếp các route con
  console.log('Đã xác thực, tiếp tục vào trang được bảo vệ');
  return <Outlet />;
};

export default ProtectedRoute;
