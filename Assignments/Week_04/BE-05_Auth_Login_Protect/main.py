from fastapi import FastAPI

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