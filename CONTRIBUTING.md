# Contributing to Tessera

Terima kasih atas minat Anda untuk berkontribusi pada Tessera! Kami menyambut kontribusi dari komunitas.

## Cara Berkontribusi

### Melaporkan Bugs

Jika Anda menemukan bug, silakan buat GitHub Issue dengan informasi:
- Deskripsi bug yang jelas
- Steps to reproduce
- Expected behavior vs actual behavior
- Environment (OS, Python version, Node version)
- Screenshots jika applicable

### Mengusulkan Features

Untuk feature requests, buat GitHub Issue dengan:
- Clear description dari feature yang diusulkan
- Use cases dan motivasi
- Potential implementation approach

### Pull Requests

1. Fork repository
2. Create feature branch: `git checkout -b feature/nama-feature`
3. Commit changes dengan message yang descriptive
4. Push ke branch: `git push origin feature/nama-feature`
5. Buat Pull Request ke `main` branch

### Keseriusan kematangan (tim hackathon)

Kami menghindari pola «skip error untuk dibahas lain waktu»: setiap Deliverable utama harian **dibenangkan**, **dibuktikan dengan tes/smoke**, atau **diklaim sebagai blokir luar** secara terbuka di **`docs/HACKATHON_BLOCKERS.md`**. Ikuti **`docs/HACKATHON_QUALITY_BAR.md`** dan **Gate keluar** di **`docs/TODOLIST-7-HARI.md`**.

### Coding Standards

**Python (Backend)**:
- Follow PEP 8 style guide
- Gunakan type hints untuk semua functions
- Variabel baru: Bahasa Indonesia dengan snake_case
- Komentar: Bahasa Indonesia yang natural
- Run `black` dan `flake8` sebelum commit

**TypeScript (Frontend)**:
- Follow Airbnb style guide
- Variabel baru: Bahasa Indonesia dengan camelCase
- Komentar: Bahasa Indonesia
- Run `npm run lint` sebelum commit

### Testing

- Semua fitur baru sebaiknya punya tes yang relevan (lihat konsensus tim untuk batas minimal).
- Sebelum membuka atau memperbarui PR, jalankan dari **akar repo**:

  ```bash
  ./scripts/verify.sh
  ```

  Sebelum merge PR besar atau rekaman hackathon utama, jalankan jalur lebih berlapis (**`compileall`** backend dan **Next production build**):

  ```bash
  ./scripts/verify-full.sh
  ```

  Setara pemanggilan: `npm run verify:full` lewat **`package.json` tipis di akar** repository.

- Cabang Anda pada push/PR diperiksa ulang secara otomatis oleh **`.github/workflows/ci.yml`**; sebaiknya lulus secara lokal dulu agar hemat waktu reviewer.
- Butuh panduan lebih lengkap atau langkah manual? Lihat **`docs/VERIFY.md`**.
- Untuk alur **Implementasi → Verifikasi → QA** di Cursor (kode teruji sebelum merge): **`AGENTS.md`** dan **`docs/AGENT_PIPELINE.md`**.

### Commit Messages

Format: `<type>: <subject>`

Types:
- `feat`: Feature baru
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `style`: Code style changes (formatting)

Contoh:
```
feat: tambah vector search untuk pattern matching
fix: perbaiki detection missing tenant_id di nested queries
docs: update README dengan deployment instructions
```

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Frontend
```bash
cd frontend
npm install
```

### Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

## Architecture

Lihat [ARCHITECTURE.md](docs/ARCHITECTURE.md) untuk understanding sistem design.

## Questions?

Buka GitHub Discussion atau mention di Issues.

## License

Dengan berkontribusi, Anda setuju bahwa kontribusi Anda akan dilicense under MIT License.
