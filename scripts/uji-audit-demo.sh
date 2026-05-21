#!/usr/bin/env bash
# Uji manual Day 2: audit pola dari demo-app via API Tessera.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
API_URL="${TESSERA_API_URL:-http://localhost:8000}"

cd "${ROOT}"
PYTHONPATH="${ROOT}/backend:${ROOT}/demo-app" python3 - <<'PY'
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("demo-app").resolve()))
from pola_query_audit import DAFTAR_POLA_DEMO

print(json.dumps({"nama_database": "tessera_demo", "queries": DAFTAR_POLA_DEMO}))
PY
| curl -sS -X POST "${API_URL}/api/v1/audit/start" \
    -H "Content-Type: application/json" \
    -d @- | python3 -m json.tool

echo ""
echo "Selesai — pastikan backend Tessera berjalan di ${API_URL}"
