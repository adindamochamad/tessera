"""
Tessera API - Main FastAPI Application

Entry point untuk backend API Tessera.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from app.config import settings

# Setup logging
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager untuk startup dan shutdown events."""
    # Startup
    logger.info(
        "tessera_startup",
        project=settings.google_cloud_project,
        database=settings.mongodb_database
    )
    yield
    # Shutdown
    logger.info("tessera_shutdown")


# Inisialisasi FastAPI app
app = FastAPI(
    title="Tessera API",
    description="AI-Powered Multi-Tenant Data Isolation Auditor",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware untuk frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development
        "https://tessera.dev",     # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Tessera API",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check dengan status dependencies."""
    return {
        "status": "healthy",
        "checks": {
            "api": "up",
            "mongodb": "pending",
            "gemini": (
                "flag_on_pending_runtime_proof"
                if settings.enable_gemini_analysis
                else "offline_disabled"
            ),
            "mcp_server": "pending",
        }
    }


@app.get("/api/v1/info")
async def get_info():
    """Informasi sistem dan konfigurasi."""
    return {
        "project": settings.google_cloud_project,
        "database": settings.mongodb_database,
        "features": {
            "vector_search": settings.enable_vector_search,
            "auto_remediation": settings.enable_auto_remediation,
            "gemini_analysis": settings.enable_gemini_analysis,
            "gemini_json_terstruktur": settings.enable_gemini_json_terstruktur,
        },
        "version": "0.1.0"
    }


from app.api import routes_audit

app.include_router(
    routes_audit.router,
    prefix="/api/v1/audit",
    tags=["audit"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
