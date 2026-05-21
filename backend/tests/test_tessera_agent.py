"""Tes unit ringkas bagi TesseraAgent."""

import asyncio

from app.agent.tessera_agent import QUERY_CONTOH_STANDAR, TesseraAgent
from app.config import settings


def test_agent_batch_memakai_contoh_standar_tertangkap_tidak_kosong():
    ag_pemeriksa_ini = TesseraAgent(
        settings.google_cloud_project,
        settings.vertex_ai_location,
        settings.gemini_model_name,
    )
    hasil_makro_tersebet = asyncio.run(
        ag_pemeriksa_ini.mulai_audit("db_simbol_tersebet", daftar_queries_kustom=None)
    )
    assert QUERY_CONTOH_STANDAR[0]["collection"] == "orders"
    assert hasil_makro_tersebet["jumlah_query_diuji"] == len(QUERY_CONTOH_STANDAR)
    assert len(hasil_makro_tersebet["violations_terdeteksi"]) >= 1
