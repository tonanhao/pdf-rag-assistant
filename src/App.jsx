import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { Toaster } from './components/common/Toast';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import ImportPage from './pages/ImportPage';
import ChatPage from './pages/ChatPage';
import HistoryPage from './pages/HistoryPage';
import SettingsPage from './pages/SettingsPage';
import AuthPage from './pages/auth/auth';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Routes>
          {/* Route riêng cho Auth (login/register/forgot) */}
          <Route path="/auth" element={<AuthPage />} />

          {/* Các route khác sẽ được bọc trong Layout */}
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/import" element={<ImportPage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Routes>

        <Toaster />
      </Router>
    </ThemeProvider>
  );
}

export default App;
