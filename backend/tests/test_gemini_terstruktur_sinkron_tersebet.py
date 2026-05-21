"""Tes penyambungan TesseraAgent + Gemini struktur palsu tanpa Vertex."""

from __future__ import annotations

import asyncio

import pytest
from pydantic import ValidationError

from app.agent import tessera_agent as modul_tessera_tersebet
from app.agent.skema_gemini_terstruktur import KeluaranTambahanGeminiTerstruktur
from app.agent.tessera_agent import TesseraAgent
from app.config import settings


def test_analyze_query_gemini_terstruktur_terisi_tanpa_jaringan_tersebet(monkeypatch: pytest.MonkeyPatch):
    """Jangan panggil Vertex; pastikan blok terstruktur mengisi ViolationDeteksi."""
    struktur_tersebet = KeluaranTambahanGeminiTerstruktur(
        ringkasan_eksekutif=(
            "Kueri koleksi bernilai-penyewai tanpa pembatas koleksi-ke-tenant dikenali pola Tessera utama."
        ),
        penyebab_mendalam="Tidak ada filter koleksi-ke-tenant terlihat blok filter analyzer saat audit.",
        dampak_umum="Data penyewai lain bisa bocor bila koleksi digunakan bersama layanan atasnya.",
        saran_prioritas=["Tambah constant tenant aplikasi Anda", "Pantau agregasi di pipeline"],
        kepercayaan_0_hingga_100=61,
    )

    async def palsu_terstruktur_tersebet(_prompt_penuh: str):
        return struktur_tersebet

    async def narasi_tidak_boleh_dipanggil_tersebet(_teks_penjelasan: str):
        raise AssertionError("narasi_polos_fallback_tidak_dibutuhkan_saat_terstruktur_ok")

    monkeypatch.setattr(modul_tessera_tersebet.settings, "enable_gemini_analysis", True)
    monkeypatch.setattr(modul_tessera_tersebet.settings, "enable_gemini_json_terstruktur", True)
    monkeypatch.setattr(
        modul_tessera_tersebet,
        "kutip_tambahan_terstruktur_dari_gemini",
        palsu_terstruktur_tersebet,
        raising=True,
    )
    monkeypatch.setattr(
        modul_tessera_tersebet,
        "kutip_penjelasan_tambahan_dari_gemini",
        narasi_tidak_boleh_dipanggil_tersebet,
        raising=True,
    )

    ag_tersebet = TesseraAgent(
        settings.google_cloud_project,
        settings.vertex_ai_location,
        settings.gemini_model_name,
    )
    viol_tersebet = asyncio.run(
        ag_tersebet.analyze_query(
            {"collection": "orders", "command": "find", "filter": {"status": "z"}},
            nama_basis_audit_tersebet="db_uji_terstruktur",
        )
    )
    assert viol_tersebet is not None
    assert viol_tersebet.analisis_terstruktur_gemini is not None
    assert viol_tersebet.analisis_terstruktur_gemini["kepercayaan_0_hingga_100"] == 61


def test_analyze_query_gemini_terstruktur_tidak_terisi_memakai_narasi_lama_tersebet(
    monkeypatch: pytest.MonkeyPatch,
):
    """Bila blok JSON kosong pemanggilan jatuh ke narasi Gemini polos Lama."""

    narasi_terperangkap: dict[str, str] = {}

    async def struktur_tidak_terserah(_prompt_penuh: str):
        return None

    async def narasi_palsu_ringkas_tersebet(teks_masuk: str):
        narasi_terperangkap["isi"] = teks_masuk
        return "penjelasan_singkat_palsu_dari_gemini"

    monkeypatch.setattr(modul_tessera_tersebet.settings, "enable_gemini_analysis", True)
    monkeypatch.setattr(modul_tessera_tersebet.settings, "enable_gemini_json_terstruktur", True)
    monkeypatch.setattr(
        modul_tessera_tersebet,
        "kutip_tambahan_terstruktur_dari_gemini",
        struktur_tidak_terserah,
        raising=True,
    )
    monkeypatch.setattr(
        modul_tessera_tersebet,
        "kutip_penjelasan_tambahan_dari_gemini",
        narasi_palsu_ringkas_tersebet,
        raising=True,
    )

    ag_tersebet = TesseraAgent(
        settings.google_cloud_project,
        settings.vertex_ai_location,
        settings.gemini_model_name,
    )
    viol_tersebet = asyncio.run(
        ag_tersebet.analyze_query(
            {"collection": "orders", "command": "find", "filter": {}},
            nama_basis_audit_tersebet="db_uji_fallback",
        )
    )
    assert viol_tersebet is not None
    assert viol_tersebet.analisis_terstruktur_gemini is None
    assert narasi_terperangkap["isi"].startswith(
        "Jelaskan secara singkat (Bahasa Indonesia) pelanggaran isolasi multi-tenant"
    )
    assert "[Gemini] penjelasan_singkat_palsu_dari_gemini" in viol_tersebet.deskripsi


def test_utuhkan_json_valid_tersebet_terapung_ke_schema():
    from app.agent.skema_gemini_terstruktur import coba_utuhkan_dari_teks_json_gemini_terstruktur

    teks_tersebet = (
        '{"ringkasan_eksekutif": "Ringkasan cukup panjang dua kali tiga kata untuk tes unit.", '
        '"penyebab_mendalam": "Kerentanan muncul karena pola filter tidak konsisten koleksi utama.", '
        '"dampak_umum": "Pelanggaran kerahasiaan multi-tenant rentan eksploitasi gabungan KPI.", '
        '"saran_prioritas": ["Segera sisipkan pembatas koleksi-ke-tenant utama", "Rekam tes keamanan"], '
        '"kepercayaan_0_hingga_100": 72}'
    )
    kembalikan_objek_tersebet = coba_utuhkan_dari_teks_json_gemini_terstruktur(teks_tersebet)
    assert kembalikan_objek_tersebet is not None
    assert kembalikan_objek_tersebet.kepercayaan_0_hingga_100 == 72


def test_utuhkan_json_rusak_mengembalikan_none_tersebet():
    from app.agent.skema_gemini_terstruktur import coba_utuhkan_dari_teks_json_gemini_terstruktur

    assert coba_utuhkan_dari_teks_json_gemini_terstruktur("{bukan-json") is None


def test_model_tolak_saran_kosong_total_tersebet():
    with pytest.raises((ValidationError, ValueError)):
        KeluaranTambahanGeminiTerstruktur(
            ringkasan_eksekutif="A" * 10,
            penyebab_mendalam="Penyebab minimal string panjang tes unit di sisi validasi lagi",
            dampak_umum="Dampak umum koleksi utama yang mendukung tes unit lagi di sisi validasi Anda",
            saran_prioritas=["   ", ""],
            kepercayaan_0_hingga_100=50,
        )
