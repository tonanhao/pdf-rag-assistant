import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContextNoNavigate';
import { Toaster } from './components/common/Toast';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import ImportPage from './pages/ImportPage';
import ChatPage from './pages/ChatPage';
import HistoryPage from './pages/HistoryPage';
import SettingsPage from './pages/SettingsPage';
import AuthPage from './pages/auth/auth';
import ProtectedRoute from './components/auth/ProtectedRoute';
import ResetButton from './components/common/ResetButton';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    console.log('App khởi động - Kiểm tra token:', localStorage.getItem('token') ? 'Có token' : 'Không có token');
  }, []);

  return (
    <ThemeProvider>
      <Router>
        <AuthProvider>
          <Routes>
            {/* Route riêng cho Auth (login/register/forgot) */}
            <Route path="/auth" element={<AuthPage />} />
            
            {/* Chuyển hướng từ / sang /auth */}
            <Route path="/" element={<Navigate to="/auth" replace />} />

            {/* Các route được bảo vệ (cần đăng nhập) */}
            <Route element={<ProtectedRoute />}>
              <Route element={<Layout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/import" element={<ImportPage />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/history" element={<HistoryPage />} />
                <Route path="/settings" element={<SettingsPage />} />
              </Route>
            </Route>
          </Routes>

          <Toaster />
          <ResetButton />
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default App;
