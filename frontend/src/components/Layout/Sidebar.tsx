/**
 * Sidebar navigation component
 */

import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Divider,
} from '@mui/material';
import {
  Dashboard,
  Analytics,
  TrendingUp,
  Person,
  Instagram,
} from '@mui/icons-material';
import { Link, useLocation } from 'react-router-dom';

const SIDEBAR_WIDTH = 240;

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  const menuItems = [
    {
      text: 'Dashboard',
      icon: <Dashboard />,
      path: '/dashboard',
    },
    {
      text: 'Analytics',
      icon: <Analytics />,
      path: '/analytics',
    },
    {
      text: 'Predictions',
      icon: <TrendingUp />,
      path: '/predictions',
    },
    {
      text: 'Instagram',
      icon: <Instagram />,
      path: '/instagram',
    },
    {
      text: 'Profile',
      icon: <Person />,
      path: '/profile',
    },
  ];

  const sidebarContent = (
    <Box sx={{ width: SIDEBAR_WIDTH, pt: 2 }}>
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              component={Link}
              to={item.path}
              selected={isActive(item.path)}
              onClick={onClose}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: 'primary.main',
                  color: 'primary.contrastText',
                  '& .MuiListItemIcon-root': {
                    color: 'primary.contrastText',
                  },
                  '&:hover': {
                    backgroundColor: 'primary.dark',
                  },
                },
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Drawer
      variant="temporary"
      open={open}
      onClose={onClose}
      ModalProps={{
        keepMounted: true, // Better open performance on mobile
      }}
      sx={{
        '& .MuiDrawer-paper': {
          width: SIDEBAR_WIDTH,
          boxSizing: 'border-box',
        },
      }}
    >
      {sidebarContent}
    </Drawer>
  );
};

export default Sidebar; 