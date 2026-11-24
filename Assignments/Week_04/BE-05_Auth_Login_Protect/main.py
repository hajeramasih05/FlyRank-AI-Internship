from fastapi import FastAPI
from fastapi import HTTPException
from schemas import AuthRequest
from auth import signup_user, login_user
from supabase_client import supabase

app = FastAPI(
    title="Auth Login & Protect",
    description="Secure authentication API using FastAPI and Supabase.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Auth Login & Protect API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "supabase": "client initialized"
    }

@app.post("/auth/signup", status_code=201)
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


@app.post("/auth/login")
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