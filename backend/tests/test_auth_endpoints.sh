#!/bin/bash

# Base URL for the API
API_URL="http://localhost:8000/api"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Function to print success/failure
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
        echo "Error response: $3"
    fi
}

echo "Testing Auth Endpoints..."
echo "========================"

# Test 1: Register new user
echo -n "Testing /auth/register: "
REGISTER_RESPONSE=$(curl -s -X POST "${API_URL}/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "test@example.com",
        "name": "Test",
        "surname": "User",
        "password": "TestPassword123!"
    }')
print_result $? "Register new user" "$REGISTER_RESPONSE"

# Test 2: Login
echo -n "Testing /auth/login: "
LOGIN_RESPONSE=$(curl -s -X POST "${API_URL}/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test@example.com&password=TestPassword123!")
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
print_result $? "Login" "$LOGIN_RESPONSE"

if [ ! -z "$ACCESS_TOKEN" ]; then
    # Test 3: Get current user (Protected route)
    echo -n "Testing /users/me: "
    ME_RESPONSE=$(curl -s -X GET "${API_URL}/users/me" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")
    print_result $? "Get current user" "$ME_RESPONSE"

    # Test 4: Refresh token
    echo -n "Testing /auth/refresh-token: "
    REFRESH_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"refresh_token":"[^"]*' | cut -d'"' -f4)
    REFRESH_RESPONSE=$(curl -s -X POST "${API_URL}/auth/refresh-token" \
        -H "Content-Type: application/json" \
        -d "{\"refresh_token\": \"${REFRESH_TOKEN}\"}")
    print_result $? "Refresh token" "$REFRESH_RESPONSE"

    # Test 5: Logout
    echo -n "Testing /auth/logout: "
    LOGOUT_RESPONSE=$(curl -s -X POST "${API_URL}/auth/logout" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")
    print_result $? "Logout" "$LOGOUT_RESPONSE"
fi

# Test 6: Password reset flow
echo -n "Testing /auth/forgot-password: "
FORGOT_RESPONSE=$(curl -s -X POST "${API_URL}/auth/forgot-password" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "test@example.com"
    }')
print_result $? "Request password reset" "$FORGOT_RESPONSE"

echo "Test completed!"
