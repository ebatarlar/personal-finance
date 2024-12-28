interface Category {
    type: 'expense' | 'income';
    name: string;
    is_default: boolean;
}

interface CreateCategoryData {
    type: 'expense' | 'income';
    name: string;
}

export const categoryService = {
    async getDefaultCategories() {
        try {
            const response = await fetch('http://localhost:8000/api/categories/default');
            if (!response.ok) {
                throw new Error('Failed to fetch default categories');
            }
            return await response.json() as Category[];
        } catch (error) {
            console.error('Error fetching default categories:', error);
            throw error;
        }
    },

    async getCustomCategories(userId: string) {
        try {
            const response = await fetch(`http://localhost:8000/api/categories/custom/${userId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch custom categories');
            }
            return await response.json() as Category[];
        } catch (error) {
            console.error('Error fetching custom categories:', error);
            throw error;
        }
    },

    async getAllCategories(userId: string) {
        try {
            const response = await fetch(`http://localhost:8000/api/categories/${userId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch categories');
            }
            return await response.json() as Category[];
        } catch (error) {
            console.error('Error fetching categories:', error);
            throw error;
        }
    },

    async createCustomCategory(userId: string, categoryData: CreateCategoryData) {
        try {
            const response = await fetch(`http://localhost:8000/api/categories/custom/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(categoryData),
            });
            if (!response.ok) {
                throw new Error('Failed to create custom category');
            }
            return await response.json() as Category;
        } catch (error) {
            console.error('Error creating custom category:', error);
            throw error;
        }
    },

    async deleteCustomCategory(userId: string, categoryName: string) {
        try {
            const response = await fetch(`http://localhost:8000/api/categories/custom/${userId}/${categoryName}`, {
                method: 'DELETE',
            });
            if (!response.ok) {
                throw new Error('Failed to delete custom category');
            }
            return await response.json();
        } catch (error) {
            console.error('Error deleting custom category:', error);
            throw error;
        }
    }
}
