from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router


app = FastAPI(
    title="LegalEase API",
    description="AI-Powered Legal Document Generator",
    version="1.0.0"
)


# Allow Streamlit frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Include API routes
app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "LegalEase API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }