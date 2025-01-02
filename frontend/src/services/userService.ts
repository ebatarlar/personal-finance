interface User {
  email: string;
  name: string;
  surname: string;
  password?: string;
  oauth_info?: {
    provider?: string;
    provider_user_id?: string
  }
}

interface OauthInfo { 
  provider: string;
  provider_user_id: string;
}

export const userService = {
  async createOrUpdateUser(userData: User) {
    try {
      const response = await fetch('http://localhost:8000/api/users/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        throw new Error('Failed to create/update user');
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating/updating user:', error);
      throw error;
    }
  },

  async loginByOAuth(userData: User , oauthInfo: OauthInfo) {
    const requestBody = { oauth_info: oauthInfo , user_data:userData,  };
    console.log('loginByOAuth request body:', requestBody);

    try {
      const response = await fetch('http://localhost:8000/api/users/oauth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error('Failed to login by OAuth');
      }

      return await response.json();
    } catch (error) {
      console.error('Error logging in by OAuth:', error);
      throw error;
    }

  },

  async getUserByEmail(email: string) {
    try {
      const response = await fetch(`http://localhost:8000/api/users/email/${email}`);
      
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
  },
};
