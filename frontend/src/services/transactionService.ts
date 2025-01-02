import { authService } from './authService';

export const transactionService = {
    async getTransactions(userId: string) {
        try {
            const accessToken = await authService.getAccessToken();
            if (!accessToken) {
                throw new Error('No access token available');
            }

            const response = await fetch(`http://localhost:8000/api/transactions/user/${userId}`, {
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
            });

            if (response.status === 401) {
                // Token might be expired, try to refresh
                const refreshed = await authService.refreshAccessToken();
                if (refreshed) {
                    // Retry with new token
                    const newToken = await authService.getAccessToken();
                    const retryResponse = await fetch(`http://localhost:8000/api/transactions/user/${userId}`, {
                        headers: {
                            'Authorization': `Bearer ${newToken}`,
                        },
                    });
                    if (!retryResponse.ok) {
                        throw new Error('Failed to fetch transactions after token refresh');
                    }
                    return await retryResponse.json();
                }
                throw new Error('Failed to refresh token');
            }

            if (!response.ok) {
                throw new Error('Failed to fetch transactions');
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching transactions:', error);
            throw error;
        }
    },

    async createTransaction(transactionData: any) {
        try {
            const accessToken = await authService.getAccessToken();
            if (!accessToken) {
                throw new Error('No access token available');
            }

            const response = await fetch('http://localhost:8000/api/transactions/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`,
                },
                body: JSON.stringify(transactionData),
            });

            if (response.status === 401) {
                // Token might be expired, try to refresh
                const refreshed = await authService.refreshAccessToken();
                if (refreshed) {
                    // Retry with new token
                    const newToken = await authService.getAccessToken();
                    const retryResponse = await fetch('http://localhost:8000/api/transactions', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${newToken}`,
                        },
                        body: JSON.stringify(transactionData),
                    });
                    if (!retryResponse.ok) {
                        throw new Error('Failed to create transaction after token refresh');
                    }
                    return await retryResponse.json();
                }
                throw new Error('Failed to refresh token');
            }

            if (!response.ok) {
                throw new Error('Failed to create transaction');
            }

            return await response.json();
        } catch (error) {
            console.error('Error creating transaction:', error);
            throw error;
        }
    }
};