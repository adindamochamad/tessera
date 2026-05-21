# Tessera — Todolist 7 Hari Build

**Project**: Tessera — AI-Powered Multi-Tenant Data Isolation Auditor  
**Track**: MongoDB (Google Cloud Rapid Agent Hackathon 2026)  
**Deadline submission**: 02.00 WIB, 12 Juni 2026  
**Mulai build**: 20 Mei 2026  

---

## Ringkasan Progress

| Hari | Fokus | Status |
|------|--------|--------|
| Day 1 | Foundation & Architecture | ✅ Repo selesai — infra cloud/Atlas jalankan manual (`docs/INFRA_DAY1.md`) |
| Day 2 | Core Agent + Gemini (+ ingest profiler + LC ringkas + cov analyzer) | ✅ Repo selesai — Gemini live & LC+Gemini LLM opsional/manual |
| Day 3 | MCP + Vector Search | ⬜ Belum |
| Day 4 | Frontend Dashboard | ⬜ Belum |
| Day 5 | Demo Scenario + Remediation | ⬜ Belum |
| Day 6 | Deployment + Video Demo | ⬜ Belum |
| Day 7 | Dokumentasi + Submission | ⬜ Belum |

**Estimasi waktu per hari**: 10–12 jam (full-time commitment)

---

## Standar kematangan harian (wajib — hackathon-ready)

Ini **kontrak tim** untuk mempertahankan dan menaikkan peluang menang bukan sekadar cepat mencoret checklist: juri menilai **demo hidup, video ≤3 menit, dan repo**. Narasi MCP / Gemini yang «nanti baru kita luruskan» tetapi error dibiarkan memangkas kredibilitas Stage 2.

### Prinsip

- **Dilarang** menutup hari dengan pola «error dibuang dulu / nanti kita bahas»: error harus **diperbaiki** atau secara formal dicatat sebagai **blokir luar** bersama ETA dan fallback (**`docs/HACKATHON_BLOCKERS.md`** — bukan hanya percakapan chat).
- **Deliverables** dalam section hari Anda **belum boleh dianggap selesai** jika jalur utama masih gagal tes, gagal `./scripts/verify.sh`, gagal `./scripts/verify-full.sh` bila Anda mengubah konfigurasi frontend/Tailwind/Next secara relevan bagi build produksi, atau konsol demo merah tanpa blokir dokumentasi yang sah.

### Yang dilarang (jejak buruk bagi juri / teman satu tim)

| Pola tidak boleh | Mengapa membahayakan skor hackathon |
|------------------|--------------------------------------|
| Tes gagal atau sengaja `skip` / `xfail` agar cepat hijau padahal fitur dicentang Deliverable | Regres atau kebohongan di repo yang mudah dibongkar reviewer |
| `TODO` kritikal pada alur demo video tanpa issue + reschedule tertulis di hari berikutnya | Video tidak bisa nunjuk MCP multi-step / analisis Gemini dengan utuh |
| Merah konsol ESLint/pytest/console di jalur rekaman utama | Rekaman kedengaran «tidak kelar» sampai masa penilaian |
| `next build` / CI produksi frontend gagal sementara Anda mengaku UI/dashboard siap | Juri gagal men-deploy atau Anda kehilangan bukti konsistensi Vercel/Cloudflare |
| Mengklaim fitur Gemini/MCP «sudah selesai» padahal masih stub kosong | Langsung tembus kerentanan narasi Stage 2 & checklist anti-diskualifikasi |

### Gate keluar (tiap sore, sebelum pindah ke hari atau milestone berikutnya)

Gunakan secara mandiri bersama rekaman cepat apa pun yang Anda hasilkan sore itu:

- [ ] `./scripts/verify.sh` **hijau** — atau blokir dokumentasi sah + rencana perbaikan (**`docs/HACKATHON_BLOCKERS.md`**)
- [ ] Sebelum merge utama / rekaman Hari 6: `./scripts/verify-full.sh` juga **hijau** (termasuk **`next build`**), kecuali blokir yang sama di **`docs/HACKATHON_BLOCKERS.md`**
- [ ] Fitur utama yang kemarin bisa dijalankan **tetap bisa** dijalankan; ada regres maka dibenahkan hari ini atau dimasukkan ke **`docs/HACKATHON_BLOCKERS.md`** bersama ETA
- [ ] Tidak ada pemalsuan hijau tes (penyampingan tes tanpa blokir dokumentasi yang sah atau fix)
- [ ] Sesuatu yang bisa ditunjukkan ke juri hari itu **dibuktikan rekaman pendek atau catatan konkret satu paragraf** (cadangan luar biasa berguna bagi Hari 6)
- [ ] Cek cepat satu baris menghubungkan kemajuan Anda dengan salah satu unsur **Stage 2** dalam `docs/HACKATHON_QUALITY_BAR.md`

**Pedoman lengkap** (definisi matang harian / rubrik / rekaman fallback): **`docs/HACKATHON_QUALITY_BAR.md`**.

---

## Day 1 — Foundation & Architecture ✅

**Tanggal target**: 20 Mei 2026  
**Goal**: Project setup, GCP config, architecture finalized

### Pagi (4 jam)
- [x] Buat folder project `tessera` di `/Users/mac/Development/`
- [x] Setup struktur folder: `backend/`, `frontend/`, `docs/`, `scripts/`, `demo-app/`
- [ ] Buat Google Cloud project: `tessera-hackathon` (atau nama serupa)
- [ ] Enable APIs: Vertex AI, Cloud Run, Secret Manager, Cloud Build
- [ ] Setup billing ($100 hackathon credit + $300 free trial)
- [ ] Create service account + IAM roles
- [x] Create GitHub repo (public, MIT license)
- [x] Initial commit dengan timestamp proof (built from scratch)
- [x] LICENSE file + visible di About section (saat push ke GitHub)
- [ ] MongoDB Atlas: buat cluster M0 (free tier)
- [ ] Enable MongoDB Vector Search + buat search index
- [ ] Seed sample multi-tenant database + intentional violations:
  - [ ] Collection `orders` (tenant_id, customer_name, amount, created_at)
  - [ ] Collection `users` (tenant_id, email, role)
  - [ ] Collection `analytics_events` (tenant_id, event_type, metadata)

### Siang (4 jam)
- [x] Finalize system architecture (diagram di README / ARCHITECTURE.md)
- [x] Define agent workflow: Collect → Analyze → Detect → Report → Recommend
- [x] Design MongoDB query patterns yang akan di-audit
- [x] Plan vector embedding strategy
- [x] Setup Python venv + `requirements.txt`
- [x] Setup Next.js 14 + TailwindCSS + TypeScript
- [x] Create `.env.example`
- [x] Setup pre-commit hooks (black, flake8) — `.pre-commit-config.yaml` (mypy opsional belum)

### Malam (2–3 jam)
- [x] Build demo multi-tenant FastAPI app (subject untuk audit) — `demo-app/`
- [x] Endpoints dengan violations:
  - [x] `GET /orders` — missing tenant_id filter (CRITICAL)
  - [x] `GET /orders/{id}` — safe query
  - [x] `GET /analytics` — cross-tenant aggregation (HIGH)
  - [x] `GET /users` + `GET /reports/join` — pola tambahan MEDIUM/CRITICAL
- [x] Deploy demo app ke Cloud Run (opsional) — `demo-app/Dockerfile` siap; deploy manual Day 5/6

### Deliverables Day 1
- [x] Folder + struktur project lengkap
- [x] README, LICENSE, ARCHITECTURE, CONTRIBUTING
- [x] Backend skeleton (agent, analyzers, mcp, api)
- [x] Frontend skeleton (landing page)
- [x] Git repo + 2 commits
- [ ] GCP project configured — skrip: `scripts/infra/setup-gcp.sh`, panduan: `docs/INFRA_DAY1.md`
- [ ] MongoDB Atlas + sample data — seed: `scripts/seed_mongodb_demo.py`, index: `scripts/infra/atlas-vector-index.json`

---

## Day 2 — Core Agent Logic + Gemini Integration

**Tanggal target**: 21 Mei 2026  
**Goal**: Agent bisa menganalisis pola query dan (opsional) memperkaya output lewat Gemini

**Baseline repo terbaru:** motor aturan **`query_analyzer`**, **`profiler_ingest`**, **`prompt_templatan_violasi`** + **`skema_gemini_terstruktur`**, jalur Gemini JSON (`response_mime_type=application/json` bila SDK mendukung) + narasi fallback di **`gemini_opsional.py`**, kolom **`analisis_terstruktur_gemini`** di respons violation, **`langchain_lingkar_audit`**, dan **`pytest-cov`** untuk `app/analyzers` (≥80 %). **Belum otomatis di CI**: akses GCP Vertex menyentuh jaringan, serta **LangChain + Gemini sebagai LLM** pemilih alat multi-langkah.

### Pagi (4 jam)
- [x] ~~Setup Vertex AI API client~~ — jalur kode ada (`gemini_opsional.py` lazy `vertexai`); **credential + proyek GCP** Anda buktikan manual di luar `./scripts/verify.sh`
- [ ] Test Gemini 2.x dengan prompt Tessera — **uji manual/staging** (CI tidak memanggil Vertex)
- [x] ~~Buat prompt templates untuk violation types~~ — **`app/agent/prompt_templatan_violasi.py`**
- [x] ~~Keluaran terstruktur JSON pelanggaran~~ — **`KeluaranTambahanGeminiTerstruktur`** + `analisis_terstruktur_gemini` (bukan nama OpenAI «function calling» tetapi setara JSON-bound output)
- [x] ~~Parse pola dari jejak profiler MongoDB~~ — modul **`app/analyzers/profiler_ingest.py`**: `find` / `aggregate` dari field `command`
- [x] Ekstrak: pattern, collection, filters, aggregations — lewat ingest + `MongoDBQueryAnalyzer.analyze`
- [x] Identify missing `tenant_id` filters (heuristik tenant-scoped collections)
- [x] Detect cross-tenant `$lookup` / `$group` (heuristik)

### Siang (4 jam)
- [x] Implement 4 detection rules:
  - [x] Rule 1: Query tanpa tenant_id filter pada tenant-scoped collection
  - [x] Rule 2: Aggregation `$group` across tenants
  - [x] Rule 3: `$lookup` cross-tenant references
  - [x] Rule 4: Inconsistent tenant field names (tenant_id vs tenantId)
- [x] Severity scoring: critical / high / medium / low (`SEVERITY_PER_POLA` + puncak)
- [ ] Setup LangChain agent dengan Gemini as LLM — **belum** pada jalur `./scripts/verify.sh` (**pemasangan utama** ada di `requirements.txt`; audit production bisa menautkan model Vertex ke agent LC terpisah)
- [x] Define tools: `query_mongodb`, `analyze_query_pattern`, `search_similar_violations` — **parsial**: perkakas analisis pola nyata (`perkakas_analisis_query_tessera_tersebet`, `langchain_lingkar_audit.py`); panggilan MCP/`query_mongodb` stub; vector `search_similar` stub (Day 3)
- [x] ~~Implement ReACT loop: Thought → Action → Observation~~ — **varian deterministik offline**: `langkah_reka_lingkar_sederhana_tersebet` memanggil perkakas analisis bergantian (tanpa model bahasa pemilih alat di CI)

### Malam (2–3 jam)
- [x] Expand pytest: missing filter, safe query, cross-tenant aggregation, profiler ingest, API audit, agent
- [x] Manual test dengan sample queries dari demo app — `pola_query_audit.py`, `scripts/uji-audit-demo.sh`, `test_demo_app_pola_audit.py`
- [x] Connect `TesseraAgent.analyze_query()` ke Gemini (opsional, bukan stub wajib)
- [x] Connect `TesseraAgent.mulai_audit()` end-to-end minimal (API + contoh `queries`)

### Deliverables Day 2
- [x] Gemini integration **opsional** / siap Vertex (bukan hard dependency CI)
- [x] Query analyzer siap produksi **heuristik** (bukan proof formal)
- [x] Violation detection engine (4 rules)
- [ ] LangChain + **Gemini** sebagai LLM end-to-end di CI/produksi (opsional ke `requirements.txt` + konfigurasi Vertex)
- [x] Test coverage **≥80%** untuk `app/analyzers` — `pytest.ini` + `pytest-cov` di `requirements-verify.txt` (saat ini ~95% baris terukur)

---

## Day 3 — MongoDB MCP + Vector Search

**Tanggal target**: 22 Mei 2026  
**Goal**: Meaningful MCP integration + vector similarity search

### Pagi (4 jam)
- [ ] Install/configure MongoDB MCP server (`@modelcontextprotocol/server-mongodb`)
- [ ] Test MCP tools: query, find, aggregate
- [ ] Integrate MCP client ke Tessera agent (`app/mcp/client.py` — implementasi nyata)
- [ ] Setup Google Cloud Agent Builder (atau dokumentasi kenapa LangChain saja)
- [ ] Define agent flows: "Audit my database" → MCP → analyze → report
- [ ] Test via console / API

### Siang (4 jam)
- [ ] Vertex AI Text Embeddings untuk query patterns
- [ ] Store embeddings di MongoDB Atlas Vector Search index
- [ ] Implement `cari_pattern_serupa()` di `TesseraAgent`
- [ ] Populate knowledge base: 50+ synthetic violation patterns
  - [ ] E-commerce SaaS patterns
  - [ ] CRM SaaS patterns
  - [ ] Analytics platform patterns
- [ ] Setiap pattern: type, severity, remediation suggestion

### Malam (2–3 jam)
- [ ] Validasi MCP adalah core (bukan wrapper): multi-step MCP → analyze → MCP search
- [ ] Dokumentasi MCP flow di README + ARCHITECTURE
- [ ] Diagram agent ↔ MCP ↔ MongoDB
- [ ] Update `/health` endpoint: mongodb, gemini, mcp status real

### Deliverables Day 3
- [ ] MongoDB MCP integrated & working
- [ ] Vector Search + 50+ patterns di index
- [ ] Meaningful MCP orchestration terbukti di demo
- [ ] Agent Builder atau dokumentasi alternatif jelas

---

## Day 4 — Frontend Dashboard + Reporting

**Tanggal target**: 23 Mei 2026  
**Goal**: Professional UI untuk violations dan compliance reports

### Pagi (4 jam)
- [ ] Install shadcn/ui components (button, card, table, dialog, tabs)
- [ ] Layout: sidebar navigation (Dashboard, Audit, Violations, Reports)
- [ ] **Overview page**:
  - [ ] Total violations count
  - [ ] Severity breakdown (Critical / High / Medium)
  - [ ] Compliance score (0–100)
  - [ ] Trend chart (Recharts)

### Siang (4 jam)
- [ ] **Violations list**: table + filter severity/collection/date
- [ ] Detail modal per violation
- [ ] **Audit trigger page**:
  - [ ] Tombol "Start Database Audit"
  - [ ] Progress + agent thinking steps (SSE atau polling)
  - [ ] Agent activity log (MCP calls visible)
- [ ] Backend API routes:
  - [x] `POST /api/v1/audit/start` (**backend Day 2** — status/polling & violations list belum)
  - [ ] `GET /api/v1/audit/{id}/status`
  - [ ] `GET /api/v1/violations`
  - [ ] `GET /api/v1/report/{audit_id}`

### Malam (2–3 jam)
- [ ] **Compliance report page**:
  - [ ] Executive summary + risk score
  - [ ] SOC 2 / ISO 27001 mapping (contoh CC6.1)
  - [ ] Export PDF (jsPDF atau server-side) — nice-to-have
- [ ] Connect frontend ke backend (`lib/api.ts`)
- [ ] Dark mode polish + responsive mobile

### Deliverables Day 4
- [ ] Dashboard functional end-to-end
- [ ] Real-time audit UI (minimal polling)
- [ ] Compliance report view
- [ ] API integration tested

---

## Day 5 — Demo Scenario + Remediation + Tests

**Tanggal target**: 24 Mei 2026  
**Goal**: Compelling demo dengan 5 planted violations + auto-fix suggestions

### Pagi (4 jam)
- [ ] Finalize demo scenario: 3 tenants (Acme Corp, Globex, Initech)
- [ ] Plant 5 violations:
  - [ ] #1 Orders endpoint missing tenant_id (CRITICAL)
  - [ ] #2 Analytics cross-tenant aggregation (HIGH)
  - [ ] #3 Inconsistent field names tenant_id vs tenantId (MEDIUM)
  - [ ] #4 $lookup cross-tenant (CRITICAL)
  - [ ] #5 Missing compound index (MEDIUM)
- [ ] Seed MongoDB demo data konsisten dengan scenario

### Siang (4 jam)
- [ ] `generate_remediation()`: root cause, risk, code fix before/after
- [ ] Auto-generate pytest security tests per tenant boundary (10+ tests)
- [ ] Compliance dashboard: before 45/100 → after 92/100
- [ ] Remediation status tracking (detected → fixed → pending)

### Malam (2–3 jam)
- [ ] **Similar Violations** UI: Vector Search hasil top 3 similar cases
- [ ] End-to-end test: trigger audit → 5 violations → remediation → score
- [ ] Polish agent log messages untuk video demo

### Deliverables Day 5
- [ ] Demo app + DB siap untuk judges
- [ ] Remediation engine working
- [ ] Auto-generated tests
- [ ] Vector Search showcase di UI

---

## Day 6 — Deployment + Video Demo (3 menit)

**Tanggal target**: 25 Mei 2026  
**Goal**: Production URLs live + video submission-ready

### Pagi (4 jam)
- [ ] `Dockerfile` untuk FastAPI backend
- [ ] Deploy backend ke Cloud Run (min instances: 1, memory 2GB)
- [ ] Secrets di Secret Manager (MongoDB URI, API keys)
- [ ] Deploy frontend ke Vercel
- [ ] MongoDB Atlas: whitelist IPs Cloud Run + Vercel
- [ ] End-to-end test production URLs

### Siang + Malam (5–6 jam) — VIDEO
- [ ] Record screen 1080p (Loom/OBS)
- [ ] Script 3 menit EXACT:
  - [ ] 0:00–0:20 Hook + problem ($2M breach story)
  - [ ] 0:20–0:40 Solution intro (Gemini + Agent Builder + MongoDB)
  - [ ] 0:40–2:20 Live demo (audit → violations → fix → vector search)
  - [ ] 2:20–2:50 Impact + tech stack
  - [ ] 2:50–3:00 CTA (URL + GitHub)
- [ ] Voice-over Bahasa Inggris ATAU subtitle Inggris
- [ ] Edit: no copyrighted music, tight cuts
- [ ] Upload YouTube (Unlisted) — durasi ≤ 3:00

### Deliverables Day 6
- [ ] Hosted URL live 24/7 sampai judging selesai
- [ ] Video URL ready
- [ ] Production smoke test passed

---

## Day 7 — Dokumentasi + Submission (EARLY)

**Tanggal target**: 26 Mei 2026 (submit ~5 hari sebelum deadline)  
**Goal**: Devpost submitted + anti-disqualification checklist

### Pagi (4 jam)
- [ ] Polish README: Inspiration, How we built it, Challenges, Learnings
- [ ] Screenshots dashboard di README
- [ ] Demo GIF (LICEcap) — opsional
- [ ] `docs/API.md`, `docs/DEPLOYMENT.md` jika belum lengkap
- [ ] Code comments cleanup (Bahasa Indonesia untuk variabel baru)

### Siang (3 jam)
- [ ] Push ke GitHub public
- [ ] Verify license visible di About section
- [ ] Devpost form:
  - [ ] Title: Tessera - AI-Powered Multi-Tenant Data Isolation Auditor
  - [ ] Tagline + description
  - [ ] Demo URL
  - [ ] GitHub URL
  - [ ] Video URL
  - [ ] Track: **MongoDB**
  - [ ] Technologies checklist
- [ ] **SUBMIT** (~19.00 WIB recommended)

### Malam (2 jam)
- [ ] Pre-submission checklist (lihat bawah)
- [ ] Tweet / LinkedIn (tag @googlecloud @MongoDB) — opsional
- [ ] Screenshot konfirmasi submission

### Deliverables Day 7
- [ ] Devpost submitted EARLY
- [ ] All Stage 1 requirements verified
- [ ] Social proof started (opsional)

---

## Checklist Anti-Diskualifikasi (Stage 1)

Centang sebelum submit Devpost:

### Repo & License
- [ ] GitHub repo **public**
- [ ] MIT (atau OSI) license file ada
- [ ] License **visible** di GitHub About section (Settings → License)
- [ ] Repo created / commits setelah 5 Mei 2026
- [ ] Bukan fork project lama tanpa substantial change

### Hosted & Video
- [ ] Demo URL accessible tanpa login khusus (incognito test)
- [ ] App tetap online 22 Juni – 6 Juli 2026
- [ ] Video YouTube atau Vimeo, Public/Unlisted
- [ ] Durasi video **≤ 3:00** (hanya 3 menit pertama dinilai)
- [ ] Bahasa Inggris atau subtitle Inggris
- [ ] Tidak ada musik/konten berhak cipta ilegal

### Tech Stack (Wajib)
- [ ] **Gemini** digunakan (Vertex AI / AI Studio)
- [ ] **Google Cloud Agent Builder** digunakan (atau documented equivalent)
- [ ] **MongoDB MCP** meaningful (bukan sekadar CRUD)
- [ ] **TIDAK** pakai OpenAI, Claude, Mistral, dll.
- [ ] Agent multi-step autonomous (bukan chatbot saja)

### Submission Form
- [ ] Semua field Devpost mandatory terisi
- [ ] Track: MongoDB (satu track per submission)
- [ ] Platform: Web (minimal)

---

## Checklist Stage 2 (Scoring 25% masing-masing)

| Kriteria | Target | Checklist |
|----------|--------|-----------|
| **Tech Implementation** | Multi-step agent, MCP, Vector Search | [ ] Demo tunjukkan MCP calls + Gemini analysis + vector similar cases |
| **Design** | UX profesional | [ ] Dark mode, clear navigation, real-time audit UX |
| **Potential Impact** | Terukur | [ ] "$500K–$2M prevented", "45→92 compliance score", "40h→2h audit time" |
| **Idea Quality** | Novel | [ ] README + video emphasize: no existing runtime isolation auditor |

---

## Buffer & Risk Mitigation

| Risk | Mitigasi |
|------|----------|
| Vector Search stuck | Fallback rule-based similarity; tetap dokumentasikan learning path |
| Agent Builder complex | LangChain + dokumentasi; jelaskan di README |
| Video gagal record | Backup screen recording dari Day 5 testing |
| Deployment down saat judging | Cloud Run min instances = 1; test weekly |
| GCP credit habis | Monitor billing; pakai M0 MongoDB free tier |

---

## Quick Commands Reference

```bash
# Setup
cd /Users/mac/Development/tessera
./scripts/setup-dev.sh

# Backend
cd backend && source venv/bin/activate
uvicorn app.api.main:app --reload

# Frontend
cd frontend && npm run dev

# Verifikasi (lint + tes + Cursor rules minimal)
./scripts/verify.sh

# Verifikasi berlapis penuh lokal (= mirip CI): compileall backend + npm run build
./scripts/verify-full.sh

# Tes backend saja (dari akar backend dengan pytest.ini mengarahkan ke tests/)
cd backend && pytest -v

# Git
git add . && git commit -m "feat: deskripsi"
git push origin main
```

---

## Kontak & Resources

- **Hackathon**: https://rapid-agent.devpost.com
- **Support**: support@devpost.com
- **Agent Starter Pack**: https://github.com/GoogleCloudPlatform/agent-starter-pack
- **MongoDB MCP**: https://github.com/modelcontextprotocol/servers/tree/main/src/mongodb
- **Plan detail**: `.cursor/plans/` atau `docs/DAY1_PROGRESS.md`
- **Standar kematangan + rubrik**: [docs/HACKATHON_QUALITY_BAR.md](docs/HACKATHON_QUALITY_BAR.md), blokir dokumentasi sah: [docs/HACKATHON_BLOCKERS.md](docs/HACKATHON_BLOCKERS.md)

---

*Last updated: 21 Mei 2026 — Day 1 sisa repo: demo-app, seed Atlas, infra GCP/Atlas, pre-commit, uji pola demo*
