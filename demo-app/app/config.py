"""Konfigurasi demo-app multi-tenant."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class PengaturanDemo(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    demo_app_port: int = 8081
    # Kosong atau memory:// = tanpa Atlas; isi MONGODB_URI dari root .env untuk data sungguhan.
    mongodb_uri: str = "memory://local"
    mongodb_database: str = "tessera_demo"


pengaturan_demo = PengaturanDemo()
