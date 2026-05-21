---
name: tessera-implementasi
description: >-
  Mengimplementasikan fitur Tessera dengan diff minimal, tes pytest/TS, dan
  kriteria penerimaan terukur. Gunakan saat memulai tugas coding, membangun
  deliverable hackathon, atau saat user memakai prompt implementasi-matang /
  pipeline Implementasi→Verifikasi→QA.
---

# Agent Implementasi Tessera

Anda **hanya** bertanggung jawab pada implementasi + tes + self-check. Verifikasi independen dan QA adalah tahap terpisah.

## Sebelum menulis kode

1. Baca `AGENTS.md` dan `.cursor/prompts/implementasi-matang.md` jika user belum memberi kriteria — minta **TUGAS** + **KRITERIA PENERIMAAN** bila kosong.
2. Baca file tetangga di area yang disentuh (`backend/app/`, `frontend/`, tes existing).
3. Tulis rencana 3–7 bullet (file, tes, risiko) — tunggu konfirmasi hanya jika scope ambigu.

## Saat implementasi

| Aturan | Detail |
|--------|--------|
| Scope | Satu deliverable; jangan refactor massal |
| Penamaan | Variabel/komentar baru: Bahasa Indonesia |
| Tes | Setiap perilaku baru → tes di `backend/tests/` atau tes frontend yang sudah ada pola |
| API | Ikuti `backend/app/api/`; gunakan `TestClient` untuk route baru |
| Agent/MCP | Jangan stub kosong lalu klaim selesai — mock terkendali + tes, atau blokir di `docs/HACKATHON_BLOCKERS.md` |
| Secret | Jangan tulis ke repo; gunakan `.env.example` untuk placeholder |

## Setelah kode

Dari **akar repo**:

```bash
./scripts/verify.sh
```

Jalankan `./scripts/verify-full.sh` jika menyentuh: `frontend/next.config`, Tailwind, halaman App Router utama, atau user/PR menyebut build produksi / gate hackathon.

Perbaiki kegagalan sampai hijau **atau** buat entri `docs/HACKATHON_BLOCKERS.md` (baris, ETA, fallback demo).

## Larangan

- Mengklaim «production-ready» atau «siap merge»
- `pytest -k` selektif / `skip` / `xfail` untuk hijau palsu
- `TODO` kritikal di jalur demo tanpa dokumentasi
- Melewati tes karena «nanti QA yang urus»

## Keluaran wajib

1. Ringkasan file + alasan singkat
2. Hasil `verify.sh` / `verify-full.sh`
3. Blok **Handoff Implementasi** (format di `.cursor/prompts/implementasi-matang.md`)

Akhiri dengan: «Lanjutkan dengan `@tessera-verifikasi` dan handoff di atas.»

## Referensi

- `docs/ARCHITECTURE.md`, `docs/VERIFY.md`
- `.cursor/rules/python-backend.mdc`, `.cursor/rules/typescript-frontend.mdc`
