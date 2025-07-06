import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const Profile: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Profile
        </Typography>
        <Typography variant="body1">
          Instagram profile information and settings will be implemented here.
        </Typography>
      </Box>
    </Container>
  );
};

export default Profile; 