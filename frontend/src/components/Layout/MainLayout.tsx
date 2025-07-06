/**
 * Main layout component that includes header and sidebar
 */

import React, { useState } from 'react';
import { Box } from '@mui/material';
import Header from './Header';
import Sidebar from './Sidebar';
import { useAuth } from '../../context/AuthContext';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { isAuthenticated } = useAuth();

  const handleMenuClick = () => {
    setSidebarOpen(true);
  };

  const handleSidebarClose = () => {
    setSidebarOpen(false);
  };

  return (
    <>
      <Header onMenuClick={handleMenuClick} />
      {isAuthenticated && (
        <Sidebar open={sidebarOpen} onClose={handleSidebarClose} />
      )}
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        {children}
      </Box>
    </>
  );
};

export default MainLayout; 