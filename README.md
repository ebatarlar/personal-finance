# Personal Finance App

A comprehensive full-stack application designed to help users manage their personal finances effectively. Built with Next.js for the frontend and Python for the backend, the app offers a seamless experience for tracking expenses, managing income, and planning budgets.

## Project Structure

This project is organized into two main parts: the backend and the frontend.

### Backend

The backend directory contains the server-side code and services for the application. The key components include:
- `.env`: Environment variables for the backend.
- `app/`: Contains the main application logic.
  - `core/`: Core functionalities and utilities.
    - `database.py`: Database connection and configuration.
  - `models/`: Database models.
    - `user.py`: User data model.
    - `transaction.py`: Transaction data model.
    - `category.py`: Category data model.
  - `routes/`: Defines the API routes for handling requests.
    - `user_routes.py`: Handles user-related API requests.
    - `transaction_routes.py`: Handles transaction-related API requests.
    - `category_routes.py`: Handles category-related API requests.
  - `schemas/`: Data validation schemas.
    - `category.py`: Category data validation schemas.
  - `services/`: Contains business logic and services used by the routes.
    - `user_service.py`: Logic related to user operations.
    - `transaction_service.py`: Logic related to transaction operations.
    - `category_service.py`: Logic related to category operations.
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
│   │   └── database.py
│   ├── models/
│   │   ├── __pycache__/
│   │   ├── category.py
│   │   ├── transaction.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __pycache__/
│   │   ├── category_routes.py
│   │   ├── transaction_routes.py
│   │   └── user_routes.py
│   ├── schemas/
│   └── services/
│       ├── __pycache__/
│       ├── category_service.py
│       ├── transaction_service.py
│       └── user_service.py
├── main.py
├── requirements.txt
├── test_db_connection.py
└── venv/
```

### Frontend

The frontend directory contains the client-side code for the application. The key components include:
- `.env.local`: Local environment variables for the frontend.
- `.eslintrc.json`: ESLint configuration.
- `.next/`: Next.js build output.
- `auth.ts`: Authentication logic.
- `components.json`: Component configurations.
- `next-env.d.ts`: TypeScript environment declarations.
- `next.config.ts`: Next.js configuration.
- `node_modules/`: Installed Node.js modules.
- `public/`: Static files.
- `src/`: Contains the source code for the frontend application.
  - `app/`: Main application components.
  - `components/`: Reusable UI components.
  - `hooks/`: Custom React hooks.
  - `lib/`: Utility functions.
  - `services/`: Services for handling API requests and business logic.
    - `userService.ts`: Service for interacting with user-related API endpoints.
    - `transactionService.ts`: Service for interacting with transaction-related API endpoints.
    - `categoryService.ts`: Service for interacting with category-related API endpoints.
  - `types/`: TypeScript type definitions.
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
│   └── services/
│       ├── userService.ts
│       ├── transactionService.ts
│       └── categoryService.ts
└── types/
    └── next-auth.d.ts
```


## Features

- **User Authentication**: Secure login and registration system.
- **Expense Tracking**: Monitor and categorize your expenses.
- **Income Management**: Keep track of various income sources.
- **Financial Analytics**: Visualize financial data with charts and graphs.
- **Budget Planning**: Create and manage budgets to meet financial goals.

## Technologies Used

- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI
- **Database**: MongoDB


## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ebatarlar/personal-finance.git
   cd personal-finance-app
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Install Backend Dependencies**
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Backend**
   ```bash
   python main.py
   ```

2. **Start the Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

## Usage

- Access the application at `http://localhost:3000`.
- Explore the features through the intuitive user interface.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
