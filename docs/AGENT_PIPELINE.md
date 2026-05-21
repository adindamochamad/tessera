# Pipeline agent Tessera (Implementasi → Verifikasi → QA)

Panduan ini melengkapi **`AGENTS.md`** di akar repo. Gunakan pipeline ini setiap kali Anda ingin kode **benar-benar teruji** dan mendekati **production-ready**, bukan hanya «terlihat jadi» di editor.

## Mengapa tiga agent?

| Masalah satu agent | Solusi terpisah |
|--------------------|-----------------|
| Mengabaikan tes setelah implementasi | **Verifikasi** wajib menjalankan `verify.sh` / `verify-full.sh` |
| «Hijau» hanya lint, jalur demo masih rusak | **QA** mengecek smoke, regres, dan rubrik demo |
| Scope melebar tanpa kriteria | **Prompt matang** mengunci deliverable dan kriteria penerimaan |

## Langkah cepat

1. Salin `.cursor/prompts/implementasi-matang.md` ke chat Cursor Agent.
2. Isi bagian **TUGAS**, **KRITERIA PENERIMAAN**, dan **AREA REPO**.
3. Setelah selesai, jalankan agent Verifikasi (`@tessera-verifikasi` atau chat baru + handoff).
4. Jika PASS, jalankan agent QA (`@tessera-qa`).
5. Merge / rekaman demo hanya setelah QA **SIAP**.

## Piramida verifikasi (sinkron dengan skrip)

| Lapisan | Agent yang bertanggung jawab |
|---------|------------------------------|
| pytest + cov analyzers | Verifikasi |
| lint + type-check frontend | Verifikasi |
| compileall + `npm run build` | Verifikasi (scope PR utama / frontend build) |
| curl `/health`, `npm run dev`, konsol browser | QA |
| Kesesuaian TODOLIST / blokir dokumentasi | QA |

Lihat tabel lengkap di `docs/VERIFY.md`.

## Kapan `verify-full` wajib?

- Perubahan di `frontend/` yang mempengaruhi build produksi
- Menutup **Gate keluar** hari di `docs/TODOLIST-7-HARI.md`
- Sebelum PR utama atau rekaman video hackathon

## Blokir luar

Jika GCP/Atlas/MCP sungguhan tidak bisa diuji, agent **Verifikasi** atau **QA** harus meminta entri di `docs/HACKATHON_BLOCKERS.md` — bukan menutup dengan FAIL tanpa jejak atau PASS palsu.

## Troubleshooting

| Gejala | Tindakan |
|--------|----------|
| Agent implementasi tidak menulis tes | Ulangi dengan kriteria «tes wajib untuk perilaku baru» di prompt |
| `verify.sh` gagal di mesin Anda | Agent Verifikasi wajib memperbaiki atau melaporkan error spesifik |
| QA FAIL pada smoke manual | Dokumentasikan langkah reproduksi; kembali ke Implementasi |
| Skill tidak terdeteksi | Pastikan folder `.cursor/skills/tessera-*/SKILL.md` ada; sebut `@tessera-implementasi` eksplisit |

## Referensi

- `AGENTS.md` — ringkasan peran dan perintah Cursor
- `docs/HACKATHON_QUALITY_BAR.md` — definisi hari matang
- `docs/HACKATHON_BLOCKERS.md` — blokir resmi
- `CONTRIBUTING.md` — penamaan dan standar PR
