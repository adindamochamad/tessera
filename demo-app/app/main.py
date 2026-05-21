"""
Demo multi-tenant SaaS — sengaja berisi pola query berisiko untuk diaudit Tessera.

Jalankan: uvicorn app.main:aplikasi --reload --port 8081 (dari folder demo-app)
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

import structlog
from fastapi import FastAPI, Header, HTTPException, Query

from app.config import pengaturan_demo
from app.database import (
    dapatkan_basis_data,
    koleksi_memori,
    memakai_mode_memori,
    muat_data_awal_memori,
    tutup_koneksi,
)

logger = structlog.get_logger()


@asynccontextmanager
async def siklus_hidup_aplikasi(_: FastAPI):
    if memakai_mode_memori():
        await muat_data_awal_memori()
        logger.info("demo_mode_memori_aktif")
    yield
    await tutup_koneksi()


aplikasi = FastAPI(
    title="Tessera Demo App",
    description="Aplikasi multi-tenant dengan pelanggaran isolasi yang disengaja",
    version="0.1.0",
    lifespan=siklus_hidup_aplikasi,
)


@aplikasi.get("/health")
async def cek_kesehatan():
    return {
        "status": "ok",
        "mode": "memory" if memakai_mode_memori() else "mongodb",
        "database": pengaturan_demo.mongodb_database,
    }


@aplikasi.get("/orders")
async def daftar_pesanan_tanpa_filter_tenant(
    status: str = Query(default="pending"),
):
    """
    CRITICAL: find orders tanpa tenant_id — semua tenant bisa terekspos.
    """
    filter_query = {"status": status}
    if memakai_mode_memori():
        baris = [d for d in koleksi_memori("orders") if d.get("status") == status]
        return {"mode": "memory", "filter": filter_query, "count": len(baris), "data": baris}
    basis = await dapatkan_basis_data()
    kursor = basis.orders.find(filter_query)
    hasil = await kursor.to_list(length=500)
    return {"mode": "mongodb", "filter": filter_query, "count": len(hasil), "data": hasil}


@aplikasi.get("/orders/{id_pesanan}")
async def detail_pesanan_aman(
    id_pesanan: str,
    x_tenant_id: Optional[str] = Header(default=None, alias="X-Tenant-Id"),
):
    """Aman: wajib header tenant + filter tenant_id pada find."""
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Header X-Tenant-Id wajib")
    filter_query = {"_id": id_pesanan, "tenant_id": x_tenant_id}
    if memakai_mode_memori():
        baris = [
            d
            for d in koleksi_memori("orders")
            if d.get("_id") == id_pesanan and d.get("tenant_id") == x_tenant_id
        ]
        if not baris:
            raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")
        return {"mode": "memory", "filter": filter_query, "data": baris[0]}
    basis = await dapatkan_basis_data()
    dok = await basis.orders.find_one(filter_query)
    if dok is None:
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")
    return {"mode": "mongodb", "filter": filter_query, "data": dok}


@aplikasi.get("/analytics")
async def ringkasan_analytics_lintas_tenant(
    event_type: str = Query(default="purchase"),
):
    """
    HIGH: agregasi $group tanpa penyekatan tenant utama.
    """
    pipeline = [
        {
            "$match": {
                "event_type": event_type,
                "tenant_id": "acme-corp",
            }
        },
        {"$group": {"_id": "$event_type", "jumlah": {"$sum": 1}}},
    ]
    if memakai_mode_memori():
        baris = koleksi_memori("analytics_events")
        cocok = [d for d in baris if d.get("event_type") == event_type]
        return {
            "mode": "memory",
            "pipeline": pipeline,
            "hasil": [{"_id": event_type, "jumlah": len(cocok)}],
        }
    basis = await dapatkan_basis_data()
    hasil = await basis.analytics_events.aggregate(pipeline).to_list(length=50)
    return {"mode": "mongodb", "pipeline": pipeline, "hasil": hasil}


@aplikasi.get("/users")
async def daftar_pengguna_campuran_field_tenant(
    tenant_id: Optional[str] = Query(default=None),
    tenantId: Optional[str] = Query(default=None),
):
    """
    MEDIUM: filter bisa memakai tenant_id dan tenantId sekaligus (inkonsisten).
    """
    filter_query: Dict[str, Any] = {}
    if tenant_id:
        filter_query["tenant_id"] = tenant_id
    if tenantId:
        filter_query["tenantId"] = tenantId
    if not filter_query:
        filter_query = {"tenantId": "globex", "tenant_id": "acme-corp"}
    if memakai_mode_memori():
        baris = [
            d
            for d in koleksi_memori("users")
            if all(d.get(k) == v for k, v in filter_query.items())
        ]
        return {"mode": "memory", "filter": filter_query, "data": baris}
    basis = await dapatkan_basis_data()
    kursor = basis.users.find(filter_query)
    hasil = await kursor.to_list(length=200)
    return {"mode": "mongodb", "filter": filter_query, "data": hasil}


@aplikasi.get("/reports/join")
async def laporan_join_tanpa_batas_tenant(
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
):
    """CRITICAL: $lookup ke users tanpa memastikan foreignField menyertakan tenant."""
    pipeline = [
        {"$match": {"tenant_id": x_tenant_id}},
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "profil",
            }
        },
    ]
    if memakai_mode_memori():
        pesanan = [d for d in koleksi_memori("orders") if d.get("tenant_id") == x_tenant_id]
        return {"mode": "memory", "pipeline": pipeline, "sample_count": len(pesanan)}
    basis = await dapatkan_basis_data()
    hasil = await basis.orders.aggregate(pipeline).to_list(length=100)
    return {"mode": "mongodb", "pipeline": pipeline, "hasil": hasil}


@aplikasi.get("/internal/pola-query-audit")
async def ekspor_pola_untuk_tessera() -> Dict[str, List[Dict[str, Any]]]:
    """Daftar pola query untuk POST /api/v1/audit/start (pengembangan)."""
    import sys
    from pathlib import Path

    akar_demo = Path(__file__).resolve().parents[2]
    if str(akar_demo) not in sys.path:
        sys.path.insert(0, str(akar_demo))
    from pola_query_audit import DAFTAR_POLA_DEMO  # noqa: PLC0415

    return {"pola": DAFTAR_POLA_DEMO, "jumlah": len(DAFTAR_POLA_DEMO)}
