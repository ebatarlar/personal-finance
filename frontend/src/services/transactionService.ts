import { authService } from './authService';
import { getApiUrl } from '@/config/api';
import { signOut } from 'next-auth/react';

export const transactionService = {
    async getTransactions(userId: string) {
        try {
            let accessToken = await authService.getAccessToken();
            
            if (!accessToken) {
                const refreshToken = await authService.getRefreshToken();
                if (!refreshToken) {
                    throw new Error('No tokens available. Please log in again.');
                }
                const tokens = await authService.refreshAccessToken(refreshToken);
                if (!tokens) {
                    throw new Error('Failed to refresh token. Please log in again.');
                }
                accessToken = tokens.access_token;
            }

            const response = await fetch(getApiUrl(`/api/transactions/user/${userId}`), {
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
            });

            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Session expired. Please log in again.');
                }
                throw new Error('Failed to fetch transactions');
            }

            return response.json();
        } catch (error) {
            console.error('Error fetching transactions:', error);
            throw error;
        }
    },

    async createTransaction(transactionData: any) {
        try {
            let accessToken = await authService.getAccessToken();
            if (!accessToken) {
                const refreshToken = await authService.getRefreshToken();
                if (!refreshToken) {
                    throw new Error('No tokens available. Please log in again.');
                }
                const tokens = await authService.refreshAccessToken(refreshToken);
                if (!tokens) {
                    throw new Error('Failed to refresh token. Please log in again.');
                }
                accessToken = tokens.access_token;
            }

            const response = await fetch(getApiUrl('/api/transactions/create'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`,
                },
                body: JSON.stringify(transactionData),
            });

            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Session expired. Please log in again.');
                }
                throw new Error('Failed to create transaction');
            }

            return response.json();
        } catch (error) {
            console.error('Error creating transaction:', error);
            throw error;
        }
    }
};