"""
Tessera Agent — inti auditor berbasis aturan (+ Gemini opsional).
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog

from app.analyzers.query_analyzer import (
    SEVERITY_PER_POLA,
    URUT_KETAT_SEVERITY,
    query_analyzer,
)
from app.agent.gemini_opsional import (
    kutip_penjelasan_tambahan_dari_gemini,
    kutip_tambahan_terstruktur_dari_gemini,
)
from app.agent.prompt_templatan_violasi import (
    bangun_massukan_terstruktur_violasi_tersebet,
    dapatkan_instruksi_sistem_tersebet,
)
from app.config import settings

logger = structlog.get_logger()


# Contoh jalur cepat pengujian lokal ketika MCP belum tersedia.
QUERY_CONTOH_STANDAR: List[Dict[str, Any]] = [
    {
        "collection": "orders",
        "command": "find",
        "filter": {"status": "pending"},
    },
]


def pilih_nama_pola_terparah(daftar_polanya: List[str]) -> str:
    """Pilih pola dengan severity tertinggi; seri sama menurun leksikografi."""
    if not daftar_polanya:
        return "unknown_pattern"
    peringkat_angka = {s: i for i, s in enumerate(URUT_KETAT_SEVERITY)}
    tupel_pembanding: List[tuple[int, str, str]] = []
    for nama_pola_satu_ini in sorted(set(daftar_polanya)):
        tingkat_terjemahan_ini = peringkat_angka.get(
            SEVERITY_PER_POLA.get(nama_pola_satu_ini, "low"), 99
        )
        tupel_pembanding.append((tingkat_terjemahan_ini, nama_pola_satu_ini, nama_pola_satu_ini))
    tupel_pembanding.sort(key=lambda tup: (tup[0], tup[1]))
    return tupel_pembanding[0][2]


UNTUK_DESKRIPSI_POLA_RINGKAS_INI: Dict[str, tuple[str, str, str]] = {
    "missing_tenant_filter": (
        "Query koleksi bernilai-penyewai tanpa pembatas penyewai tenant sah.",
        "Filter tidak mengharuskan pembatas koleksi-ke-tenant penyewaan.",
        "Data tenant lain bisa ikut tertampil secara tidak sengaja — risiko kerahasiaan dan regulasi tinggi.",
    ),
    "lookup_tenant_boundary_missing": (
        "Tahapan $lookup ke koleksi tenant-scoped tidak menjamin batas penyewaan tenant.",
        "Join bisa melintasi batas koleksi-ke-tenant — pipeline atau pasangan kolom tidak mengunci tenant.",
        "Gabungan koleksi bisa mengembalikan baris penyewai lain secara implisit.",
    ),
    "cross_tenant_operation": (
        "$group pada agregasi mengelompokkan atas dimensi non-tenant utama.",
        "Agregasi global tanpa penyekatan tenant utama yang jelas menyatukan beberapa penyewa.",
        "Pelaporan bisa mengcampur KPI beda penyewai menyesatkan keamanan SaaS Anda.",
    ),
    "inconsistent_tenant_field_mix": (
        "Kolom tenant_id snake_case dan tenantId camelCase muncul berdampingan secara tidak konsisten.",
        "Bahasa penamaan terpecah antara tim atau layanan menghambat kebijakan pemaksaan pembatas koleksi-ke-tenant.",
        "Kerentanan logika penyaringan koleksi-ke-tenant karena pembacaan pola berbeda-beda antara servis Anda.",
    ),
}


@dataclass
class ViolationDeteksi:
    """Model satu pelanggaran yang telah terurai."""

    id_violation: str
    tipe_violation: str
    severity: str
    koleksi: str
    query_pattern: str
    deskripsi: str
    root_cause: str
    dampak_potensial: str
    rekomendasi_fix: str
    kode_fix: Optional[str] = None
    waktu_deteksi: datetime = None
    analisis_terstruktur_gemini: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.waktu_deteksi is None:
            self.waktu_deteksi = datetime.now(timezone.utc)

    def jadi_dict_serial(self) -> Dict[str, Any]:
        """Serialisasi aman bagi JSON REST."""
        kembalikan_kamus_tersebet = {
            "id_violation": self.id_violation,
            "tipe_violation": self.tipe_violation,
            "severity": self.severity,
            "koleksi": self.koleksi,
            "query_pattern": self.query_pattern,
            "deskripsi": self.deskripsi,
            "root_cause": self.root_cause,
            "dampak_potensial": self.dampak_potensial,
            "rekomendasi_fix": self.rekomendasi_fix,
            "kode_fix": self.kode_fix,
            "waktu_deteksi": self.waktu_deteksi.isoformat(),
        }
        if self.analisis_terstruktur_gemini is not None:
            kembalikan_kamus_tersebet["analisis_terstruktur_gemini"] = self.analisis_terstruktur_gemini
        return kembalikan_kamus_tersebet


class TesseraAgent:
    """Menjalankan rantai analisis aturan kemudian opsional Gemini untuk penjelasan."""

    def __init__(
        self,
        nama_proyek_id: str,
        wilayah_vertikal: str = "us-central1",
        nama_model_generatif_gemini_saja: str = "gemini-2.0-flash",
    ):
        self.project_id = nama_proyek_id
        self.location = wilayah_vertikal
        self.model_name = nama_model_generatif_gemini_saja
        self.violations_terdeteksi: List[ViolationDeteksi] = []
        logger.info(
            "agent_initialized",
            project=nama_proyek_id,
            model=nama_model_generatif_gemini_saja,
        )

    async def mulai_audit(
        self,
        nama_database: str,
        daftar_queries_kustom: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Urut beberapa query sampai penilaian pematuhan koleksi-ke-tenant sederhana."""
        self.violations_terdeteksi.clear()
        koleksi_kerja_ini = daftar_queries_kustom or QUERY_CONTOH_STANDAR
        untuk_setiap_dicetak_tersebut: List[Dict[str, Any]] = []

        for bentuk_satunya in koleksi_kerja_ini:
            bentuk_keparahan_tersebet = await self.analyze_query(
                bentuk_satunya,
                nama_basis_audit_tersebet=nama_database,
            )
            if bentuk_keparahan_tersebet is not None:
                self.violations_terdeteksi.append(bentuk_keparahan_tersebet)
                untuk_setiap_dicetak_tersebut.append(
                    {
                        "query": bentuk_satunya,
                        "violation_id": bentuk_keparahan_tersebet.id_violation,
                    }
                )

        kembalikan_pembantu_score = round(self.hitung_skor_kepatuhan(), 4)
        return {
            "status": "completed_rule_based_batch",
            "database": nama_database,
            "jumlah_query_diuji": len(koleksi_kerja_ini),
            "violations_terdeteksi": [itu.jadi_dict_serial() for itu in self.violations_terdeteksi],
            "skor_pematuhan_tersebut_pct": kembalikan_pembantu_score,
            "analisis_terperinci_kecil_tersebut": untuk_setiap_dicetak_tersebut,
            "waktu_selesai_utc_iso": datetime.now(timezone.utc).isoformat(),
        }

    async def analyze_query(
        self,
        bentuk_query_abstraksi: Dict[str, Any],
        nama_basis_audit_tersebet: str = "",
    ) -> Optional[ViolationDeteksi]:
        hasil_analisis_tersebet = query_analyzer.analyze(bentuk_query_abstraksi)
        if not hasil_analisis_tersebet.pattern_violations:
            return None

        pola_puncak_nomor_tertentu_ini = pilih_nama_pola_terparah(
            hasil_analisis_tersebet.pattern_violations
        )
        tingkat_severity_tersebut_ini = (
            hasil_analisis_tersebet.nama_severity_puncak
            if hasil_analisis_tersebet.nama_severity_puncak
            else SEVERITY_PER_POLA.get(pola_puncak_nomor_tertentu_ini, "low")
        )
        pola_info_tripel = UNTUK_DESKRIPSI_POLA_RINGKAS_INI.get(
            pola_puncak_nomor_tertentu_ini,
            (
                "Pola koleksi-ke-tenant tidak dikenali penyaringan Anda.",
                "Analisis aturan Tessera mencat pola tambahan Anda sendiri masa depannya.",
                "Tinjau arsitektur pembatas koleksi-ke-tenant menyeluruh.",
            ),
        )
        nomor_sidik_unik_tersebet = str(uuid.uuid4())

        pola_cetak_tersebut = json.dumps(bentuk_query_abstraksi, default=str)
        pola_cetak_tersebut_terpotonglah = pola_cetak_tersebut[:4096]

        viol_objek_tersebet = ViolationDeteksi(
            id_violation=nomor_sidik_unik_tersebet,
            tipe_violation=pola_puncak_nomor_tertentu_ini,
            severity=tingkat_severity_tersebut_ini,
            koleksi=hasil_analisis_tersebet.koleksi,
            query_pattern=pola_cetak_tersebut_terpotonglah,
            deskripsi=pola_info_tripel[0],
            root_cause=pola_info_tripel[1],
            dampak_potensial=pola_info_tripel[2],
            rekomendasi_fix=(
                "Sempurnakan filter tenant_id konstan di setiap operasi pembacaan utama "
                "atau lakukan pembatas koleksi-ke-tenant di pipeline agregasi."
            ),
        )

        if settings.enable_gemini_analysis:
            massukan_penuh_gemini_tersebet = (
                dapatkan_instruksi_sistem_tersebet()
                + "\n\n=== MASSUKAN TEKNIS TERSTRUKTUR ===\n\n"
                + bangun_massukan_terstruktur_violasi_tersebet(
                    pola_puncak_nomor_tertentu_ini,
                    tingkat_severity_tersebut_ini,
                    pola_info_tripel,
                    pola_cetak_tersebut_terpotonglah,
                    hasil_analisis_tersebet.koleksi,
                    nama_basis_audit_tersebet,
                )
            )
            struktur_gemini_tersebet = await kutip_tambahan_terstruktur_dari_gemini(massukan_penuh_gemini_tersebet)
            if struktur_gemini_tersebet is not None:
                viol_objek_tersebet.analisis_terstruktur_gemini = struktur_gemini_tersebet.model_dump()
            else:
                gabungan_kepungan_tanya_gemini_tersebet = (
                    f"Jelaskan secara singkat (Bahasa Indonesia) pelanggaran isolasi multi-tenant: "
                    f"{viol_objek_tersebet.deskripsi} — pola utama {pola_puncak_nomor_tertentu_ini}"
                )
                teks_penjelasan_tambahan = await kutip_penjelasan_tambahan_dari_gemini(
                    gabungan_kepungan_tanya_gemini_tersebet
                )
                if teks_penjelasan_tambahan:
                    viol_objek_tersebet.deskripsi = (
                        f"{viol_objek_tersebet.deskripsi} [Gemini] {teks_penjelasan_tambahan[:900]}"
                    )

        # Catatan pemanggilan: viol tidak otomatis disimpan dalam daftar sampai pemanggilan mulai_audit.
        return viol_objek_tersebet

    async def cari_pattern_serupa(self, violation: ViolationDeteksi) -> List[Dict[str, Any]]:
        """Masa-depan Vector Search (Day 3)."""
        logger.info(
            "pencarian_vector_belum_tersedia",
            idnya=violation.id_violation,
        )
        return []

    async def generate_remediation(self, violation: ViolationDeteksi) -> Dict[str, Any]:
        """Saran struktural bergantung aturan Anda — tanpa Gemini wajib."""
        return {
            "id_violation": violation.id_violation,
            "tipe": violation.tipe_violation,
            "langkah_umum_pembaharuan_tersebet": violation.rekomendasi_fix,
            "contoh_umum_tersebet": violation.kode_fix,
            "sumber_kepungan": "aturan Tessera_day2_manual",
        }

    def hitung_skor_kepatuhan(self) -> float:
        if not self.violations_terdeteksi:
            return 100.0
        total_penalty = 0
        for sebuah_viol_tersebet in self.violations_terdeteksi:
            if sebuah_viol_tersebet.severity == "critical":
                total_penalty += 25
            elif sebuah_viol_tersebet.severity == "high":
                total_penalty += 15
            elif sebuah_viol_tersebet.severity == "medium":
                total_penalty += 5
            else:
                total_penalty += 2
        return max(0.0, 100.0 - total_penalty)

    def get_compliance_score(self) -> float:
        """Alias dokumentasi roadmap lama Anda."""
        return self.hitung_skor_kepatuhan()
