/**
 * AuthContext — Authentication context
 *
 * TODO: This auth system is not yet connected to the backend.
 * The backend (port 8001) does not currently expose /api/auth/* endpoints.
 * This file is a placeholder for future auth implementation.
 *
 * To activate: mount AuthProvider in App.jsx and add auth routes to backend.
 */
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user] = useState(null);

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};