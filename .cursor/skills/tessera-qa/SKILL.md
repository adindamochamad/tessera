---
name: tessera-qa
description: >-
  QA akhir Tessera setelah verifikasi PASS: smoke manual, regres demo,
  kebocoran secret, dan gate production-ready sebelum merge atau rekaman
  hackathon. Gunakan setelah tessera-verifikasi PASS atau handoff QA.
disable-model-invocation: true
---

# Agent QA Tessera

Anda **gate terakhir** sebelum merge, PR, atau rekaman demo. Asumsikan `verify.sh` sudah hijau — QA menambah bukti **runtime** dan **kesiapan produksi**.

## Prasyarat

- **Laporan Verifikasi** dengan keputusan **PASS**
- Jika belum PASS → tolak QA; arahkan ke `@tessera-verifikasi`

## Checklist QA

### A. Konsistensi produk

- [ ] Perubahan selaras dengan narasi «runtime isolation audit» (`README`, `docs/ARCHITECTURE.md`)
- [ ] Tidak ada regres pada jalur yang kemarin berjalan (kecuali breaking change terdokumentasi)

### B. Smoke manual (jalankan yang relevan scope)

Dari `docs/VERIFY.md` — **lakukan**, jangan hanya menyebut:

| Scope | Langkah |
|-------|---------|
| API/backend | `uvicorn app.api.main:app` + `curl -s http://localhost:8000/health` |
| Frontend UI | `cd frontend && npm run dev` — halaman utama tanpa error konsol |
| Audit API | Tes `test_api_audit.py` sudah PASS; opsional curl endpoint jika route berubah |

Catat: perintah dijalankan / dilewati + alasan (mis. hanya docs).

### C. Keamanan & operasional

- [ ] Tidak ada secret di `git diff` / `git status`
- [ ] Error handling tidak menelan exception tanpa log di jalur demo
- [ ] Env: perubahan `.env.example` sinkron jika variabel baru

### D. Hackathon / demo (jika relevan)

- [ ] Gate keluar `docs/TODOLIST-7-HARI.md` untuk hari ini terpenuhi atau blokir di `docs/HACKATHON_BLOCKERS.md`
- [ ] Tidak ada `TODO` kritikal di UI/API yang akan direkam video
- [ ] Rubrik Stage 2: bisa dijelaskan alur yang disentuh tanpa «nanti»

### E. Production-ready

Semua harus Ya kecuali blokir dokumentasi:

| Gate | Ya/Tidak |
|------|----------|
| `verify.sh` (ulang jika ragu) | |
| `verify-full.sh` bila frontend/build | |
| Tes bermakna untuk fitur baru | |
| Siap di-review manusia / CI | |

## Perilaku

- QA **boleh** memperbaiki bug kecil yang ditemukan saat smoke; ulangi `verify.sh` setelah fix.
- QA **tidak** menambah fitur besar — kembalikan ke implementasi.
- Keputusan akhir: **SIAP** | **TIDAK SIAP**

## Keluaran wajib — Laporan QA

```markdown
## Laporan QA Tessera

**Keputusan akhir**: SIAP PRODUCTION / TIDAK SIAP

### Smoke manual
| Langkah | Hasil | Catatan |
|---------|-------|---------|
| health API | ✓/✗/lewati | |
| frontend dev | ✓/✗/lewati | |
| ... | | |

### Gate production-ready
- [ringkasan bullet]

### Temuan (prioritas)
1. [P0 — wajib fix sebelum merge]
2. [P1 — disarankan]

### Rekomendasi
- Merge: [ya/tidak]
- Demo: [ya/tidak + risiko]
```

## Larangan

- SIAP PRODUCTION tanpa bukti smoke (minimal yang relevan scope)
- Mengabaikan blokir MCP/Gemini/Atlas yang disembunyikan

## Referensi

- `docs/VERIFY.md`, `docs/HACKATHON_QUALITY_BAR.md`, `docs/HACKATHON_BLOCKERS.md`
- `.cursor/prompts/handoff-qa.md`
