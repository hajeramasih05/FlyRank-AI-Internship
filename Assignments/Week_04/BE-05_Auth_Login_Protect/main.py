from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from schemas import AuthRequest
from auth import signup_user, login_user
from supabase_client import supabase

bearer_scheme = HTTPBearer(auto_error=False)



app = FastAPI(
    title="Auth Login & Protect",
    description="Secure authentication API using FastAPI and Supabase.",
    version="1.0.0",
)


# ---------------- HOME AND HEALTH ----------------

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


# ---------------- SIGNUP ----------------

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


# ---------------- LOGIN ----------------

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


# ---------------- PUBLIC ROUTE ----------------

@app.get("/public/info")
def public_info():
    return {
        "message": "This is a public endpoint",
        "access": "Anyone can access this route"
    }


# ---------------- PROTECTED ROUTE ----------------

@app.get("/protected/profile")
def protected_profile(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)
):
    # Step 1: Check whether the token was supplied
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    # Step 2: Extract the actual JWT
    token = credentials.credentials

    # Step 3: Ask Supabase to verify the token
    try:
        response = supabase.auth.get_user(token)

        user = response.user

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        # Step 4: Return authenticated user information
        return {
            "message": "Authentication successful",
            "user_id": user.id,
            "email": user.email,
            "authenticated": True
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )