import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from '../pages/Dashboard';
import Analytics from '../pages/Analytics';
import Predictions from '../pages/Predictions';
import Profile from '../pages/Profile';
import Instagram from '../pages/Instagram';
import InstagramCallback from '../components/InstagramCallback';
import Login from '../pages/Login';
import Register from '../pages/Register';
import ProtectedRoute from '../components/Layout/ProtectedRoute';
import { useAuth } from '../context/AuthContext';

const AppRoutes: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      {/* Public routes */}
      <Route 
        path="/login" 
        element={
          isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />
        } 
      />
      <Route 
        path="/register" 
        element={
          isAuthenticated ? <Navigate to="/dashboard" replace /> : <Register />
        } 
      />
      
      {/* Protected routes */}
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/analytics" 
        element={
          <ProtectedRoute>
            <Analytics />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/predictions" 
        element={
          <ProtectedRoute>
            <Predictions />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/instagram" 
        element={
          <ProtectedRoute>
            <Instagram />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/instagram/callback" 
        element={
          <ProtectedRoute>
            <InstagramCallback />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/profile" 
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        } 
      />
      
      {/* Default redirect */}
      <Route 
        path="/" 
        element={
          <Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />
        } 
      />
    </Routes>
  );
};

export default AppRoutes; 