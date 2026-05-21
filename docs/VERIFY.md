# Verifikasi Tessera (otomatis dan manual)

**Tidak ada satu nama framework atau satu perintah ajaib** yang bisa **memjamin** aplikasi Anda identik sepenuhnya dengan produksi (GCP live + MCP + Gemini + Atlas) tanpa **tes integrasi atau E2E** yang Anda desain sendiri. Praktik proyek matang memakai **piramida verifikasi berlapis**. Tessera sudah menyediakan beberapa lapisan tersebut; Anda dapat menambahkan lapisan atas (misalnya tes API FastAPI atau E2E dengan Playwright) sesuai kebutuhan hackathon Anda.

## Piramida verifikasi (apa yang sudah ada di repo ini)

| Tingkat | Yang diverifikasi | Cara Anda menjalankan / di mana ada |
|---------|---------------------|--------------------------------------|
| 1 Rules agent | Konteks Tessera konsisten bagi Cursor AI | `./scripts/verify.sh` (cek `.cursor/rules` + pipeline `AGENTS.md` / skills) |
| 2 Lint + tipe frontend | pola React/TS yang bermasalah sebelum jalankan server | `npm run lint`, `npm run type-check` di dalam `./scripts/verify.sh` |
| 3 Unit test backend | perilaku `query_analyzer`, `profiler_ingest`, integrasi ringkas `langchain_core` | `pytest` + cakupan **`app/analyzers` ≥80 %** (`pytest-cov`, `backend/pytest.ini`) di `./scripts/verify.sh` |
| 4 Sintaks seluruh modul Python `app/` | fail impor/sintaks di berkas yang belum disentuh tes | `python -m compileall -q app` di dalam `./scripts/verify-full.sh` |
| 5 Build produksi Next.js | error yang baru muncul saat bundel produksi | `npm run build` di dalam `./scripts/verify-full.sh` |
| 6 CI di GitHub | ulang semua di atas pada mesin bersih (Python 3.11) | workflow **`.github/workflows/ci.yml`** |
| 7 *Sebagian* — API audit | `POST /api/v1/audit/start` dengan `TestClient` | `backend/tests/test_api_audit.py` |
| 8 *Belum ada* — E2E UI | alur klik sungguhan | Playwright atau Cypress nanti jika alur UI kompleks |
| 9 *Belum ada* — integrasi Atlas/MCP/Vertex | perilaku terhadap layanan sungguhan | sandboxes, secrets terlarang di CI, atau mocking terkendali |

**Perintah jangkar**

- Harian / setelah edit agent: `./scripts/verify.sh` (atau `npm run verify` dari akar repo apabila Anda memakai `package.json` monorepo tipis di root).
- Sebelum PR penting atau menutup hari hackathon yang menyentuh frontend build: `./scripts/verify-full.sh` (atau `npm run verify:full`).

---

Dokumen di bawah menjelaskan detail penggunaan skrip verifikasi dan langkah manual pelengkap.

## Verifikasi otomatis (disarankan)

Dari root repository:

```bash
chmod +x scripts/verify.sh   # hanya pertama kali, jika perlu izin eksekusi
./scripts/verify.sh
```

Skrip akan:

1. Memastikan ada folder `.cursor/rules` dan minimal satu file `.mdc`.
2. Menjalankan `pytest` di `backend/`:
   - Jika `backend/venv` sudah ada **dan** sudah terpasang `pytest`, skrip memakai interpreter itu.
   - Jika belum, skrip membuat `backend/venv` lalu memasang **`backend/requirements-verify.txt`** (hanya pemasangan ringan untuk menjalankan unit test sekarang ini; **tidak sama** dengan `requirements.txt` penuh).
   - `backend/pytest.ini` membatasi penemuan tes ke folder **`tests/`** saja sehingga modul aplikasi tidak disalahartikan sebagai tes, dan menambahkan **`pytest-cov`** pada paket **`app/analyzers`** dengan **fail-under 80 %**.
3. Menjalankan `npm run lint` dan `npm run type-check` di `frontend/` (membutuhkan `npm install` di `frontend/`).

**Catatan**: stack lengkap Tessera tetap bersandar pada **`requirements.txt`** dan **Python 3.11+**. `backend/requirements-verify.txt` memuat `fastapi`, `httpx`, `pydantic` versi fleksibel, **`pytest-cov`**, serta **`langchain-core`** (integrasi ringkas di `app/agent/langchain_lingkar_audit.py`); Vertex + dependency LangChain penuh tetap lewat `requirements.txt`. Jalur `./scripts/verify.sh` memastikan tes dan API ringan jalan tanpa Mongo/Gemini sungguhan.

**Keluar sukses** = kode keluar `0` dan pesan akhir «Semua pemeriksaan otomatis lulus».

### Penutupan hari kerja (hackathon)

Sebelum Anda pindah fokus ke milestone TODOLIST berikutnya, **`./scripts/verify.sh`** wajib hijau atas perubahan di branch Anda, kecuali ada **blokir luar** dengan jejak dokumentasi di **`docs/HACKATHON_BLOCKERS.md`** (lihat panduan lebih panjang **`docs/HACKATHON_QUALITY_BAR.md`** serta **Gate keluar** di **`docs/TODOLIST-7-HARI.md`**).

---

## Saat `./scripts/verify.sh` gagal

| Pesannya | Yang biasanya salah |
|-----------|---------------------|
| `LEWATI frontend: jalankan npm install` | Jalankan `cd frontend && npm install`, lalu ulangi skrip. |
| pytest gagal | Perbaiki tes atau implementasi sesuai error stack trace di terminal. |
| `npm run lint` / type-check gagal | Perbaiki error ESLint atau TypeScript yang ditampilkan. |

Agent AI diarahkan oleh rule proyek untuk menjalankan skrip ini dan memberi ringkasan hasil kepada Anda setelah menyentuh kode substantive.

---

## Verifikasi manual tambahan

Lakukan jika Anda ingin melihat bahwa aplikasi bisa dijalankan, bukan hanya lint/tipe/tes statis.

### 1. Cek Cursor Rules ter-load di editor

Anda menggunakan Cursor:

1. Buka **[Cursor Settings]** → bagian **[Rules]** (nama menu bisa sedikit berbeda per versi Cursor).
2. Pastikan Anda melihat rule proyek seperti **«Konteks Tessera + …»** (rule `alwaysApply`).
3. Opsional: buka file `frontend/app/page.tsx` dan pastikan rule terkait frontend muncul / relevan ketika Anda bekerja di file tersebut (bergantung versi Cursor).

Ini memvalidasi bahwa berkas ada di `.cursor/rules/*.mdc` dan biasanya terdeteksi workspace.

### 2. Backend cepat (`/health`)

```bash
cd backend && source venv/bin/activate  # jika memakai venv
pip install -r requirements.txt          # pertama kali
uvicorn app.api.main:app --reload &
# Di terminal lain:
curl -s http://localhost:8000/health | head
```

Anda boleh hentikan server (`fg` lalu Ctrl+C atau `pkill`-sesuai kebutuhan).

**Catatan**: `config` bisa memerlukan `.env`; jika `uvicorn` gagal karena env, salin `.env.example` ke `.env` dan isi placeholder (lihat `docs/QUICKSTART.md`). Verifikasi manual ini tetap berguna walau `./scripts/verify.sh` bisa lulus dengan env minimal untuk pytest.

### 3. Frontend dev

```bash
cd frontend && npm install && npm run dev
```

Buka browser `http://localhost:3000` — pastikan halaman utama Tessera dimuat tanpa error di konsol browser.

### 4. Sanity git (tanpa mengubah history)

Anda bisa memastikan tidak ada file sensitif tertulis:

```bash
git status
git diff --stat
```

Jangan mengutip isi `.env` atau kunci GCP ke dokumen atau commit.

---

## Ringkasan

| Metode | Kapan digunakan |
|--------|-------------------|
| `./scripts/verify.sh` atau `npm run verify` | Sesudah sebagian besar penyuntingan cepat; cepat. |
| `./scripts/verify-full.sh` atau `npm run verify:full` | Sebelum PR utama / sebelum merekam video; termasuk `compileall` + Next **production build**. |
| GitHub Actions workflow **CI** | Setiap push/PR; ulang verifikasi atas mesin bersih. |
| Curl + uvicorn | Setelah menyentuh API atau konfigurasi runtime. |
| `npm run dev` | Setelah menyentuh UI/layout. |
| Cek Rules di Cursor Settings | Setelah menambah/mengubah `.cursor/rules/`. |

Jika nanti Anda menambah alat baru (misalnya **Playwright** untuk E2E), pertimbangkan memanggilnya dari `verify-full.sh` atau job CI terpisah agar piramida bertambah konsisten.
