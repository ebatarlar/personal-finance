import { getSession } from 'next-auth/react';
import { auth } from '@/auth';
import { getApiUrl } from '@/config/api';

interface Token {
    access_token: string;
    refresh_token: string;
    token_type: string;
    expires_at?: number;
}

interface LoginCredentials {
    email: string;
    password: string;
}

interface PasswordResetRequest {
    email: string;
}

interface PasswordReset {
    token: string;
    new_password: string;
}

export const authService = {
    async getAccessToken(): Promise<string | null> {
        if (typeof window === 'undefined') {
            const session = await auth();
            return session?.tokens?.access_token || null;
        }
        const session = await getSession();
        return session?.tokens?.access_token || null;
    },

    async getRefreshToken(): Promise<string | null> {
        if (typeof window === 'undefined') {
            const session = await auth();
            return session?.tokens?.refresh_token || null;
        }
        const session = await getSession();
        return session?.tokens?.refresh_token || null;
    },

    async login(credentials: LoginCredentials): Promise<Token> {
        const response = await fetch(getApiUrl('/api/auth/login'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        return response.json();
    },

    async refreshAccessToken(refreshToken: string): Promise<Token | null> {
        if (!refreshToken) return null;

        try {
            const response = await fetch(getApiUrl('/api/auth/refresh-token'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refreshToken }),
            });

            if (!response.ok) {
                console.error('Token refresh failed:', response.status);
                return null;
            }

            return response.json();
        } catch (error) {
            console.error('Error refreshing token:', error);
            return null;
        }
    },

    async logout(token: string): Promise<boolean> {
        try {
            const response = await fetch(getApiUrl('/api/auth/logout'), {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            return response.ok;
        } catch (error) {
            console.error('Error during logout:', error);
            return false;
        }
    },

    async requestPasswordReset(data: PasswordResetRequest): Promise<boolean> {
        const response = await fetch(getApiUrl('/api/auth/forgot-password'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        return response.ok;
    },

    async resetPassword(data: PasswordReset): Promise<boolean> {
        const response = await fetch(getApiUrl('/api/auth/reset-password'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        return response.ok;
    },

    async verifyEmail(token: string): Promise<boolean> {
        const response = await fetch(getApiUrl('/api/auth/verify-email'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token }),
        });

        return response.ok;
    }
};
