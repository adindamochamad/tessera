"""
Endpoint pemeriksaan audit — Day 2 (alur aturan + agent).
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agent.tessera_agent import TesseraAgent
from app.config import settings

router = APIRouter()


class IsiAwalAuditHttp(BaseModel):
    nama_database: str = Field(..., description="Basis data Mongo sasaran logis Anda")
    queries: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Daftar struktur-serial query Anda; boleh None memakai contoh Tessera.",
    )


def pembangunan_agent_dari_penampungan() -> TesseraAgent:
    return TesseraAgent(
        settings.google_cloud_project,
        settings.vertex_ai_location,
        settings.gemini_model_name,
    )


@router.post("/start")
async def jalankan_audit_mulai_untuk_http(isinya: IsiAwalAuditHttp):
    agent_pemeriksaan = pembangunan_agent_dari_penampungan()
    return await agent_pemeriksaan.mulai_audit(
        isinya.nama_database,
        daftar_queries_kustom=isinya.queries,
    )
