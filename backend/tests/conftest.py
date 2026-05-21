"""Test configuration — tetapkan variabel lingkungan minimal sebelum impor aplikasi Tessera."""

import os
from pathlib import Path

# Wajib sebelum apa pun membaca Settings() agar tes ringan bisa jalan di CI tanpa .env Anda.
_MINIMAL_SEMUA_BAGI_CI = {
    "GOOGLE_CLOUD_PROJECT": "tessera-ringan-pemeriksaan-unit",
    "GOOGLE_APPLICATION_CREDENTIALS": "/tmp/tessera-pemeriksaan-tidakenyata.json",
    "MONGODB_URI": "mongodb://127.0.0.1:27017",
    "MONGODB_DATABASE": "tessera_mini_uji_bukan_produksi",
    "JWT_SECRET": "jwt-rahasia-simbol-pemeriksaan-minimal-dua-dua-dua-dua-dua-dua-dua-dua-dua-dua-dua-dua-dua-dua-dua-dua",
    "ENABLE_GEMINI_ANALYSIS": "false",
}
for nama_kunci_mikro, nilai_simpel_tersebet in _MINIMAL_SEMUA_BAGI_CI.items():
    os.environ.setdefault(nama_kunci_mikro, nilai_simpel_tersebet)

import pytest
import sys

backend_path_utama_tersebet = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path_utama_tersebet))
