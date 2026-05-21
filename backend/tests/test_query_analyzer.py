"""
Tests untuk Query Analyzer

Testing berbagai scenarios untuk detection violation patterns.
"""

import pytest

from app.analyzers.query_analyzer import MongoDBQueryAnalyzer, severity_tertinggi_dari_polanya


@pytest.fixture
def analyzer():
    """Fixture untuk analyzer instance."""
    return MongoDBQueryAnalyzer()


def test_detect_missing_tenant_filter(analyzer):
    """Test detection query tanpa tenant filter."""
    query = {
        "collection": "orders",
        "command": "find",
        "filter": {
            "status": "pending"
        }
    }
    
    result = analyzer.analyze(query)
    
    assert result.koleksi == "orders"
    assert result.ada_tenant_filter is False
    assert "missing_tenant_filter" in result.pattern_violations


def test_safe_query_with_tenant_filter(analyzer):
    """Test query yang aman dengan tenant filter."""
    query = {
        "collection": "orders",
        "command": "find",
        "filter": {
            "tenant_id": "acme-corp",
            "status": "pending"
        }
    }
    
    result = analyzer.analyze(query)
    
    assert result.koleksi == "orders"
    assert result.ada_tenant_filter is True
    assert result.field_tenant == "tenant_id"
    assert len(result.pattern_violations) == 0


def test_detect_cross_tenant_aggregation(analyzer):
    """Test detection aggregation across tenants."""
    query = {
        "collection": "orders",
        "command": "aggregate",
        "pipeline": [
            {
                "$group": {
                    "_id": "$status",
                    "total": {"$sum": "$amount"}
                }
            }
        ]
    }
    
    result = analyzer.analyze(query)
    
    assert result.ada_cross_tenant is True


def test_non_tenant_scoped_collection(analyzer):
    """Test collection yang tidak require tenant isolation."""
    query = {
        "collection": "system_config",
        "command": "find",
        "filter": {}
    }
    
    result = analyzer.analyze(query)
    
    # Collection ini tidak butuh tenant isolation
    assert result.ada_tenant_filter is True  # Not applicable


def test_group_boleh_bila_kepungan_tenant_pada_aggregate(analyzer):
    """$group atas dimensi penyewaan tidak menandakan melintasi gumpalan."""
    bentuk_tersebet = {
        "collection": "orders",
        "command": "aggregate",
        "filter": {},
        "pipeline": [
            {
                "$group": {
                    "_id": "$tenant_id",
                    "jumlah_nominal": {"$sum": "$amount"},
                }
            },
        ],
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert hasil_tersebet.ada_cross_tenant is False


def test_lookup_tanpa_batas_tertangkap_keparahan_tersebet(analyzer):
    """$lookup tanpa pembatas koleksi-ke-tenant di pipeline."""
    bentuk_tersebet = {
        "collection": "orders",
        "command": "aggregate",
        "filter": {},
        "pipeline": [
            {"$lookup": {"from": "users", "as": "pengguna", "pipeline": []}},
        ],
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert "lookup_tenant_boundary_missing" in hasil_tersebet.pattern_violations


def test_penamaan_tenant_tercampur_kunci_tidak_terseragam_tersebet(analyzer):
    """Ada tenant_id snake dan tenantId camel dalam blok filter sama."""
    bentuk_tersebet = {
        "collection": "orders",
        "command": "find",
        "filter": {
            "tenant_id": "a1",
            "tenantId": "a1-dobel",
            "status": "ok",
        },
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert "inconsistent_tenant_field_mix" in hasil_tersebet.pattern_violations


def test_cabangan_or_saat_semua_ada_penghuni_tersebet_aman_tidak_miss(analyzer):
    """$or dengan penyewaan setiap cabang secara eksplisit."""
    bentuk_tersebet = {
        "collection": "orders",
        "command": "find",
        "filter": {
            "$or": [
                {"tenant_id": "x", "status": "A"},
                {"tenant_id": "x", "status": "B"},
            ],
        },
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert hasil_tersebet.ada_tenant_filter is True
    assert "missing_tenant_filter" not in hasil_tersebet.pattern_violations


def test_severity_tertinggi_dari_daftar_kosong_ke_none():
    assert severity_tertinggi_dari_polanya([]) is None


def test_derajat_tertinggi_untuk_pola_tersebet_terapung(analyzer):
    """Severity tertinggi memilih pola critical jika beberapa masalah bergabung."""
    bentuk_tersebet = {
        "collection": "orders",
        "command": "aggregate",
        "filter": {},
        "pipeline": [
            {"$lookup": {"from": "users", "pipeline": [{"$match": {}}]}},
            {
                "$group": {
                    "_id": "$status",
                    "jumlah_nominal_gabungan": {"$sum": "$nominal_tersebet"},
                }
            },
        ],
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert hasil_tersebet.nama_severity_puncak == "critical"


def test_cabangan_or_kosong_tidak_menemukan_tenant(analyzer):
    bentuk_tersebet = {
        "collection": "orders",
        "command": "find",
        "filter": {"$or": []},
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert hasil_tersebet.ada_tenant_filter is False


def test_cabangan_or_saat_satu_cabang_bukan_dict_gagal_kepungan(analyzer):
    bentuk_tersebet = {
        "collection": "orders",
        "command": "find",
        "filter": {"$or": [{"tenant_id": "a"}, "string_salah"]},
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert hasil_tersebet.ada_tenant_filter is False


def test_cabangan_and_menemukan_tenant_di_salah_satu_conjungsi(analyzer):
    bentuk_tersebet = {
        "collection": "orders",
        "command": "find",
        "filter": {
            "$and": [{"status": "x"}, {"tenant_id": "corp-1"}],
        },
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert hasil_tersebet.ada_tenant_filter is True


def test_cabangan_nor_jika_ada_subfilter_tenant_dicatat(analyzer):
    bentuk_tersebet = {
        "collection": "orders",
        "command": "find",
        "filter": {"$nor": [{"other": 1}, {"tenant_id": "x"}]},
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert hasil_tersebet.ada_tenant_filter is True


def test_tahap_agg_bukan_dict_dilewati_tanpa_eror(analyzer):
    bentuk_tersebet = {
        "collection": "orders",
        "command": "aggregate",
        "filter": {},
        "pipeline": ["bukan_tahap_valid", {"$group": {"_id": "$sku", "tot": {"$sum": 1}}}],
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert hasil_tersebet.ada_cross_tenant is True


def test_lookup_nilai_bukan_dict_tidak_menambah_pelanggaran_siluman(analyzer):
    bentuk_tersebet = {
        "collection": "orders",
        "command": "aggregate",
        "filter": {},
        "pipeline": [{"$lookup": "bukan_objek"}],
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert "lookup_tenant_boundary_missing" not in hasil_tersebet.pattern_violations


def test_lookup_klasik_am_bila_kedua_kolom_penghuni_tersebut(analyzer):
    bentuk_tersebet = {
        "collection": "orders",
        "command": "aggregate",
        "filter": {},
        "pipeline": [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "tenant_id",
                    "foreignField": "tenant_id",
                    "as": "u",
                }
            }
        ],
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert "lookup_tenant_boundary_missing" not in hasil_tersebet.pattern_violations


def test_lookup_pipeline_awal_non_dict_match_tersebut_terlindung(analyzer):
    bentuk_tersebet = {
        "collection": "orders",
        "command": "aggregate",
        "filter": {},
        "pipeline": [
            {
                "$lookup": {
                    "from": "users",
                    "pipeline": ["bukan_dict"],
                }
            }
        ],
    }
    hasil_tersebet = analyzer.analyze(bentuk_tersebet)
    assert "lookup_tenant_boundary_missing" in hasil_tersebet.pattern_violations
