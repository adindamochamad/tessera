# Tessera Demo App

Aplikasi FastAPI multi-tenant **dengan pelanggaran isolasi yang disengaja** — subjek audit untuk Tessera (Day 1).

## Menjalankan

```bash
cd demo-app
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Tanpa Atlas (mode memori):
uvicorn app.main:aplikasi --reload --port 8081

# Dengan Atlas (set MONGODB_URI di .env root atau export):
export MONGODB_URI="mongodb+srv://..."
export MONGODB_DATABASE=tessera_demo
uvicorn app.main:aplikasi --reload --port 8081
```

## Endpoint

| Method | Path | Pelanggaran |
|--------|------|-------------|
| GET | `/orders` | Tanpa filter `tenant_id` (CRITICAL) |
| GET | `/orders/{id}` | Aman — butuh `X-Tenant-Id` |
| GET | `/analytics` | `$group` lintas tenant (HIGH) |
| GET | `/users` | Campuran `tenant_id` / `tenantId` (MEDIUM) |
| GET | `/reports/join` | `$lookup` tanpa batas tenant (CRITICAL) |
| GET | `/internal/pola-query-audit` | Ekspor pola untuk API Tessera |

## Audit dengan Tessera

```bash
# 1. Backend Tessera
cd backend && source venv/bin/activate && uvicorn app.api.main:app --reload

# 2. Pola dari demo (atau pakai skrip)
./scripts/uji-audit-demo.sh
```

Pola statis juga ada di `pola_query_audit.py` — diuji otomatis oleh `backend/tests/test_demo_app_pola_audit.py`.
