import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const Analytics: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Analytics
        </Typography>
        <Typography variant="body1">
          Detailed analytics charts and insights will be implemented here.
        </Typography>
      </Box>
    </Container>
  );
};

export default Analytics; 