"""Tes untuk konversi dokumen profiler → bentuk analyzer."""

from app.analyzers.profiler_ingest import (
    bagi_string_ns_jadi_basis_dan_koleksi,
    daftar_entri_audit_dari_batch_profiler,
    entri_audit_dari_dok_profiler,
)
from app.analyzers.query_analyzer import query_analyzer


def test_bagi_ns_memisahkan_pada_titik_pertama_saja():
    basis, koleksi = bagi_string_ns_jadi_basis_dan_koleksi("saas.orders.events")
    assert basis == "saas"
    assert koleksi == "orders.events"


def test_profiler_find_terjemahkan_dan_terdeteksi_tanpa_tenant():
    dok_profiler_mini = {
        "op": "query",
        "ns": "contoh.orders",
        "command": {
            "$db": "contoh",
            "find": "orders",
            "filter": {"status": "open"},
            "projection": {"_id": 0},
        },
    }
    entri = entri_audit_dari_dok_profiler(dok_profiler_mini)
    assert entri is not None
    assert entri["collection"] == "orders"
    assert entri["command"] == "find"
    assert entri["database"] == "contoh"
    analisis = query_analyzer.analyze(entri)
    assert "missing_tenant_filter" in analisis.pattern_violations


def test_profiler_aggregate_dengan_pipeline_masuk_analyzer():
    dok_profiler_agg = {
        "op": "command",
        "ns": "saas.orders",
        "command": {
            "$db": "saas",
            "aggregate": "orders",
            "pipeline": [{"$match": {}}, {"$group": {"_id": "$status", "hitung_total": {"$sum": 1}}}],
            "cursor": {},
        },
    }
    entri = entri_audit_dari_dok_profiler(dok_profiler_agg)
    assert entri["command"] == "aggregate"
    analisis = query_analyzer.analyze(entri)
    assert analisis.ada_cross_tenant or "missing_tenant_filter" in analisis.pattern_violations


def test_dok_profiler_insert_ditolak_returns_none():
    assert (
        entri_audit_dari_dok_profiler({"command": {"insert": "orders", "documents": [{}]}})
        is None
    )


def test_batch_profiler_membuang_tidak_terdukung():
    campuran = [
        {
            "ns": "a.orders",
            "command": {"$db": "a", "find": "orders", "filter": {"tenant_id": "t1"}},
        },
        {"command": {"killCursors": 1}},
    ]
    ringkas = daftar_entri_audit_dari_batch_profiler(campuran)
    assert len(ringkas) == 1
    assert ringkas[0]["collection"] == "orders"


def test_bagi_ns_non_string_mengembalikan_kosong():
    assert bagi_string_ns_jadi_basis_dan_koleksi(123) == ("", "")  # type: ignore[arg-type]


def test_bagi_ns_tanpa_titik_semua_basis():
    basis, koleksi = bagi_string_ns_jadi_basis_dan_koleksi("hanya_satu_token")
    assert basis == "hanya_satu_token"
    assert koleksi == ""


def test_entri_profiler_input_bukan_mapping():
    assert entri_audit_dari_dok_profiler([]) is None  # type: ignore[arg-type]


def test_entri_profiler_find_legacy_dquery():
    dok = {
        "ns": "x.orders",
        "command": {
            "$db": "x",
            "find": "orders",
            "query": {"$query": {"tenant_id": "t-legacy", "ok": 1}},
        },
    }
    entri = entri_audit_dari_dok_profiler(dok)
    assert entri is not None
    assert entri["filter"]["tenant_id"] == "t-legacy"


def test_agregasi_profiler_pipeline_bukan_list_dianggap_kosong():
    dok = {
        "command": {
            "$db": "x",
            "aggregate": "orders",
            "pipeline": "bukan_list",
        },
    }
    entri = entri_audit_dari_dok_profiler(dok)
    assert entri is not None
    assert entri["pipeline"] == []
