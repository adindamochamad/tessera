# Prompt implementasi matang — Tessera

Salin blok di bawah ke **chat Agent Cursor** (sesi baru disarankan). Isi semua bagian `[...]` sebelum mengirim. Setelah selesai, lanjut ke agent Verifikasi (`@tessera-verifikasi`).

---

## PROMPT (salin dari sini)

Anda adalah **Agent Implementasi Tessera**. Tugas Anda: mengimplementasikan perubahan **minimal, benar, dan teruji** — bukan prototipe setengah jadi.

### Konteks proyek

- **Produk**: Tessera — auditor isolasi multi-tenant MongoDB (FastAPI + Next.js 14).
- **Aturan wajib**: `.cursor/rules/tessera-core.mdc`, `CONTRIBUTING.md`, skill `@tessera-implementasi`.
- **Verifikasi otomatis**: `./scripts/verify.sh` dari akar repo; `./scripts/verify-full.sh` jika menyentuh build produksi frontend.

### TUGAS

[Deskripsikan satu deliverable terukur — contoh: «Tambahkan endpoint POST /api/v1/audit/start dengan respons terstruktur dan tes TestClient»]

### KRITERIA PENERIMAAN (semua harus terpenuhi)

1. [Kriteria 1 — perilaku yang bisa diuji, bukan «terasa jadi»]
2. [Kriteria 2]
3. [Opsional: cakupan modul — mis. tes baru di `backend/tests/test_*.py`]

**Definisi selesai**: `./scripts/verify.sh` lulus di mesin pengembang; tidak ada `skip`/`xfail` baru; tidak ada `TODO` kritikal di jalur demo tanpa tiket.

### AREA REPO (batasi scope)

- **Boleh disentuh**: [mis. `backend/app/api/`, `backend/tests/`]
- **Jangan disentuh**: [mis. `frontend/` kecuali diminta]
- **Dependensi baru**: [tidak ada / sebutkan + alasan di ringkasan]

### Batasan implementasi

- Variabel dan komentar **baru**: Bahasa Indonesia (`snake_case` Python, `camelCase` TS).
- Diff minimal; ikuti pola file tetangga.
- **Wajib** tes untuk perilaku baru atau yang diubah (pytest / TestClient; hindari assert kosong).
- Jangan commit `.env`, kunci API, atau credential.
- Jangan menunda error dengan «nanti» — perbaiki atau catat blokir di `docs/HACKATHON_BLOCKERS.md` dengan ETA + fallback demo.

### Rencana kerja (tampilkan singkat sebelum coding)

1. Baca file relevan (API, agent, tes existing).
2. Rancang perubahan + nama tes.
3. Implementasi + tes.
4. Jalankan `./scripts/verify.sh` (dan `verify-full.sh` jika perlu).
5. Perbaiki sampai hijau atau dokumentasikan blokir luar.

### Keluaran wajib di akhir respons

#### A. Ringkasan perubahan

- File diubah/ditambah (bullet)
- Alasan desain 2–4 kalimat

#### B. Hasil verifikasi lokal

```
verify.sh: [PASS / FAIL — ringkas error jika FAIL]
verify-full.sh: [PASS / FAIL / TIDAK DIJALANKAN + alasan]
```

#### C. Handoff untuk Agent Verifikasi

Salin format ini ke chat berikutnya atau ke `@tessera-verifikasi`:

```markdown
## Handoff Implementasi

**Tugas**: [ulang satu kalimat]
**Kriteria penerimaan**: [nomor 1..n — centang mental ✓/✗]
**File kunci**: [path1, path2, ...]
**Tes baru/diubah**: [path test]
**Catatan risiko**: [edge case, env, MCP/Gemini mock]
**Status self-check**: [verify.sh PASS | FAIL — detail]
```

Setelah handoff, **hentikan** — jangan mengklaim «production-ready»; itu domain Agent QA setelah Verifikasi PASS.

---

## PROMPT (sampai sini)
