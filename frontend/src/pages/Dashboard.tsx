import React from 'react';
import { Container, Typography, Grid, Paper, Box } from '@mui/material';

const Dashboard: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h6">Total Followers</Typography>
              <Typography variant="h3" color="primary">
                12.5K
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h6">Engagement Rate</Typography>
              <Typography variant="h3" color="secondary">
                4.2%
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h6">Posts This Month</Typography>
              <Typography variant="h3" color="success.main">
                24
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h6">Avg. Likes per Post</Typography>
              <Typography variant="h3" color="info.main">
                523
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <Typography>
                Chart components will be implemented here
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard; 