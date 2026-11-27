from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials

from schemas import AuthRequest
from auth import signup_user, login_user
from supabase_client import supabase
from dependencies import get_current_user, bearer_scheme


app = FastAPI(
    title="Auth Login & Protect API",
    description="""
    ## Authentication API

    A secure REST API built using FastAPI and Supabase Auth.

    ### Features
    - User registration
    - User login
    - JWT access and refresh tokens
    - User logout
    - Public endpoints
    - JWT-protected endpoints

    ### Authentication
    Protected endpoints require a valid Supabase access token.

    Click **Authorize** and enter your access token to test them.
    """,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User signup, login and logout operations."
        },
        {
            "name": "Public",
            "description": "Endpoints accessible without authentication."
        },
        {
            "name": "Protected",
            "description": "Endpoints requiring a valid JWT access token."
        }
    ]
)


@app.get("/")
def home():
    return {"message": "Auth Login & Protect API is running"}


@app.get("/health")
def health():
    return {"status": "healthy", "supabase": "client initialized"}


@app.post("/auth/signup", status_code=201, tags=["Authentication"], summary="Register a new user")
def signup(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = signup_user(data.email, data.password)

        return {
            "message": "User registered successfully",
            "user_id": response.user.id if response.user else None,
            "email": response.user.email if response.user else data.email
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Signup failed. Check your input or whether the email is already registered."
        )


@app.post("/auth/login", tags=["Authentication"], summary="Login and obtain JWT tokens")
def login(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = login_user(data.email, data.password)

        if not response.session:
            raise HTTPException(
                status_code=401,
                detail="Login failed. Please verify your email if confirmation is enabled."
            )

        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


@app.post("/auth/logout", status_code=204, tags=["Authentication"], summary="Logout the authenticated user")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user=Depends(get_current_user)
):
    token = credentials.credentials

    try:
        supabase.auth.admin.sign_out(token, "local")
        return

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Logout failed"
        )


@app.get("/public/info", tags=["Public"], summary="Get public information")
def public_info():
    return {
        "message": "This is a public endpoint",
        "access": "Anyone can access this route"
    }


@app.get("/protected/profile", tags=["Protected"], summary="Get authenticated user profile")
def protected_profile(current_user=Depends(get_current_user)):
    return {
        "message": "Authentication successful",
        "user_id": current_user.id,
        "email": current_user.email,
        "authenticated": True
    }


@app.get("/protected/dashboard", tags=["Protected"], summary="Access protected dashboard")
def protected_dashboard(current_user=Depends(get_current_user)):
    return {
        "message": "Welcome to your protected dashboard",
        "user_id": current_user.id,
        "email": current_user.email,
        "access": "Authorized user only"
    }