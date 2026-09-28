from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="LegalEase",
    description="AI-Powered Legal Document Generator",
    version="1.0"
)

app.include_router(router)


@app.get("/")
def home():

    return {
        "message": "Welcome to LegalEase - AI Powered Legal Document Generator"
    }


@app.get("/health")
def health():

    return {
        "status": "LegalEase is running"
    }
from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="LegalEase",
    description="AI-Powered Legal Document Generator",
    version="1.0"
)

app.include_router(router)


@app.get("/")
def home():

    return {
        "message": "Welcome to LegalEase - AI Powered Legal Document Generator"
    }


@app.get("/health")
def health():

    return {
        "status": "LegalEase is running"
    }
