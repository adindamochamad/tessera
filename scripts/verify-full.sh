#!/usr/bin/env bash
# Verifikasi berlapis maksimal di mesin pengembang tanpa MCP/Gemini/DB sungguhan.
# Menjalankan verify.sh kemudian compileall backend + npm run build frontend.
set -euo pipefail

akar_proyek="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Tessera verify-full (lint + tes + sintaks backend + Next build produksi) ==="

bash "${akar_proyek}/scripts/verify.sh"

echo ""
echo "[verify-full] Backend: compileall (cek sintaks modul)..."

export PYTHONPATH="${akar_proyek}/backend"
perintah_py="python3"
if [[ -x "${akar_proyek}/backend/venv/bin/python" ]]; then
  perintah_py="${akar_proyek}/backend/venv/bin/python"
fi
"${perintah_py}" -m compileall -q "${akar_proyek}/backend/app"

echo "[verify-full] Frontend: npm run build (cek bundel produksi)..."
pushd "${akar_proyek}/frontend" >/dev/null
if [[ ! -d node_modules ]]; then
  echo "GAGAL: jalankan npm install di folder frontend dahulu." >&2
  exit 1
fi
npm run build
popd >/dev/null

echo ""
echo "Seluruh lapisan verify-full lulus."
