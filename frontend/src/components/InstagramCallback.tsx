import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Box, CircularProgress, Typography, Alert } from '@mui/material';
import { apiService } from '../services/api';

const InstagramCallback: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(true);

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const state = searchParams.get('state');
      const errorParam = searchParams.get('error');
      const errorDescription = searchParams.get('error_description');

      if (errorParam) {
        setError(errorDescription || 'Instagram authorization was denied');
        setProcessing(false);
        return;
      }

      if (!code || !state) {
        setError('Missing authorization code or state parameter');
        setProcessing(false);
        return;
      }

      try {
        await apiService.handleInstagramCallback(code, state);
        
        // Success - redirect to Instagram page
        navigate('/instagram', { 
          replace: true,
          state: { message: 'Instagram account connected successfully!' }
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to connect Instagram account');
        setProcessing(false);
      }
    };

    handleCallback();
  }, [navigate, searchParams]);

  const handleRetry = () => {
    navigate('/instagram');
  };

  if (processing) {
    return (
      <Box 
        sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          justifyContent: 'center', 
          height: '100vh',
          gap: 2
        }}
      >
        <CircularProgress size={60} />
        <Typography variant="h6">
          Connecting your Instagram account...
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Please wait while we process your authorization
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box 
        sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          justifyContent: 'center', 
          height: '100vh',
          gap: 2,
          px: 3
        }}
      >
        <Alert severity="error" sx={{ maxWidth: 500 }}>
          <Typography variant="h6" gutterBottom>
            Connection Failed
          </Typography>
          <Typography variant="body2">
            {error}
          </Typography>
        </Alert>
        
        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
          <button 
            onClick={handleRetry}
            style={{
              padding: '10px 20px',
              backgroundColor: '#1976d2',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Try Again
          </button>
        </Box>
      </Box>
    );
  }

  return null;
};

export default InstagramCallback; 