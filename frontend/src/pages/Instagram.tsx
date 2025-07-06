import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Grid,
  Alert,
  CircularProgress,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  AlertTitle,
} from '@mui/material';
import {
  Instagram as InstagramIcon,
  Refresh as RefreshIcon,
  Delete as DeleteIcon,
  Visibility as VisibilityIcon,
  Close as CloseIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { apiService, InstagramAccount, InstagramMedia } from '../services/api';

const Instagram: React.FC = () => {
  const location = useLocation();
  const [accounts, setAccounts] = useState<InstagramAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [connectingAccount, setConnectingAccount] = useState(false);
  const [syncingAccountId, setSyncingAccountId] = useState<number | null>(null);
  const [selectedMedia, setSelectedMedia] = useState<InstagramMedia[]>([]);
  const [mediaDialogOpen, setMediaDialogOpen] = useState(false);
  const [loadingMedia, setLoadingMedia] = useState(false);

  useEffect(() => {
    loadAccounts();
    
    // Check for success message from navigation state
    if (location.state?.message) {
      setSuccessMessage(location.state.message);
      // Clear the state to prevent showing message on refresh
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [location]);

  const loadAccounts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getInstagramAccounts();
      setAccounts(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load Instagram accounts');
    } finally {
      setLoading(false);
    }
  };

  const handleConnectInstagram = async () => {
    try {
      setConnectingAccount(true);
      setError(null);
      const { auth_url } = await apiService.getInstagramAuthUrl();
      window.location.href = auth_url;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect Instagram account');
      setConnectingAccount(false);
    }
  };

  const handleSyncAccount = async (accountId: number) => {
    try {
      setSyncingAccountId(accountId);
      setError(null);
      const result = await apiService.syncInstagramAccount(accountId);
      
      // Show success message or update UI
      setSuccessMessage(`Successfully synced ${result.synced_media_count} media posts`);
      
      // Reload accounts to update media count
      await loadAccounts();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to sync Instagram account');
    } finally {
      setSyncingAccountId(null);
    }
  };

  const handleDisconnectAccount = async (accountId: number) => {
    if (!window.confirm('Are you sure you want to disconnect this Instagram account?')) {
      return;
    }

    try {
      setError(null);
      await apiService.disconnectInstagramAccount(accountId);
      await loadAccounts();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to disconnect Instagram account');
    }
  };

  const handleViewMedia = async (accountId: number) => {
    try {
      setLoadingMedia(true);
      setError(null);
      const media = await apiService.getInstagramMedia(accountId);
      setSelectedMedia(media);
      setMediaDialogOpen(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load Instagram media');
    } finally {
      setLoadingMedia(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Instagram Accounts
        </Typography>
        <Button
          variant="contained"
          startIcon={<InstagramIcon />}
          onClick={handleConnectInstagram}
          disabled={connectingAccount}
        >
          {connectingAccount ? 'Connecting...' : 'Connect Instagram Account'}
        </Button>
      </Box>

      {/* Critical Deprecation Warning */}
      <Alert severity="error" sx={{ mb: 3 }}>
        <AlertTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <WarningIcon />
            CRITICAL: Instagram Basic Display API Deprecated
          </Box>
        </AlertTitle>
        <Typography variant="body2" sx={{ mb: 1 }}>
          <strong>Instagram Basic Display API was permanently disabled on December 4, 2024.</strong>
        </Typography>
        <Typography variant="body2" sx={{ mb: 1 }}>
          • New Instagram connections are no longer possible
        </Typography>
        <Typography variant="body2" sx={{ mb: 1 }}>
          • Data synchronization is disabled
        </Typography>
        <Typography variant="body2" sx={{ mb: 1 }}>
          • Only historical data from database is available
        </Typography>
        <Typography variant="body2" sx={{ mt: 2 }}>
          For business accounts, consider migrating to{' '}
          <strong>Instagram API with Instagram Login</strong> or{' '}
          <strong>Instagram API with Facebook Login</strong>.
        </Typography>
      </Alert>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {successMessage && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccessMessage(null)}>
          {successMessage}
        </Alert>
      )}

      {accounts.length === 0 ? (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 6 }}>
            <InstagramIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              No Instagram accounts connected
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Connect your Instagram account to start analyzing your content performance
            </Typography>
            <Button
              variant="contained"
              startIcon={<InstagramIcon />}
              onClick={handleConnectInstagram}
              disabled={connectingAccount}
            >
              Connect Instagram Account
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {accounts.map((account) => (
            <Grid item xs={12} md={6} lg={4} key={account.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <InstagramIcon sx={{ mr: 1, color: '#E4405F' }} />
                    <Typography variant="h6" component="h2">
                      @{account.username}
                    </Typography>
                  </Box>

                  <Box sx={{ mb: 2 }}>
                    <Chip
                      label={account.account_type}
                      size="small"
                      color={account.account_type === 'BUSINESS' ? 'primary' : 'default'}
                      sx={{ mr: 1 }}
                    />
                    <Chip
                      label={account.is_active ? 'Active' : 'Inactive'}
                      size="small"
                      color={account.is_active ? 'success' : 'error'}
                    />
                  </Box>

                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Connected: {formatDate(account.created_at)}
                  </Typography>

                  {account.media_count !== undefined && (
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Media posts: {account.media_count}
                    </Typography>
                  )}

                  {account.followers_count !== undefined && (
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Followers: {account.followers_count.toLocaleString()}
                    </Typography>
                  )}

                  {account.token_expires_at && (
                    <Typography variant="body2" color="text.secondary">
                      Token expires: {formatDate(account.token_expires_at)}
                    </Typography>
                  )}
                </CardContent>

                <CardActions>
                  <IconButton
                    onClick={() => handleSyncAccount(account.id)}
                    disabled={syncingAccountId === account.id}
                    title="Sync data"
                  >
                    {syncingAccountId === account.id ? (
                      <CircularProgress size={20} />
                    ) : (
                      <RefreshIcon />
                    )}
                  </IconButton>

                  <IconButton
                    onClick={() => handleViewMedia(account.id)}
                    title="View media"
                  >
                    <VisibilityIcon />
                  </IconButton>

                  <IconButton
                    onClick={() => handleDisconnectAccount(account.id)}
                    color="error"
                    title="Disconnect account"
                  >
                    <DeleteIcon />
                  </IconButton>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Media Dialog */}
      <Dialog
        open={mediaDialogOpen}
        onClose={() => setMediaDialogOpen(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          Instagram Media
          <IconButton
            onClick={() => setMediaDialogOpen(false)}
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          {loadingMedia ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : selectedMedia.length === 0 ? (
            <Typography>No media found</Typography>
          ) : (
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Type</TableCell>
                    <TableCell>Caption</TableCell>
                    <TableCell>Likes</TableCell>
                    <TableCell>Comments</TableCell>
                    <TableCell>Date</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {selectedMedia.map((media) => (
                    <TableRow key={media.id}>
                      <TableCell>
                        <Chip label={media.media_type} size="small" />
                      </TableCell>
                      <TableCell>
                        {media.caption ? (
                          <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                            {media.caption}
                          </Typography>
                        ) : (
                          <Typography variant="body2" color="text.secondary">
                            No caption
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell>{media.like_count || 0}</TableCell>
                      <TableCell>{media.comments_count || 0}</TableCell>
                      <TableCell>{formatDate(media.timestamp)}</TableCell>
                      <TableCell>
                        {media.permalink && (
                          <Button
                            size="small"
                            href={media.permalink}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            View on Instagram
                          </Button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setMediaDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Instagram; 