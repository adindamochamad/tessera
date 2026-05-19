"""
Konfigurasi aplikasi Tessera.

Module ini mengelola semua environment variables dan settings
yang dibutuhkan oleh aplikasi.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Settings aplikasi dari environment variables."""
    
    # Google Cloud Configuration
    google_cloud_project: str
    google_application_credentials: str
    vertex_ai_location: str = "us-central1"
    
    # MongoDB Configuration  
    mongodb_uri: str
    mongodb_database: str
    mongodb_vector_search_index: str = "violations_index"
    
    # MCP Server Configuration
    mcp_server_url: str = "http://localhost:3000"
    mcp_server_port: int = 3000
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Security
    jwt_secret: str
    api_key: Optional[str] = None
    
    # Feature Flags
    enable_vector_search: bool = True
    enable_auto_remediation: bool = False
    debug_mode: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instance global settings
settings = Settings()
