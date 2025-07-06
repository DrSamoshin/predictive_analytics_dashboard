import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const Predictions: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Predictions
        </Typography>
        <Typography variant="body1">
          AI-powered predictions and recommendations will be implemented here.
        </Typography>
      </Box>
    </Container>
  );
};

export default Predictions; 