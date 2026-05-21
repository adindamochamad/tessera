# Infrastruktur Day 1 — GCP & MongoDB Atlas

Langkah yang **harus dijalankan di akun Anda** (billing/credential). Repo menyediakan skrip bantu; centang di `TODOLIST-7-HARI.md` setelah selesai.

## Google Cloud

```bash
chmod +x scripts/infra/setup-gcp.sh
export TESSERA_GCP_PROJECT=tessera-hackathon   # atau nama Anda
./scripts/infra/setup-gcp.sh
```

Perbarui `.env`:

```env
GOOGLE_CLOUD_PROJECT=tessera-hackathon
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
VERTEX_AI_LOCATION=us-central1
```

**Billing:** aktifkan akun billing dan klaim kredit hackathon di konsol GCP.

## MongoDB Atlas

1. Buat cluster **M0** (free tier).
2. Database user + network access (IP Anda atau `0.0.0.0/0` sementara untuk dev).
3. Salin connection string ke `.env`:

```env
MONGODB_URI=mongodb+srv://USER:PASS@cluster.mongodb.net/
MONGODB_DATABASE=tessera_demo
```

4. Seed data demo:

```bash
python3 scripts/seed_mongodb_demo.py
```

5. **Vector Search** (persiapan Day 3):
   - Koleksi `violation_patterns` dengan field `embedding` (768 dim, sesuai model embedding nanti).
   - Buat Search Index dari `scripts/infra/atlas-vector-index.json` lewat Atlas UI → Search → Create Index, atau Atlas CLI.

## Demo app

```bash
cd demo-app && pip install -r requirements.txt
# Tanpa Atlas:
uvicorn app.main:aplikasi --reload --port 8081
# Dengan Atlas: set MONGODB_URI di .env root lalu jalankan sama.
```

## Blokir

Jika billing/API tertahan, catat di `docs/HACKATHON_BLOCKERS.md` dengan fallback demo (mode memori + rekaman lokal).
