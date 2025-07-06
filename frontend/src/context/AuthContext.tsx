/**
 * Authentication context for managing user state
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, apiService } from '../services/api';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (login: string, password: string) => Promise<void>;
  register: (data: {
    email: string;
    username: string;
    password: string;
    first_name?: string;
    last_name?: string;
  }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      if (apiService.isAuthenticated()) {
        try {
          const currentUser = await apiService.getCurrentUser();
          setUser(currentUser);
        } catch (error) {
          console.error('Failed to get current user:', error);
          apiService.logout();
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (login: string, password: string) => {
    try {
      await apiService.login({ login, password });
      const currentUser = await apiService.getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      throw error;
    }
  };

  const register = async (data: {
    email: string;
    username: string;
    password: string;
    first_name?: string;
    last_name?: string;
  }) => {
    try {
      const newUser = await apiService.register(data);
      // Auto login after registration using email
      await login(data.email, data.password);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    apiService.logout();
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 