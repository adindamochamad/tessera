#!/usr/bin/env bash
# Skrip verifikasi otomatis Tessera — jalankan dari root repository.
set -euo pipefail

# Direktori root project (orang tua dari scripts/)
akar_proyek="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${akar_proyek}"

gagal=0

# --- 1) Cursor rules ---
echo "[verify] Cursor rules..."
if [[ ! -d ".cursor/rules" ]]; then
  echo "GAGAL: folder .cursor/rules tidak ada"
  exit 1
fi
jumlah_rules=$(find .cursor/rules -name "*.mdc" -type f 2>/dev/null | wc -l | tr -d ' ')
if [[ "${jumlah_rules}" -eq 0 ]]; then
  echo "GAGAL: tidak ada file .mdc di .cursor/rules"
  exit 1
fi
echo "      OK (${jumlah_rules} file rule .mdc)"

# --- 1b) Pipeline agent (skills + AGENTS.md) ---
echo "[verify] Pipeline agent..."
if [[ ! -f "AGENTS.md" ]]; then
  echo "GAGAL: AGENTS.md tidak ada (pipeline Implementasi→Verifikasi→QA)"
  exit 1
fi
for skill_wajib in tessera-implementasi tessera-verifikasi tessera-qa; do
  if [[ ! -f ".cursor/skills/${skill_wajib}/SKILL.md" ]]; then
    echo "GAGAL: skill .cursor/skills/${skill_wajib}/SKILL.md tidak ada"
    exit 1
  fi
done
echo "      OK (AGENTS.md + 3 skill pipeline)"

# --- 2) Backend: pytest ---
# PYTHONPATH mengarah ke folder backend supaya paket app.* bisa di-import.
echo "[verify] Backend (pytest)..."

export PYTHONPATH="${akar_proyek}/backend"
pushd "${akar_proyek}/backend" >/dev/null

pilih_python_untuk_pytest=""
if [[ -f "venv/bin/python" ]] && ./venv/bin/python -c "import pytest" 2>/dev/null; then
  pilih_python_untuk_pytest="./venv/bin/python"
  echo "      memakai backend/venv (pytest sudah terpasang)"
elif python3 -c "import pytest" 2>/dev/null; then
  pilih_python_untuk_pytest="python3"
  echo "      memakai python sistem (disarankan Python 3.11+ untuk full requirements.txt)"
elif [[ ! -d "venv" ]]; then
  echo "      membuat backend/venv + pip install requirements-verify.txt (hanya tes) ..."
  python3 -m venv venv
  ./venv/bin/python -m pip install -q -r requirements-verify.txt
  pilih_python_untuk_pytest="./venv/bin/python"
else
  echo "      pytest tidak ada; memasang requirements-verify.txt ke backend/venv ..."
  ./venv/bin/python -m pip install -q -r requirements-verify.txt
  pilih_python_untuk_pytest="./venv/bin/python"
fi

if ! "${pilih_python_untuk_pytest}" -m pytest -q; then
  echo "GAGAL: pytest backend"
  gagal=1
fi
popd >/dev/null

# --- 3) Frontend ---
echo "[verify] Frontend..."
pushd frontend >/dev/null
if [[ ! -d "node_modules" ]]; then
  echo "LEWATI frontend: jalankan npm install di folder frontend lebih dulu."
  gagal=1
else
  if ! npm run lint; then
    echo "GAGAL: npm run lint"
    gagal=1
  fi
  if ! npm run type-check; then
    echo "GAGAL: npm run type-check"
    gagal=1
  fi
fi
popd >/dev/null

if [[ "${gagal}" -ne 0 ]]; then
  echo ""
  echo "Ringkasan: ada pemeriksaan yang gagal. Lihat pesan di atas dan docs/VERIFY.md."
  exit 1
fi

echo ""
echo "Semua pemeriksaan otomatis lulus."
