"""
Tes Day 2: pola query dari demo-app terdeteksi oleh analyzer Tessera.
"""

import asyncio
import sys
from pathlib import Path

import pytest

AKAR_DEMO = Path(__file__).resolve().parents[2] / "demo-app"
if str(AKAR_DEMO) not in sys.path:
    sys.path.insert(0, str(AKAR_DEMO))

from pola_query_audit import (  # noqa: E402
    DAFTAR_POLA_DEMO,
    POLA_ANALYTICS_LINTAS_TENANT,
    POLA_LOOKUP_TANPA_BATAS_TENANT,
    POLA_ORDERS_AMAN_DENGAN_TENANT,
    POLA_ORDERS_TANPA_TENANT,
    POLA_USERS_CAMPURAN_FIELD_TENANT,
)
from app.analyzers.query_analyzer import MongoDBQueryAnalyzer  # noqa: E402


@pytest.fixture
def analyzer():
    return MongoDBQueryAnalyzer()


def test_pola_demo_orders_tanpa_tenant(analyzer):
    hasil = analyzer.analyze(POLA_ORDERS_TANPA_TENANT)
    assert "missing_tenant_filter" in hasil.pattern_violations


def test_pola_demo_orders_aman(analyzer):
    hasil = analyzer.analyze(POLA_ORDERS_AMAN_DENGAN_TENANT)
    assert hasil.pattern_violations == []


def test_pola_demo_analytics_lintas_tenant(analyzer):
    hasil = analyzer.analyze(POLA_ANALYTICS_LINTAS_TENANT)
    assert "cross_tenant_operation" in hasil.pattern_violations


def test_pola_demo_users_campuran_field(analyzer):
    hasil = analyzer.analyze(POLA_USERS_CAMPURAN_FIELD_TENANT)
    assert "inconsistent_tenant_field_mix" in hasil.pattern_violations


def test_pola_demo_lookup_tanpa_batas(analyzer):
    hasil = analyzer.analyze(POLA_LOOKUP_TANPA_BATAS_TENANT)
    assert "lookup_tenant_boundary_missing" in hasil.pattern_violations


def test_mulai_audit_dengan_semua_pola_demo():
    from app.agent.tessera_agent import TesseraAgent

    agen = TesseraAgent("proyek-tes", "us-central1")
    laporan = asyncio.run(
        agen.mulai_audit("tessera_demo", daftar_queries_kustom=DAFTAR_POLA_DEMO)
    )
    daftar_viol = laporan["violations_terdeteksi"]
    assert len(daftar_viol) >= 4
    tipe = {v["tipe_violation"] for v in daftar_viol}
    assert len(daftar_viol) >= 4
    assert "missing_tenant_filter" in tipe
    assert "cross_tenant_operation" in tipe
    assert "inconsistent_tenant_field_mix" in tipe
    assert "lookup_tenant_boundary_missing" in tipe
