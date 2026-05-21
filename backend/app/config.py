"""
Konfigurasi aplikasi Tessera.

Module ini mengelola semua environment variables dan settings
yang dibutuhkan oleh aplikasi.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Nilai pembacaan lingkungan operasi Tessera."""

    # Abaikan variabel frontend (NEXT_PUBLIC_*) bila .env root disalin ke backend/.
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

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
    enable_gemini_analysis: bool = False
    enable_gemini_json_terstruktur: bool = True
    gemini_model_name: str = "gemini-2.0-flash"
    gemini_sampling_suhu: float = 0.18
    gemini_token_maks_keluaran_terstruktur: int = 2048
    debug_mode: bool = False


# Instance global settings
settings = Settings()
