import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import './App.css';
import AppRoutes from './routes/AppRoutes';
import MainLayout from './components/Layout/MainLayout';
import { AuthProvider } from './context/AuthContext';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AuthProvider>
          <div className="App">
            <MainLayout>
              <AppRoutes />
            </MainLayout>
          </div>
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default App; 