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
                    await signOut({ redirect: true, callbackUrl: '/' });
                    return null;
                }
                const tokens = await authService.refreshAccessToken(refreshToken);
                if (!tokens) {
                    await signOut({ redirect: true, callbackUrl: '/' });
                    return null;
                }
                accessToken = tokens.access_token;
            }

            const response = await fetch(getApiUrl(`/api/transactions/user/${userId}`), {
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                if (response.status === 401) {
                    await signOut({ redirect: true, callbackUrl: '/' });
                    return null;
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
                    await signOut({ redirect: true, callbackUrl: '/' });
                    return null;
                }
                const tokens = await authService.refreshAccessToken(refreshToken);
                if (!tokens) {
                    await signOut({ redirect: true, callbackUrl: '/' });
                    return null;
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
                    await signOut({ redirect: true, callbackUrl: '/' });
                    return null;
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