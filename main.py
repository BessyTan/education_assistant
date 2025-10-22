from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="AI-Driven Education Assistant (Supabase Edition)",
    description="Adaptive learning assistant using GPT + Supabase",
    version="2.0.0"
)

app.include_router(router)
