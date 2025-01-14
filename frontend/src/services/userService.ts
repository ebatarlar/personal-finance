import { getApiUrl } from '@/config/api';
import { authService } from './authService';

interface User {
  id?: string;
  email: string;
  name: string;
  surname: string;
  password?: string;
  is_active?: boolean;
  is_verified?: boolean;
  oauth_info?: OAuthInfo;
}

interface OAuthInfo { 
  provider: 'github' | 'google';
  provider_user_id: string;
}


export const userService = {
  async register(userData: User) {
    const response = await fetch(getApiUrl('/api/auth/register'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      throw new Error('Registration failed');
    }

    return response.json();
  },

  async getCurrentUser(): Promise<User | null> {
    const token = await authService.getAccessToken();
    if (!token) return null;

    try {
      const response = await fetch(getApiUrl('/api/users/me'), {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) return null;
      return response.json();
    } catch (error) {
      console.error('Error fetching current user:', error);
      return null;
    }
  },

  async oauthLogin(userData: User, oauthInfo: OAuthInfo) {
    const response = await fetch(getApiUrl('/api/auth/oauth'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        oauth_info: oauthInfo,
        user_data: userData
      }),
    });

    if (!response.ok) {
      throw new Error('OAuth login failed');
    }

    return response.json();
  },

  async getUserByEmail(email: string) {
    try {
      const response = await fetch(getApiUrl(`/api/users/email/${email}`));

      if (!response.ok) {
        if (response.status === 404) {
          return null;
        }
        throw new Error('Failed to fetch user');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching user:', error);
      throw error;
    }
  }
};
