export const transactionService = {
    async getTransactions(userId: string) {
        try {
            const response = await fetch(`http://localhost:8000/api/transactions/user/${userId}`);
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
            const response = await fetch('http://localhost:8000/api/transactions/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(transactionData),
            });
            if (!response.ok) {
                throw new Error('Failed to create transaction');
            }
            return await response.json();
        } catch (error) {
            console.error('Error creating transaction:', error);
            throw error;
        }
    }
}