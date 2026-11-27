# Auth Login & Protect API

A secure authentication REST API built using **Python, FastAPI and Supabase Auth**. This project demonstrates user registration, login, JWT-based authentication, protected routes and logout functionality.

## Features

- User registration using Supabase Auth.
- User login with email and password.
- Access token and refresh token generation.
- JWT access token verification.
- Protected API endpoints.
- Reusable authentication dependency.
- User logout.
- Interactive API documentation using Swagger UI.

## Tech Stack

- Python
- FastAPI
- Supabase Auth
- Supabase Python SDK
- Pydantic
- Uvicorn
- Python-dotenv

## Project Structure

```text
BE-05_Auth_Login_Protect/
│
├── main.py
├── auth.py
├── dependencies.py
├── schemas.py
├── supabase_client.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/hajeramasih05/FlyRank-AI-Internship.git
```

### 2. Navigate to the assignment folder

```bash
cd FlyRank-AI-Internship/Assignments/Week_04/BE-05_Auth_Login_Protect
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project folder:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
PORT=8000
```

Replace the placeholders with your Supabase project credentials.

**Never commit your `.env` file or expose your secret keys.**

### 7. Run the application

```bash
python -m uvicorn main:app --reload
```

The API runs at:

`http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/auth/signup` | Register a new user | No |
| POST | `/auth/login` | Login and obtain tokens | No |
| POST | `/auth/logout` | Logout authenticated user | Yes |
| GET | `/public/info` | Get public information | No |
| GET | `/protected/profile` | Get authenticated user profile | Yes |
| GET | `/protected/dashboard` | Access protected dashboard | Yes |

## Authentication Workflow

1. A user registers through `/auth/signup`.
2. The user logs in through `/auth/login`.
3. Supabase Auth returns an access token and refresh token.
4. The access token is supplied as a Bearer token when accessing protected endpoints.
5. The reusable authentication dependency verifies the token through Supabase.
6. Valid users can access protected resources.
7. The logout endpoint signs out the authenticated session.

## API Documentation

FastAPI provides interactive Swagger documentation.

After starting the server, visit:

`http://127.0.0.1:8000/docs`

Use the **Authorize** button to provide your access token and test protected endpoints.

## Security

- Credentials are stored in environment variables.
- `.env` is excluded from Git tracking.
- Protected routes verify access tokens through Supabase Auth.
- Unauthorized requests receive HTTP 401 responses.

## Author

**Hajera Masih**

FlyRank AI Internship – Backend Engineering Track