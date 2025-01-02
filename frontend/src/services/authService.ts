import { getSession } from 'next-auth/react';
import { auth } from '@/auth';

interface Token {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export const authService = {
    async getAccessToken(): Promise<string | null> {
        // Check if we're on the server
        if (typeof window === 'undefined') {
            const session = await auth();
            return session?.tokens?.access_token || null;
        }
        // Client-side
        const session = await getSession();
        return session?.tokens?.access_token || null;
    },

    async getRefreshToken(): Promise<string | null> {
        // Check if we're on the server
        if (typeof window === 'undefined') {
            const session = await auth();
            return session?.tokens?.refresh_token || null;
        }
        // Client-side
        const session = await getSession();
        return session?.tokens?.refresh_token || null;
    },

    async refreshAccessToken(): Promise<boolean> {
        const refreshToken = await this.getRefreshToken();
        if (!refreshToken) return false;

        try {
            const response = await fetch('http://localhost:8000/api/users/refresh', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh_token: refreshToken }),
            });

            if (!response.ok) {
                return false;
            }

            const tokens: Token = await response.json();
            
            // Instead of setting cookies, we'll update the NextAuth session
            // The tokens will be automatically updated in the session through the jwt callback
            return true;
        } catch (error) {
            console.error('Error refreshing token:', error);
            return false;
        }
    }
};
