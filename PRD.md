# Personal Finance App - Product Requirements Document

## Overview
The Personal Finance App is a comprehensive web application designed to help users manage their personal finances effectively. This document outlines the product requirements and specifications for development.

## Problem Statement
Many individuals struggle with managing their personal finances effectively, lacking a centralized and user-friendly platform to track expenses, manage income, and plan budgets.

## Target Users
- Individual users seeking to manage personal finances
- Budget-conscious individuals
- Users looking for financial insights and planning tools
- People wanting to track expenses and income

## Core Features

### 1. User Authentication & Authorization
- Secure user registration and login with Argon2 password hashing
- JWT-based authentication with access and refresh tokens
- OAuth support for third-party authentication
- Password recovery and email verification system
- Advanced rate limiting for security:
  - Aggressive limits (3 req/min) for sensitive endpoints (login, register)
  - Normal limits (10 req/min) for authenticated endpoints
  - IP-based rate limiting with detailed response headers
- Session management with token refresh and logout

### 2. Financial Records Management
- Add, edit, and delete financial records
- Categorize transactions
- Attach receipts/documents
- Search and filter functionality
- Transaction history view

### 3. Budget Planning
- Create and manage budgets
- Set spending limits by category
- Budget vs. actual spending analysis
- Alert system for budget overruns

### 4. Dashboard & Analytics
- Overview of financial status
- Income vs. expenses visualization
- Category-wise spending analysis
- Trend analysis and reports
- Customizable widgets

### 5. Income Management
- Multiple income sources tracking
- Regular and one-time income entries
- Income categorization
- Income trends visualization

## Technical Requirements

### Frontend
- **Framework**: Next.js with React
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn UI
- **State Management**: React Context/Hooks
- **Data Fetching**: React Query/SWR

### Backend
- **Framework**: FastAPI
- **Language**: Python
- **Database**: MongoDB
- **API Documentation**: OpenAPI/Swagger
- **Authentication**: JWT
- **Validation**: Pydantic v2

### Security Requirements
- Encrypted data transmission (HTTPS)
- Secure password hashing using Argon2
- JWT-based authentication with refresh tokens
- Advanced rate limiting and brute force protection:
  - IP-based rate limiting
  - Endpoint-specific rate limits
  - Rate limit headers (X-RateLimit-*)
- Input validation and sanitization using Pydantic v2
- CORS configuration
- Security headers implementation

### Performance Requirements
- Page load time < 2 seconds
- API response time < 500ms
- Support for concurrent users
- Efficient data caching
- Optimized database queries
- Lazy loading for large datasets


## Deployment

### Backend (Google Cloud Run)
The backend is deployed on Google Cloud Run, providing a scalable and serverless environment.

- **Production URL**: `https://personal-finance-backend-315388459026.europe-west1.run.app`
- **Deployment Stack**:
  - Python 3.11
  - FastAPI
  - MongoDB
  - Docker

### Frontend (Vercel)
The frontend is deployed on Vercel, offering automatic deployments and serverless functions.

- **Production URL**: `https://frontend-iota-ruby.vercel.app`
- **Deployment Stack**:
  - Next.js 14
  - TypeScript
  - Tailwind CSS
  - shadcn/ui

### Environment Variables

#### Backend (.env)
```
MONGODB_URL=your_mongodb_connection_string
JWT_SECRET_KEY=your_jwt_secret
```

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://personal-finance-backend-315388459026.europe-west1.run.app
NEXTAUTH_URL=https://frontend-iota-ruby.vercel.app
AUTH_GITHUB_ID=your_github_oauth_client_id
AUTH_GITHUB_SECRET=your_github_oauth_client_secret
NEXTAUTH_SECRET=your_nextauth_secret
```

## Project Structure

This project is organized into two main parts: the backend and the frontend.

### Backend

The backend directory contains the server-side code and services for the application. The key components include:
- `.env`: Environment variables for the backend.
  - `MONGODB_URL`: MongoDB connection string
  - `JWT_SECRET_KEY`: Secret key for JWT token generation
- `app/`: Contains the main application logic.
  - `core/`: Core functionalities and utilities.
    - `database.py`: Database connection and configuration.
    - `security.py`: JWT token generation and password hashing.
    - `rate_limit.py`: Rate limiting and brute force protection.
  - `models/`: Database models.
    - `user.py`: User data model and Pydantic schemas.
    - `transaction.py`: Transaction data model and schemas.
    - `category.py`: Category data model and schemas.
    
  - `routes/`: Defines the API routes for handling requests.
    - `auth_routes.py`: Authentication and authorization endpoints.
    - `user_routes.py`: User profile and management endpoints.
    - `transaction_routes.py`: Transaction-related endpoints.
    - `category_routes.py`: Category management endpoints.
  - `services/`: Contains business logic and services.
    - `auth_service.py`: Authentication and authorization logic.
    - `user_service.py`: User management operations.
    - `transaction_service.py`: Transaction operations.
    - `category_service.py`: Category operations.
- `main.py`: The entry point for the backend application.
- `requirements.txt`: Python dependencies.
- `test_db_connection.py`: Script to test database connections.
- `venv/`: Virtual environment for Python dependencies.

## Backend Directory Structure

```
backend/
├── .env
├── __pycache__/
├── app/
│   ├── core/
│   │   ├── __pycache__/
│   │   ├── database.py
│   │   ├── security.py
│   │   └── rate_limit.py
│   ├── models/
│   │   ├── __pycache__/
│   │   ├── category.py
│   │   ├── transaction.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __pycache__/
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── category_routes.py
│   │   └── transaction_routes.py
│   ├── services/
│   │   ├── __pycache__/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── category_service.py
│   │   ├── transaction_service.py
├── main.py
├── requirements.txt
├── test_db_connection.py
└── venv/
```

### Frontend

The frontend directory contains the client-side code for the application built with Next.js, TypeScript, and Tailwind CSS, using shadcn/ui for components. The key components include:
- `.env.local`: Local environment variables for the frontend.
- `.eslintrc.json`: ESLint configuration.
- `.next/`: Next.js build output.
- `auth.ts`: Authentication logic using NextAuth.js.
- `components.json`: shadcn/ui component configurations.
- `next-env.d.ts`: TypeScript environment declarations.
- `next.config.ts`: Next.js configuration.
- `node_modules/`: Installed Node.js modules.
- `public/`: Static files.
- `src/`: Contains the source code for the frontend application.
  - `app/`: Main application components and routing.
  - `components/`: Reusable UI components.
    - `AddTransDialog.tsx`: Transaction creation dialog.
    - `app-sidebar.tsx`: Application sidebar navigation.
    - `login/`: Authentication-related components.
    - `providers.tsx`: React context providers.
    - `ui/`: shadcn/ui components (button, dialog, form, etc.).
  - `hooks/`: Custom React hooks.
    - `use-mobile.tsx`: Mobile device detection hook.
    - `use-toast.ts`: Toast notification hook.
  - `lib/`: Utility functions.
    - `utils.ts`: Common utility functions.
  - `services/`: Services for handling API requests.
    - `userService.ts`: User authentication and management.
    - `transactionService.ts`: Transaction operations.
    - `categoryService.ts`: Category management.
    - `authService.ts`: Authentication utilities.
  - `types/`: TypeScript type definitions.
    - `next-auth.d.ts`: NextAuth type declarations.
- `tailwind.config.ts`: Tailwind CSS configuration.
- `tsconfig.json`: TypeScript configuration.

## Frontend Directory Structure

```
frontend/
├── .env.local
├── .eslintrc.json
├── .gitignore
├── .next/
├── README.md
├── auth.ts
├── components.json
├── next-env.d.ts
├── next.config.ts
├── node_modules/
├── package-lock.json
├── package.json
├── postcss.config.mjs
├── public/
├── src/
│   ├── app/
│   │   ├── api/
│   │   ├── dashboard/
│   │   │   ├── components/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── favicon.ico
│   │   ├── fonts/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── AddTransDialog.tsx
│   │   ├── app-sidebar.tsx
│   │   ├── providers.tsx
│   │   ├── login/
│   │   │   ├── auth-buttons-github.tsx
│   │   │   └── login-form.tsx
│   │   └── ui/
│   │       ├── button.tsx
│   │       ├── calendar.tsx
│   │       ├── card.tsx
│   │       ├── dialog.tsx
│   │       ├── dropdown-menu.tsx
│   │       ├── form.tsx
│   │       ├── input.tsx
│   │       ├── label.tsx
│   │       ├── popover.tsx
│   │       ├── select.tsx
│   │       ├── separator.tsx
│   │       ├── sheet.tsx
│   │       ├── sidebar.tsx
│   │       ├── skeleton.tsx
│   │       ├── table.tsx
│   │       ├── toast.tsx
│   │       ├── toaster.tsx
│   │       └── tooltip.tsx
│   ├── hooks/
│   │   ├── use-mobile.tsx
│   │   └── use-toast.ts
│   ├── lib/
│   │   └── utils.ts
│   ├── services/
│   │   ├── authService.ts
│   │   ├── userService.ts
│   │   ├── transactionService.ts
│   │   └── categoryService.ts
│   └── types/
│       └── next-auth.d.ts
└── tailwind.config.ts
```

## Future Enhancements
1. Mobile application development
2. Integration with bank accounts
3. Investment portfolio tracking
4. Bill payment reminders
5. Financial goal setting and tracking
6. Multi-currency support
7. Export functionality for reports
8. Collaborative budget planning

## Success Metrics
- User engagement (DAU/MAU)
- Transaction volume
- Budget adherence rate
- User retention rate
- Feature adoption rate
- System performance metrics
- User satisfaction scores

## Timeline
Phase 1 (MVP):
- Basic user authentication
- Transaction management
- Simple dashboard
- Essential budget features

Phase 2:
- Advanced analytics
- Document attachments
- Enhanced budgeting tools
- Performance optimizations

Phase 3:
- Additional features based on user feedback
- Mobile responsiveness improvements
- Integration capabilities
- Advanced reporting
