# Personal Finance App API Documentation

## Authentication

All protected endpoints require a valid JWT token in the Authorization header. Here's how to obtain and use tokens:

### 1. Obtaining Tokens

#### Regular Login
```http
POST /api/users/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=your_password
```

Note: The login endpoint uses OAuth2's password flow, which expects:
- Email in the `username` field
- Form URL-encoded format instead of JSON
- `application/x-www-form-urlencoded` content type

Response:
```json
{
    "access_token": "eyJ0...",
    "refresh_token": "eyJ0...",
    "token_type": "bearer"
}
```

#### OAuth Login
```http
POST /users/oauth
Content-Type: application/json

{
    "oauth_info": {
        "provider": "google",
        "provider_user_id": "123456789"
    },
    "user_data": {
        "email": "user@example.com",
        "name": "John Doe"
    }
}
```

### 2. Using Tokens

Include the access token in the Authorization header for all protected requests:
```http
Authorization: Bearer eyJ0...
```

### 3. Refreshing Tokens

When the access token expires (after 15 minutes), use the refresh token to get a new pair of tokens:
```http
POST /token/refresh
Content-Type: application/json

{
    "refresh_token": "eyJ0..."
}
```

## Protected Endpoints

### Transactions

#### Create Transaction
```http
POST /transactions/create
Authorization: Bearer eyJ0...
Content-Type: application/json

{
    "amount": 50.00,
    "category": "Groceries",
    "description": "Weekly groceries",
    "date": "2024-12-31T00:00:00Z"
}
```

#### Get User Transactions
```http
GET /transactions/user/{user_id}
Authorization: Bearer eyJ0...
```
Note: You can only access your own transactions. The user_id must match the authenticated user's ID.

### Categories

#### Get Default Categories (Public)
```http
GET /categories/default
```

#### Get Custom Categories
```http
GET /categories/custom/{user_id}
Authorization: Bearer eyJ0...
```

#### Get All Categories
```http
GET /categories/{user_id}
Authorization: Bearer eyJ0...
```

#### Create Custom Category
```http
POST /categories/custom/{user_id}
Authorization: Bearer eyJ0...
Content-Type: application/json

{
    "name": "Entertainment",
    "type": "expense",
    "color": "#FF5733"
}
```

#### Delete Custom Category
```http
DELETE /categories/custom/{user_id}/{category_name}
Authorization: Bearer eyJ0...
```

## Error Responses

### Authentication Errors

#### Unauthorized (401)
Returned when no token or an invalid token is provided:
```json
{
    "detail": "Could not validate credentials",
    "headers": {
        "WWW-Authenticate": "Bearer"
    }
}
```

#### Forbidden (403)
Returned when trying to access another user's data:
```json
{
    "detail": "Cannot access another user's [resource]"
}
```

### Other Common Errors

#### Bad Request (400)
```json
{
    "detail": "Invalid request data"
}
```

#### Server Error (500)
```json
{
    "detail": "Error message describing the issue"
}
```

## Best Practices

1. **Token Storage**: 
   - Store tokens securely (e.g., in HttpOnly cookies or secure local storage)
   - Never expose tokens in URLs or log them

2. **Token Refresh**:
   - Implement token refresh before the access token expires
   - Store both access and refresh tokens securely
   - Refresh the access token when you get a 401 response

3. **Error Handling**:
   - Always handle authentication errors gracefully
   - Redirect to login page when receiving 401 errors
   - Show appropriate error messages to users

4. **Security**:
   - Always use HTTPS in production
   - Never send tokens or credentials in URL parameters
   - Validate all input data before sending to the API

## Example Usage (JavaScript/Fetch)

```javascript
// Login
async function login(email, password) {
    const response = await fetch('/api/users/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${email}&password=${password}`
    });
    const tokens = await response.json();
    return tokens;
}

// Making authenticated requests
async function createTransaction(transactionData) {
    const response = await fetch('/transactions/create', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(transactionData)
    });
    return await response.json();
}

// Refreshing tokens
async function refreshTokens(refreshToken) {
    const response = await fetch('/token/refresh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_token: refreshToken })
    });
    return await response.json();
}
```

## Rate Limiting and Security

- API requests are subject to rate limiting
- Multiple failed authentication attempts may result in temporary blocking
- Access tokens expire after 15 minutes
- Refresh tokens expire after 7 days
- Always validate user input and handle errors appropriately
