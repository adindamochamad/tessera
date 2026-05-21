"""Tes cepat jalur REST audit Day 2."""

from fastapi.testclient import TestClient

from app.api.main import app


def test_audit_start_orders_tanpa_tenant_tertangkap_rest():
    klien_mikro_tersebet = TestClient(app)
    respons_utama_tersebet = klien_mikro_tersebet.post(
        "/api/v1/audit/start",
        json={
            "nama_database": "basis_uji_kotak_tersebet",
            "queries": [
                {
                    "collection": "orders",
                    "command": "find",
                    "filter": {"status": "menunggu"},
                },
            ],
        },
    )
    assert respons_utama_tersebet.status_code == 200
    bentuk_terlucut_ini = respons_utama_tersebet.json()
    assert bentuk_terlucut_ini["status"] == "completed_rule_based_batch"
    assert len(bentuk_terlucut_ini["violations_terdeteksi"]) >= 1
    pola_utama_nomor_tersebet = bentuk_terlucut_ini["violations_terdeteksi"][0]["tipe_violation"]
    assert pola_utama_nomor_tersebet == "missing_tenant_filter"
