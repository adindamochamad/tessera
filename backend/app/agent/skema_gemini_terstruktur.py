"""
Skema keluaran terstruktur dari Gemini Vertex — divalidasi dengan Pydantic sebelum disimpan.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class KeluaranTambahanGeminiTerstruktur(BaseModel):
    """Bentuk JSON yang harus dibalas model bila pemanggilan sukses."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    ringkasan_eksekutif: str = Field(
        ...,
        min_length=3,
        max_length=2400,
        description="Ikhtisar 2–6 kalimat Bahasa Indonesia untuk juri/demo.",
    )
    penyebab_mendalam: str = Field(
        ...,
        min_length=3,
        max_length=1600,
        description="Bahasa Indonesia: mengapa pola ini bermasalah di konteks SaaS.",
    )
    dampak_umum: str = Field(
        ...,
        min_length=3,
        max_length=1600,
        description="Bahasa Indonesia: risiko kebocoran/regulasi secara umum.",
    )
    saran_prioritas: List[str] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Bahasa Indonesia: daftar bertingkat apa yang dicek/perbaiki dulu.",
    )
    kepercayaan_0_hingga_100: int = Field(
        ...,
        ge=0,
        le=100,
        description="Perkiraan keyakinan model terhadap analisis narasi ini.",
    )

    @field_validator("saran_prioritas")
    @classmethod
    def pendekkan_butir_butir_tersebet(cls, nilai_butir_butir_tersebet: List[str]) -> List[str]:
        """Jaga tiap bullet tetap pendek untuk respons API."""
        bersih_tersebet: List[str] = []
        for satu_butir_tersebet in nilai_butir_butir_tersebet:
            teks_terpotong_tersebet = satu_butir_tersebet.strip()[:400]
            if teks_terpotong_tersebet:
                bersih_tersebet.append(teks_terpotong_tersebet)
        if not bersih_tersebet:
            raise ValueError("saran_prioritas_tidak_kosong_wajib")
        return bersih_tersebet


import json


def coba_utuhkan_dari_teks_json_gemini_terstruktur(
    teks_mentah_json_tersebet: str,
) -> KeluaranTambahanGeminiTerstruktur | None:
    """
    Parsing aman keluar Vertex; mengembalikan None bila gagal bentuk/skema.
    """

    try:
        potong_objek_tersebet = json.loads(teks_mentah_json_tersebet.strip())
    except (json.JSONDecodeError, AttributeError):
        return None

    if not isinstance(potong_objek_tersebet, dict):
        return None

    try:
        return KeluaranTambahanGeminiTerstruktur.model_validate(potong_objek_tersebet)
    except Exception:
        return None
