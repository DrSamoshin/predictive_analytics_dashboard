import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, IconButton } from '@mui/material';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Instagram, Logout, Menu } from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, logout } = useAuth();

  const isActive = (path: string) => location.pathname === path;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
          <AppBar position="static">
        <Toolbar>
          {isAuthenticated && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={onMenuClick}
              sx={{ mr: 2 }}
            >
              <Menu />
            </IconButton>
          )}
          <Instagram sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Instagram Analytics Dashboard
          </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          {isAuthenticated ? (
            <Button
              color="inherit"
              onClick={handleLogout}
              startIcon={<Logout />}
            >
              Logout
            </Button>
          ) : (
            <>
              <Button
                color="inherit"
                component={Link}
                to="/login"
                variant={isActive('/login') ? 'outlined' : 'text'}
              >
                Login
              </Button>
              <Button
                color="inherit"
                component={Link}
                to="/register"
                variant={isActive('/register') ? 'outlined' : 'text'}
              >
                Register
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 