"""
Pola query yang diproduksi endpoint demo-app — dipakai Tessera untuk uji manual/otomatis.

Setiap entri mengikuti bentuk yang dianalisis `MongoDBQueryAnalyzer` / API audit.
"""

from typing import Any, Dict, List

# GET /orders — tanpa filter tenant (CRITICAL)
POLA_ORDERS_TANPA_TENANT: Dict[str, Any] = {
    "collection": "orders",
    "command": "find",
    "filter": {"status": "pending"},
}

# GET /orders/{id} — aman dengan tenant_id
POLA_ORDERS_AMAN_DENGAN_TENANT: Dict[str, Any] = {
    "collection": "orders",
    "command": "find",
    "filter": {"_id": "507f1f77bcf86cd799439011", "tenant_id": "acme-corp"},
}

# GET /analytics — agregasi lintas tenant (HIGH); $match punya tenant tapi $group tidak
POLA_ANALYTICS_LINTAS_TENANT: Dict[str, Any] = {
    "collection": "analytics_events",
    "command": "aggregate",
    "pipeline": [
        {"$match": {"event_type": "purchase", "tenant_id": "acme-corp"}},
        {"$group": {"_id": "$event_type", "jumlah": {"$sum": 1}}},
    ],
}

# GET /users — campuran tenant_id dan tenantId (MEDIUM)
POLA_USERS_CAMPURAN_FIELD_TENANT: Dict[str, Any] = {
    "collection": "users",
    "command": "find",
    "filter": {"tenantId": "globex", "tenant_id": "acme-corp"},
}

# GET /reports/join — $lookup tanpa batas tenant (CRITICAL)
POLA_LOOKUP_TANPA_BATAS_TENANT: Dict[str, Any] = {
    "collection": "orders",
    "command": "aggregate",
    "pipeline": [
        {"$match": {"tenant_id": "acme-corp"}},
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "profil",
            }
        },
    ],
}

DAFTAR_POLA_DEMO: List[Dict[str, Any]] = [
    POLA_ORDERS_TANPA_TENANT,
    POLA_ORDERS_AMAN_DENGAN_TENANT,
    POLA_ANALYTICS_LINTAS_TENANT,
    POLA_USERS_CAMPURAN_FIELD_TENANT,
    POLA_LOOKUP_TANPA_BATAS_TENANT,
]

NAMA_POLA_KE_PELANGGARAN_DIHARAPKAN: Dict[str, List[str]] = {
    "orders_tanpa_tenant": ["missing_tenant_filter"],
    "orders_aman": [],
    "analytics_lintas": ["cross_tenant_operation"],
    "users_campuran": ["inconsistent_tenant_field_mix"],
    "lookup_tanpa_batas": ["lookup_tenant_boundary_missing"],
}

KUNCI_POLA_DEMO: List[str] = list(NAMA_POLA_KE_PELANGGARAN_DIHARAPKAN.keys())
