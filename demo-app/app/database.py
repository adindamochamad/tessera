"""
Koneksi MongoDB atau penyimpanan in-memory untuk demo lokal tanpa Atlas.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import structlog
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import pengaturan_demo

logger = structlog.get_logger()

_klien_motor: Optional[AsyncIOMotorClient] = None
_basis_data: Optional[AsyncIOMotorDatabase] = None
_memori: Dict[str, List[Dict[str, Any]]] = {}


def memakai_mode_memori() -> bool:
    uri = pengaturan_demo.mongodb_uri.strip()
    return not uri or uri.startswith("memory://")


async def dapatkan_basis_data() -> AsyncIOMotorDatabase:
    global _klien_motor, _basis_data
    if memakai_mode_memori():
        raise RuntimeError("basis_data_motor_tidak_tersedia_di_mode_memori")
    if _basis_data is None:
        _klien_motor = AsyncIOMotorClient(pengaturan_demo.mongodb_uri)
        _basis_data = _klien_motor[pengaturan_demo.mongodb_database]
        logger.info("demo_mongodb_terhubung", database=pengaturan_demo.mongodb_database)
    return _basis_data


def koleksi_memori(nama_koleksi: str) -> List[Dict[str, Any]]:
    return _memori.setdefault(nama_koleksi, [])


async def muat_data_awal_memori() -> None:
    """Isi contoh tiga tenant bila belum ada dokumen."""
    if _memori.get("orders"):
        return
    contoh = [
        {
            "_id": "o1",
            "tenant_id": "acme-corp",
            "customer_name": "Alice",
            "amount": 120.5,
            "status": "pending",
            "user_id": "u1",
        },
        {
            "_id": "o2",
            "tenant_id": "globex",
            "customer_name": "Bob",
            "amount": 89.0,
            "status": "pending",
            "user_id": "u2",
        },
        {
            "_id": "o3",
            "tenant_id": "initech",
            "customer_name": "Carol",
            "amount": 200.0,
            "status": "shipped",
            "user_id": "u3",
        },
    ]
    _memori["orders"] = contoh
    _memori["users"] = [
        {"_id": "u1", "tenant_id": "acme-corp", "email": "a@acme.com", "role": "admin"},
        {"_id": "u2", "tenantId": "globex", "email": "b@globex.com", "role": "user"},
        {"_id": "u3", "tenant_id": "initech", "email": "c@initech.com", "role": "viewer"},
    ]
    _memori["analytics_events"] = [
        {"tenant_id": "acme-corp", "event_type": "purchase", "metadata": {"sku": "A1"}},
        {"tenant_id": "globex", "event_type": "purchase", "metadata": {"sku": "B2"}},
        {"tenant_id": "initech", "event_type": "view", "metadata": {"page": "/home"}},
    ]


async def tutup_koneksi() -> None:
    global _klien_motor, _basis_data
    if _klien_motor is not None:
        _klien_motor.close()
        _klien_motor = None
        _basis_data = None
