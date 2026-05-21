# Panduan kematangan harian (peluang hackathon Tessera)

Dokumen ini melengkapi `docs/TODOLIST-7-HARI.md`. Tujuannya: **hari demi hari menghasilkan kondisi repo dan demo yang mempertahankan atau menaikkan peluang menang**, tanpa pola «error dibuang dulu / nanti saja».

## Kenapa tidak boleh meninggalkan error lalu dibahas nanti

- **Submission dinilai lewat demo + video + publik repo**. Log merah di konsol, tes yang gagal, atau MCP yang sekadar kosong cepat meninggalkan kesan aplikasi tidak selesai.
- **Stage 2** menghargai teknik konsisten (**agent multi-step**, **MCP bermakna**, **Vector Search**). Setiap blok yang disengaja kosong menghapus salah satu kartu pembicaraan di video Anda.
- **Buffer waktu Anda terbatas**. Hutang teknik bertumbuh cepat mendekati deadline puncak submission: menunda error sering menghabiskan slot krusial.

## Definisi “hari sudah matang” (minimal)

Sebelum Anda pindah fokus ke hari kalender atau milestone berikutnya di TODOLIST:

1. **Skrip pemeriksaan dasar dari root repo**:

   ```bash
   ./scripts/verify.sh
   ```

   Wajib **hijau** untuk perubahan di branch kerja Anda. Jika gagal dengan alasan blokir luar (lihat di bawah), catat blokir secara formal.

   **Sebelum merge besar atau rekaman utama**: jalankan `./scripts/verify-full.sh` (bundel `compileall` + **`npm run build`**) juga; konsultasikan `docs/VERIFY.md` bagi piramida lengkap serta CI `.github/workflows/ci.yml`.

2. **Dilarang menyembunyikan atau menunda kegagalan tanpa jejak dokumentasi**:

   Anda tidak boleh menutup hari itu dengan pola berikut untuk **alur yang sudah Anda klaim sebagai deliverable**:

   - Tes gagal tetapi dijadwalkan besok tanpa blokir dokumentasi atau fix.
   - `TODO` kritikal pada jalur demo tanpa Tiket/issue dan tanpa reschedule eksplisit ke hari berikutnya dalam TODOLIST.
   - Mematikan tes / `skip` / `pytest -k` selektif hanya untuk “hijau palsu”.

   Jeda sementara hanya bisa diterima bila Anda **belum** mencentang Deliverable tersebut di TODOLIST.

3. **Regres tidak diterima sebagai “hari matang partially”**:

   Sesuatu yang bisa dijalankan kemarin tetap bisa dijalankan hari ini, kecuali perubahan sengaja didokumentasikan (breaking change bersama cara migrasinya dalam komit/teks dokumentasi).

4. **Satu artefak narasi**:

   Rekam **layar pendek** (bahkan satu menit!) yang menunjukkan apa berhasil hari tersebut. Ini berguna sekali sebagai fallback jika Rekaman Hari 6 gagal mendadak.

## Blokir di luar kontrol Anda (GCP, Atlas, internet)

**Boleh** mempengaruhi kemampuan Anda menutup item hari tersebut, tetapi **tidak boleh** menghilangkan jejak dokumentasi yang jelas.

Gunakan **`docs/HACKATHON_BLOCKERS.md`**:

- Baris apa yang terblok;
- Kemungkinan selesai;
- Fallback yang tetap bisa ditunjukkan ke juri (misalnya video berbasis rekaman Hari sebelumnya, atau dokumentasi MCP yang konkret bersama rekaman konsol MCP).

Tanpa itu, blokir Anda tidak dapat dibedakan dari malas menyudahi pekerjaan — untuk partner tim itu merugikan morale.

## Rujukan rubrik (Stage 2)

| Rubrik Stage 2 | Pertanyaan cepat menjelang Anda menutup hari |
|----------------|------------------------------------------------|
| **Tech** | Bisakah saya menjelaskan alur MCP → Gemini → penyimpanan/vector dalam satu rekaman bersih tanpa melewati error? |
| **Design** | Apakah alur utama pengguna bisa disentuh walau baru versi MVP? |
| **Impact** | Apakah metrik seperti skor atau angka hemat waktu bisa dihasilkan konsisten atau dijelaskan jujur tanpa gimmick palsu? |
| **Ide** | README dan demo masih konsisten menyatakan “runtime isolation audit”? |

Sesuaikan isi Hari dengan checklist **Stage 1 + Stage 2** di akhir `TODOLIST-7-HARI.md`.
