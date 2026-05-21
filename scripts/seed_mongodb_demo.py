#!/usr/bin/env python3
"""
Seed database demo Tessera (3 tenant + koleksi orders/users/analytics_events).

Jalankan dari akar repo dengan MONGODB_URI valid di .env:
  python3 scripts/seed_mongodb_demo.py
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore

if load_dotenv:
    load_dotenv(ROOT / ".env")

from pymongo import MongoClient  # noqa: E402


def utama() -> int:
    uri = os.environ.get("MONGODB_URI", "").strip()
    nama_basis = os.environ.get("MONGODB_DATABASE", "tessera_demo").strip()
    if not uri or uri.startswith("memory://"):
        print("Lewati seed: set MONGODB_URI di .env (bukan memory://).")
        return 0

    klien = MongoClient(uri, serverSelectionTimeoutMS=8000)
    klien.admin.command("ping")
    basis = klien[nama_basis]

    sekarang = datetime.now(timezone.utc)
    tenant_acme = "acme-corp"
    tenant_globex = "globex"
    tenant_initech = "initech"

    basis.orders.delete_many({})
    basis.users.delete_many({})
    basis.analytics_events.delete_many({})

    basis.orders.insert_many(
        [
            {
                "tenant_id": tenant_acme,
                "customer_name": "Alice Acme",
                "amount": 120.5,
                "status": "pending",
                "user_id": "u-acme-1",
                "created_at": sekarang,
            },
            {
                "tenant_id": tenant_globex,
                "customer_name": "Bob Globex",
                "amount": 89.0,
                "status": "pending",
                "user_id": "u-globex-1",
                "created_at": sekarang,
            },
            {
                "tenant_id": tenant_initech,
                "customer_name": "Carol Initech",
                "amount": 200.0,
                "status": "shipped",
                "user_id": "u-initech-1",
                "created_at": sekarang,
            },
        ]
    )
    basis.users.insert_many(
        [
            {
                "tenant_id": tenant_acme,
                "email": "alice@acme.com",
                "role": "admin",
            },
            {
                "tenantId": tenant_globex,
                "email": "bob@globex.com",
                "role": "user",
            },
            {
                "tenant_id": tenant_initech,
                "email": "carol@initech.com",
                "role": "viewer",
            },
        ]
    )
    basis.analytics_events.insert_many(
        [
            {
                "tenant_id": tenant_acme,
                "event_type": "purchase",
                "metadata": {"sku": "A1"},
            },
            {
                "tenant_id": tenant_globex,
                "event_type": "purchase",
                "metadata": {"sku": "B2"},
            },
            {
                "tenant_id": tenant_initech,
                "event_type": "view",
                "metadata": {"page": "/home"},
            },
        ]
    )

    print(f"Seed selesai: {nama_basis} — orders/users/analytics_events")
    print("Tenant: acme-corp, globex, initech")
    return 0


if __name__ == "__main__":
    raise SystemExit(utama())
