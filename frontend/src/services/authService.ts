import { getSession } from 'next-auth/react';
import { auth } from '@/auth';

interface Token {
    access_token: string;
    refresh_token: string;
    token_type: string;
    expires_at?: number;
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

    async refreshAccessToken(refreshToken: string): Promise<Token | null> {
        if (!refreshToken) return null;

        try {
            const response = await fetch('http://localhost:8000/api/token/refresh', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh_token: refreshToken }),
            });

            if (!response.ok) {
                console.error('Token refresh failed:', response.status);
                return null;
            }

            const tokens: Token = await response.json();
            tokens.expires_at = Math.floor(Date.now() / 1000 + 15 * 60); // 15 minutes from now
            return tokens;
        } catch (error) {
            console.error('Error refreshing token:', error);
            return null;
        }
    }
};
