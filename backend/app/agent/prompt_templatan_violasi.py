"""
Templatan prompt Gemini untuk isolasi penyewaan — Bahasa Indonesia, siap gabung konteks Tessera.

Dipakai oleh `gemini_opsional.py` ketika keluaran JSON terstruktur diaktifkan.
"""

from __future__ import annotations

import json
from typing import Any, Dict


def dapatkan_instruksi_sistem_tersebet() -> str:
    """Peran sistem singkat bagi model Gemini Vertex."""
    return (
        "Anda adalah pembantu auditor keamanan data SaaS multi-tenant di proyek Tessera. "
        "Jangan mengarang detail operasional konkret atau menyebut data nyata konsumen tenant. "
        "Jawab hanya satu objek JSON yang mematuhi bidang eksak yang diminta massukan pemakai;"
        " hindari pembungkus Markdown atau teks di luar JSON."
    )


def gambarkan_skema_bidang_json_tersebet() -> str:
    """Ringkaskan nama bidang agar mudah menyalin ke Vertex response JSON."""
    return (
        '{"ringkasan_eksekutif": "string Bahasa Indonesia", '
        '"penyebab_mendalam": "string", '
        '"dampak_umum": "string", '
        '"saran_prioritas": ["string", ...], '
        '"kepercayaan_0_hingga_100": angka_integer_0_sampai_100}'
    )


def bangun_massukan_terstruktur_violasi_tersebet(
    nama_polanya_tessera_tersebet: str,
    tingkat_severity_tersebet: str,
    ringkasan_aturan_tessera_tuple_tersebet: tuple[str, str, str],
    potongan_query_terserial_tersebet: str,
    nama_koleksi_tersebet: str,
    nama_basis_data_logis_tersebet: str = "",
) -> str:
    """
    Satukan fakta Tessera menjadi satu blok massukan aman bagi generate_content Vertex.
    """
    desk_tersebet, akar_tersebet, dampak_tersebet = ringkasan_aturan_tessera_tuple_tersebet
    konteks_tambahan: Dict[str, Any] = {
        "nama_polanya_detektor": nama_polanya_tessera_tersebet,
        "severity_aturan_tessera": tingkat_severity_tersebet,
        "nama_koleksi": nama_koleksi_tersebet,
        "basis_data_catatan_auditor": nama_basis_data_logis_tersebet,
        "tessera_ringkasan_aturan": desk_tersebet,
        "tessera_root_cause_aturan": akar_tersebet,
        "tessera_dampak_aturan": dampak_tersebet,
        "cuplikan_query_terserial": potongan_query_terserial_tersebet[:6000],
    }
    blok_konteks = json.dumps(konteks_tambahan, ensure_ascii=False, indent=2)
    cetak_skema = gambarkan_skema_bidang_json_tersebet()
    return (
        "Sesuaikan analisis Anda dengan fakta struktural Tessera berikut (JSON konteks).\n\n"
        f"{blok_konteks}\n\n"
        f"Keluarannya WAJIB berupa satu objek JSON sah dengan tepat bidang berikut tanpa kata lain:\n{cetak_skema}\n\n"
        "Aturan bahasa: Bahasa Indonesia alami untuk semua teks bernilai string; minimal satu butir dalam "
        "`saran_prioritas`; `kepercayaan_0_hingga_100` sebagai estimasi Anda terhadap kejelasan pola."
    )
