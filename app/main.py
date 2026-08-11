import os

import psycopg2
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="DevOps Challenge API")


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "devopsdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        connect_timeout=3,
    )


@app.get("/")
def root():
    return {
        "application": "DevOps Challenge API",
        "status": "running",
    }


@app.get("/health/")
def health():
    try:
        connection = get_db_connection()
        connection.close()

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
            },
        )