"""
Panggilan Vertex Gemini secara bertingkat-flag.

Vertex dan google-cloud-aiplatform hanya diimpor secara lazy ketika fungsi dipanggil
agar lingkungan verifikasi ringan tidak wajib memasang modul GCP.
"""

from __future__ import annotations

import asyncio
from typing import Optional

import structlog

from app.agent.skema_gemini_terstruktur import (
    KeluaranTambahanGeminiTerstruktur,
    coba_utuhkan_dari_teks_json_gemini_terstruktur,
)

logger_structlog = structlog.get_logger()


async def kutip_penjelasan_tambahan_dari_gemini(teks_penanya_ringkas_bahasa_indonesia: str) -> Optional[str]:
    """Kembalikan potong penjelasan teks ataupun None bila Gemini dinonaktifkan atau gagal."""

    try:
        from app.config import settings as pengatur_aplikasi
    except Exception as kegagalan_pemuatan_penampungnya:  # pragma: tidak ada cabang tes
        logger_structlog.warning("konfig_tidak_terbuka_untuk_gemini", alas=str(kegagalan_pemuatan_penampungnya))
        return None

    if not pengatur_aplikasi.enable_gemini_analysis:
        return None

    return await asyncio.to_thread(
        _panggilan_sinkron_ke_vertex_kepungan,
        pengatur_aplikasi.google_cloud_project,
        pengatur_aplikasi.vertex_ai_location,
        pengatur_aplikasi.gemini_model_name,
        teks_penanya_ringkas_bahasa_indonesia,
    )


async def kutip_tambahan_terstruktur_dari_gemini(teks_massukan_lenkap_tersebet: str) -> Optional[KeluaranTambahanGeminiTerstruktur]:
    """
    Satu pemanggilan Vertex dengan preferensi MIME JSON kemudian validasi Pydantic.

    Mengembalikan None sesuai kebijakan diam-damai bila gagal agar tes CI tidak terganggu.
    """

    try:
        from app.config import settings as pengatur_penampungan
    except Exception as kegagalan_pemuatan_penampungan:  # pragma: tidak ada cabang tes
        logger_structlog.warning("konfig_tidak_terstruktur_untuk_gemini", alas=str(kegagalan_pemuatan_penampungan))
        return None

    if not pengatur_penampungan.enable_gemini_analysis:
        return None

    if not pengatur_penampungan.enable_gemini_json_terstruktur:
        return None

    return await asyncio.to_thread(
        _panggil_vertex_terstruktur_sinkron_tersebet,
        pengatur_penampungan.google_cloud_project,
        pengatur_penampungan.vertex_ai_location,
        pengatur_penampungan.gemini_model_name,
        teks_massukan_lenkap_tersebet,
        float(pengatur_penampungan.gemini_sampling_suhu),
        int(pengatur_penampungan.gemini_token_maks_keluaran_terstruktur),
    )


def _panggil_vertex_terstruktur_sinkron_tersebet(
    nama_proyek_gcp_tersebet: str,
    wilayah_vertikal_tersebet: str,
    nama_model_generatif_tersebet: str,
    teks_massukan_penuhnya_tersebet: str,
    suhu_model_tersebet: float,
    token_keluaran_maks_tersebet: int,
) -> Optional[KeluaranTambahanGeminiTerstruktur]:
    """Bangun GenerativeModel + GenerationConfig sesuai kemampuan SDK terpasang."""
    nama_model_tersebet = str(nama_model_generatif_tersebet).strip()
    try:
        import vertexai  # type: ignore[import-untyped]
        from vertexai.generative_models import (  # type: ignore[import-untyped]
            GenerativeModel,
            GenerationConfig,
        )
    except ImportError:
        logger_structlog.warning("vertex_tidak_terpasang_lewati_gemini_terstruktur")
        return None

    try:
        vertexai.init(project=nama_proyek_gcp_tersebet, location=wilayah_vertikal_tersebet)
        model_generatif_tersebet = GenerativeModel(nama_model_tersebet)
        keluar_bakukan_json_tersebet: Optional[str] = None

        # Utamakan MIME JSON ketika Vertex SDK mendukungnya (mudah dibersihkan tes).
        try:
            pengatur_penjana_json = GenerationConfig(
                temperature=suhu_model_tersebet,
                max_output_tokens=token_keluaran_maks_tersebet,
                response_mime_type="application/json",
            )
            respon_tersebet = model_generatif_tersebet.generate_content(
                teks_massukan_penuhnya_tersebet,
                generation_config=pengatur_penjana_json,
            )
            teks_tersebet_kasar = getattr(respon_tersebet, "text", None)
            if teks_tersebet_kasar:
                keluar_bakukan_json_tersebet = teks_tersebet_kasar.strip()
        except Exception as alas_json_tidak_terpakai_tersebet:  # pragma: tidak ada cabang sukses wajib
            logger_structlog.debug(
                "percobaan_mime_json_gagal_meluncur_ke_teks_bebas",
                alas_potong=str(alas_json_tidak_terpakai_tersebet)[:400],
            )

        if not keluar_bakukan_json_tersebet:
            respon_tersebet = model_generatif_tersebet.generate_content(teks_massukan_penuhnya_tersebet)
            teks_tersebet_kasar = getattr(respon_tersebet, "text", None)
            if teks_tersebet_kasar:
                keluar_bakukan_json_tersebet = teks_tersebet_kasar.strip()

        if not keluar_bakukan_json_tersebet:
            return None

        kembalikan_objek_tersebet = coba_utuhkan_dari_teks_json_gemini_terstruktur(keluar_bakukan_json_tersebet)
        if kembalikan_objek_tersebet is None:
            logger_structlog.warning("vertex_balas_tapi_tidak_parse_skema_terstruktur")
        return kembalikan_objek_tersebet
    except Exception as kegagalan_generatif_tersebet:  # pragma: tidak ada cabang sukses wajib tes
        logger_structlog.warning(
            "panggilan_gemini_terstruktur_gagal_diamkan",
            alas=str(kegagalan_generatif_tersebet)[:500],
        )
        return None


def _panggilan_sinkron_ke_vertex_kepungan(
    nama_proyek_gcp_tersebet: str,
    wilayah_verteks_tersebet: str,
    nama_model_generatif_tersebet: str,
    teks_masukan_penuhnya: str,
) -> Optional[str]:
    """Panggilan sinkron blokir-thread narasi polos; gagal apa pun menghasilkan None."""

    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
    except ImportError:
        logger_structlog.warning("vertex_tidak_terpasang_lewati_gemini")
        return None

    try:
        vertexai.init(project=nama_proyek_gcp_tersebet, location=wilayah_verteks_tersebet)
        model_generatif_tersebet = GenerativeModel(nama_model_generatif_tersebet)
        keluaran_tersebet = model_generatif_tersebet.generate_content(teks_masukan_penuhnya)
        if not getattr(keluaran_tersebet, "text", None):
            return None
        potong_tersebet = keluaran_tersebet.text.strip()
        return potong_tersebet[:4000]
    except Exception as kegagalan_generatif_tersebet:  # pragma: tidak ada cabang sukses wajib tes
        logger_structlog.warning(
            "panggilan_gemini_gagal_diamkan",
            alas=str(kegagalan_generatif_tersebet)[:500],
        )
        return None
