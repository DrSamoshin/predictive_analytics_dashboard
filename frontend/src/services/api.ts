/**
 * API service for backend communication
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface User {
  id: number;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface LoginRequest {
  login: string;  // Can be either email or username
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface InstagramAccount {
  id: number;
  instagram_user_id: string;
  username: string;
  account_type: string;
  media_count?: number;
  followers_count?: number;
  follows_count?: number;
  access_token: string;
  token_expires_at?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface InstagramMedia {
  id: number;
  instagram_media_id: string;
  media_type: string;
  media_url?: string;
  permalink?: string;
  caption?: string;
  timestamp: string;
  like_count?: number;
  comments_count?: number;
  created_at: string;
}

class ApiService {
  private getHeaders(includeAuth = false): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (includeAuth) {
      const token = localStorage.getItem('access_token');
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    return headers;
  }

  async register(data: RegisterRequest): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }

    return response.json();
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    const authData = await response.json();
    
    // Store token in localStorage
    localStorage.setItem('access_token', authData.access_token);
    
    return authData;
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: this.getHeaders(true),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get user info');
    }

    return response.json();
  }

  logout(): void {
    localStorage.removeItem('access_token');
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  // Instagram API methods
  async getInstagramAuthUrl(): Promise<{ auth_url: string }> {
    const response = await fetch(`${API_BASE_URL}/instagram/auth/url`, {
      headers: this.getHeaders(true),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get Instagram auth URL');
    }

    return response.json();
  }

  async handleInstagramCallback(code: string, state: string): Promise<InstagramAccount> {
    const response = await fetch(`${API_BASE_URL}/instagram/auth/callback`, {
      method: 'POST',
      headers: this.getHeaders(true),
      body: JSON.stringify({ code, state }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to connect Instagram account');
    }

    return response.json();
  }

  async getInstagramAccounts(): Promise<InstagramAccount[]> {
    const response = await fetch(`${API_BASE_URL}/instagram/accounts`, {
      headers: this.getHeaders(true),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get Instagram accounts');
    }

    return response.json();
  }

  async syncInstagramAccount(accountId: number): Promise<{ message: string; synced_media_count: number }> {
    const response = await fetch(`${API_BASE_URL}/instagram/accounts/${accountId}/sync`, {
      method: 'POST',
      headers: this.getHeaders(true),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to sync Instagram account');
    }

    return response.json();
  }

  async getInstagramMedia(accountId: number): Promise<InstagramMedia[]> {
    const response = await fetch(`${API_BASE_URL}/instagram/accounts/${accountId}/media`, {
      headers: this.getHeaders(true),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get Instagram media');
    }

    return response.json();
  }

  async disconnectInstagramAccount(accountId: number): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/instagram/accounts/${accountId}`, {
      method: 'DELETE',
      headers: this.getHeaders(true),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to disconnect Instagram account');
    }

    return response.json();
  }
}

export const apiService = new ApiService(); 