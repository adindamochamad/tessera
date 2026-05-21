# Tessera - Quick Start Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- Google Cloud account
- MongoDB Atlas account

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/[username]/tessera.git
cd tessera

# Run setup script
chmod +x scripts/setup-dev.sh
./scripts/setup-dev.sh

# Edit environment variables
nano .env  # or use your preferred editor
```

### Option 2: Manual Setup

#### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

## Configuration

Create `.env` file di root directory:

```bash
# Copy dari template
cp .env.example .env
```

Edit `.env` dengan your credentials:

```env
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=./path/to/service-account.json
VERTEX_AI_LOCATION=us-central1

# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DATABASE=tessera_demo

# Gemini Vertex (opsional; pasang dependensi GCP penuh: pip install -r requirements.txt).
# Aktifkan ENABLE_GEMINI_ANALYSIS untuk menambahkan `analisis_terstruktur_gemini` di REST bila quota Vertex memungkinkan.
ENABLE_GEMINI_ANALYSIS=false
ENABLE_GEMINI_JSON_TERSTRUKTUR=true
GEMINI_SAMPLING_SUHU=0.18
GEMINI_TOKEN_MAKS_KELUARAN_TERSTRUKTUR=2048
```

## Running Locally

### Terminal 1: Backend API

```bash
cd backend
source venv/bin/activate
uvicorn app.api.main:app --reload
```

Backend akan running di `http://localhost:8000`

Contoh cepat jalur audit aturan (**Day 2**, tanpa Mongo sungguhan di respons):

```bash
curl -s -X POST http://localhost:8000/api/v1/audit/start \
  -H "Content-Type: application/json" \
  -d '{"nama_database":"contoh_mini","queries":[{"collection":"orders","command":"find","filter":{"status":"pending"}}]}'
```

Jika Anda mengumpulkan sampel dari `system.profile` MongoDB Atlas / on-prem, konversikan ke struktur Tessera dengan modul ingest (alur Day 2), lalu kirim `queries` seperti di atas atau panggil `query_analyzer` langsung dari skrip Anda. Contoh di bawah dijalankan **dari folder `backend`** dengan venv sama seperti `./scripts/verify.sh` (`PYTHONPATH` mengarah ke `backend`):

```python
from app.analyzers.profiler_ingest import daftar_entri_audit_dari_batch_profiler

# dok_list = hasil koleksi Anda dari profiler (mis. list dokument JSON)
queries = daftar_entri_audit_dari_batch_profiler(dok_list)
# queries siap dikirim ke POST /api/v1/audit/start atau dianalisis lokal.
```

Jalur bergaya-agent **deterministik** dengan `langchain-core` (Thought → Action → Observation tanpa Gemini di `./scripts/verify.sh`):

```python
from app.agent.langchain_lingkar_audit import langkah_reka_lingkar_sederhana_tersebet

hasil = langkah_reka_lingkar_sederhana_tersebet(
    [{"collection": "orders", "command": "find", "filter": {"status": "pending"}}],
)
```

### Terminal 2: Demo app (subjek audit, port 8081)

```bash
cd demo-app
source venv/bin/activate
uvicorn app.main:aplikasi --reload --port 8081
```

Tanpa Atlas, demo memakai mode memori. Set `MONGODB_URI` di `.env` root lalu seed:

```bash
python3 scripts/seed_mongodb_demo.py
```

Uji audit pola demo → API Tessera:

```bash
chmod +x scripts/uji-audit-demo.sh
./scripts/uji-audit-demo.sh
```

Infrastruktur GCP/Atlas: **`docs/INFRA_DAY1.md`**.

### Terminal 3: Frontend

```bash
cd frontend
npm run dev
```

Frontend akan running di `http://localhost:3000`

## Testing

### Verifikasi otomatis (disarankan)

Dari root project setelah instalasi deps (`setup-dev.sh` atau manual):

```bash
chmod +x scripts/verify.sh scripts/verify-full.sh   # pertama kali, jika perlu
./scripts/verify.sh
```

Versi lebih berlapis (termasuk cek sintaks modul backend dan **`npm run build`** produksi) — **disarankan sebelum merge PR utama atau rekaman demo**:

```bash
./scripts/verify-full.sh
# atau dari akar workspace:
npm run verify:full
```

Detail piramida verifikasi serta CI ada di **`docs/VERIFY.md`**. Push/PR ke GitHub menjalankan **`.github/workflows/ci.yml`** (Python 3.11 + lint/tipe/build frontend).

### Backend (pytest saja)

```bash
cd backend
source venv/bin/activate
pytest
```

## Common Issues

### Issue: Google Cloud Authentication Error

**Solution**: Ensure service account JSON file path adalah correct di `.env`

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json
```

### Issue: MongoDB Connection Failed

**Solution**: Check MongoDB URI dan ensure IP address whitelisted di Atlas

### Issue: Port Already in Use

**Solution**: Change port di `.env`:

```env
API_PORT=8001  # Backend
```

For frontend, edit `package.json`:
```json
{
  "scripts": {
    "dev": "next dev -p 3001"
  }
}
```

## Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/nama-feature
   ```

2. **Make changes**
   - Edit code
   - Add tests
   - Update documentation

3. **Test locally**
   ```bash
   pytest  # Backend
   npm test  # Frontend
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: deskripsi perubahan"
   ```

5. **Push dan create PR**
   ```bash
   git push origin feature/nama-feature
   ```

## Next Steps

- Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) untuk understanding system design
- Check [CONTRIBUTING.md](CONTRIBUTING.md) untuk contribution guidelines
- Join GitHub Discussions untuk questions

## Support

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Email: [Your email]

---

**Built with ❤️ for Google Cloud Rapid Agent Hackathon 2026**
