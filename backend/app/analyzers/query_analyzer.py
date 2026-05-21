"""
Query Analyzer Module

Module ini menganalisis pola query MongoDB untuk mendeteksi
potensi pelanggaran isolasi multi-tenant.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple, Set

# Tingkat severity per pola detektor (hari-hari ke atas = lebih parah secara bisnis Tessera).
SEVERITY_PER_POLA = {
    "missing_tenant_filter": "critical",
    "lookup_tenant_boundary_missing": "critical",
    "cross_tenant_operation": "high",
    "inconsistent_tenant_field_mix": "medium",
}

URUT_KETAT_SEVERITY = ("critical", "high", "medium", "low")


def severity_tertinggi_dari_polanya(daftar_nama_polanya: List[str]) -> Optional[str]:
    """Ambil nama severity tertinggi dari kumpulan string pola laporan."""
    if not daftar_nama_polanya:
        return None
    peringkat_nomor = {nama: indeks for indeks, nama in enumerate(URUT_KETAT_SEVERITY)}
    terjemahan = []
    for nama_pola_satu in daftar_nama_polanya:
        nama_severity_selepas = SEVERITY_PER_POLA.get(nama_pola_satu, "low")
        terjemahan.append((peringkat_nomor.get(nama_severity_selepas, 99), nama_severity_selepas))
    terjemahan.sort(key=lambda tup: tup[0])
    return terjemahan[0][1]


@dataclass
class QueryAnalysisResult:
    """Hasil analisis query."""

    koleksi: str
    operasi: str  # "find", "aggregate", dll
    ada_tenant_filter: bool
    field_tenant: Optional[str] = None
    ada_cross_tenant: bool = False
    pattern_violations: Optional[List[str]] = None
    nama_severity_puncak: Optional[str] = None

    def __post_init__(self):
        if self.pattern_violations is None:
            self.pattern_violations = []
        if self.pattern_violations and self.nama_severity_puncak is None:
            objek_nama_baru_setelah = severity_tertinggi_dari_polanya(self.pattern_violations)
            self.nama_severity_puncak = objek_nama_baru_setelah


class MongoDBQueryAnalyzer:
    """
    Analyzer untuk query MongoDB.

    Mendeteksi pola yang menandakan potensi isu isolasi data antar penyewa tenant.
    """

    TENANT_SCOPED_COLLECTIONS = {
        "orders",
        "users",
        "analytics_events",
        "invoices",
        "products",
        "customers",
    }

    TENANT_FIELD_NAMES = {
        "tenant_id",
        "tenantId",
        "tenant",
        "organization_id",
        "organizationId",
        "org_id",
        "orgId",
        "company_id",
        "companyId",
    }

    def _ambil_filter_efektif(self, bentuk_query: Dict[str, Any]) -> Dict[str, Any]:
        """Gabungkan filter top-level atau $match pertama pada pipeline agregasi."""
        penapis_atas = bentuk_query.get("filter") or {}
        if penapis_atas:
            return penapis_atas
        for tahap in bentuk_query.get("pipeline", []):
            if isinstance(tahap, dict) and "$match" in tahap:
                potong = tahap["$match"]
                if isinstance(potong, dict):
                    return potong
        return {}

    def analyze(self, query: Dict[str, Any]) -> QueryAnalysisResult:
        koleksi = query.get("collection", "unknown")
        operasi = query.get("command", "unknown")
        objek_penapis = self._ambil_filter_efektif(query)
        untaian_agg = query.get("pipeline", [])

        butuh_pemisahan_penghuni = koleksi in self.TENANT_SCOPED_COLLECTIONS

        kumpulan_kunci = self._kumpulkan_semua_kunci_string(query)
        pola_pelanggaran: List[str] = []

        if butuh_pemisahan_penghuni and "tenant_id" in kumpulan_kunci and "tenantId" in kumpulan_kunci:
            pola_pelanggaran.append("inconsistent_tenant_field_mix")

        for tahap_potong_untuk_periksa in untaian_agg:
            if not isinstance(tahap_potong_untuk_periksa, dict):
                continue
            ada_lakukan_simpang = self._cek_lookup_butuh_penjaga(tahap_potong_untuk_periksa)
            if ada_lakukan_simpang:
                pola_pelanggaran.append("lookup_tenant_boundary_missing")

        ada_filter_tenant, nama_field_tenant = self._cek_filter_tenant(objek_penapis)
        ada_melintasi_kelompok_penghuni = self._cek_agregasi_melintas_tenant(query)

        if not butuh_pemisahan_penghuni:
            return QueryAnalysisResult(
                koleksi=koleksi,
                operasi=operasi,
                ada_tenant_filter=True,
                field_tenant=None,
                ada_cross_tenant=False,
                pattern_violations=pola_pelanggaran,
            )

        if not ada_filter_tenant:
            pola_pelanggaran.append("missing_tenant_filter")

        if ada_melintasi_kelompok_penghuni:
            pola_pelanggaran.append("cross_tenant_operation")

        return QueryAnalysisResult(
            koleksi=koleksi,
            operasi=operasi,
            ada_tenant_filter=ada_filter_tenant,
            field_tenant=nama_field_tenant,
            ada_cross_tenant=ada_melintasi_kelompok_penghuni,
            pattern_violations=pola_pelanggaran,
        )

    def _kumpulkan_semua_kunci_string(self, pangkal: Any) -> Set[str]:
        """Kumpulkan semua nama kunci bentuk string rekursif (cek inkonsistensi nama)."""
        hasil_kepingan: Set[str] = set()
        bungkus_kerja_antrian = [pangkal]
        while bungkus_kerja_antrian:
            objek_ini = bungkus_kerja_antrian.pop()
            if isinstance(objek_ini, dict):
                for kunci_dalam, nilai_dalam in objek_ini.items():
                    if isinstance(kunci_dalam, str):
                        hasil_kepingan.add(kunci_dalam)
                    bungkus_kerja_antrian.append(nilai_dalam)
            elif isinstance(objek_ini, list):
                for elemen_kecil in objek_ini:
                    bungkus_kerja_antrian.append(elemen_kecil)
        return hasil_kepingan

    def _cek_lookup_butuh_penjaga(self, tahap_kerangka: Dict[str, Any]) -> bool:
        """
        Kembalikan True jika $lookup menyentuh koleksi tenant-scoped
        tetapi tidak dapat mengamankan penyewa tenant dengan jelas.
        """
        if "$lookup" not in tahap_kerangka:
            return False
        objek_simpang_raw = tahap_kerangka["$lookup"]
        if not isinstance(objek_simpang_raw, dict):
            return False

        koleksi_kepungan = objek_simpang_raw.get("from", "")
        if koleksi_kepungan not in self.TENANT_SCOPED_COLLECTIONS:
            return False

        untaian_dalam_simpang_raw = objek_simpang_raw.get("pipeline")

        # Pipeline ada — hanya boleh lolos ketika blok $match pertama mengandungi filter tenant sah.
        if untaian_dalam_simpang_raw is not None:
            if not isinstance(untaian_dalam_simpang_raw, list) or len(untaian_dalam_simpang_raw) == 0:
                return True
            for satu_tapis in untaian_dalam_simpang_raw:
                if not isinstance(satu_tapis, dict):
                    continue
                if "$match" in satu_tapis:
                    potong_kepungan = satu_tapis["$match"]
                    if not isinstance(potong_kepungan, dict):
                        return True
                    ada_tersemat_kepungan, _ = self._cek_filter_tenant(potong_kepungan)
                    return not ada_tersemat_kepungan
            return True

        # Bentuk klasik dengan localField dan foreignField — dua-duanya mestilah bernama penyewa tenant yang dikenali.
        kiri_lokal = objek_simpang_raw.get("localField") or ""
        kanan_awal_asing = objek_simpang_raw.get("foreignField") or ""
        if not isinstance(kiri_lokal, str) or not isinstance(kanan_awal_asing, str):
            return True
        sah_kiri_local = self._cek_kolom_layak_penghuni(kiri_lokal)
        sah_awal_foreign = self._cek_kolom_layak_penghuni(kanan_awal_asing)
        return not (sah_kiri_local and sah_awal_foreign)

    def _cek_kolom_layak_penghuni(self, nama_kolom_potong_string: str) -> bool:
        return nama_kolom_potong_string in self.TENANT_FIELD_NAMES

    def _cek_filter_tenant(self, objek_penapis: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Periksa apakah blok filter mengunci penyewa tenant dengan nama kolom umum Tessera."""

        # Asumsi koleksi utama sudah disaring di pemanggilan analyze.
        if not isinstance(objek_penapis, dict):
            return (False, None)

        for nama_kolom_tersebut in self.TENANT_FIELD_NAMES:
            if nama_kolom_tersebut in objek_penapis:
                return (True, nama_kolom_tersebut)

        if "$or" in objek_penapis and isinstance(objek_penapis["$or"], list):
            daftar_kepungan_bersambung_raw = objek_penapis["$or"]
            if len(daftar_kepungan_bersambung_raw) == 0:
                return (False, None)
            nama_kolom_terpilih_terpenuhi_optional: Optional[str] = None
            for salah_satu_kepingan_dalam_raw in daftar_kepungan_bersambung_raw:
                if not isinstance(salah_satu_kepingan_dalam_raw, dict):
                    return (False, None)
                ada_filternya_tersandang_tenantnya, nama_satu_tersebet = self._cek_filter_tenant(
                    salah_satu_kepingan_dalam_raw
                )
                if not ada_filternya_tersandang_tenantnya:
                    return (False, None)
                if nama_satu_tersebet is not None:
                    nama_kolom_terpilih_terpenuhi_optional = nama_kolom_terpilih_terpenuhi_optional or nama_satu_tersebet
            return (True, nama_kolom_terpilih_terpenuhi_optional)

        if "$and" in objek_penapis and isinstance(objek_penapis["$and"], list):
            for salah_satu_kepingan in objek_penapis["$and"]:
                if isinstance(salah_satu_kepingan, dict):
                    ada_tersebut, nama_kolom_tersebut = self._cek_filter_tenant(salah_satu_kepingan)
                    if ada_tersebut:
                        return (True, nama_kolom_tersebut)

        if "$nor" in objek_penapis and isinstance(objek_penapis["$nor"], list):
            # Pola lebih jarang; kita perlakukan sama seperti penyaringan rekursif dangkal.
            for salah_satu_kepingan in objek_penapis["$nor"]:
                if isinstance(salah_satu_kepingan, dict):
                    ada_tersebut, nama_kolom_tersebut = self._cek_filter_tenant(salah_satu_kepingan)
                    if ada_tersebut:
                        return (True, nama_kolom_tersebut)

        return (False, None)

    def _cek_agregasi_melintas_tenant(self, bentuk_semua_raw: Dict[str, Any]) -> bool:
        """
        Tangkap $group yang mengelompokkan atas dimensi lain tanpa kunci penyewa tenant pertama.
        Heuristik sederhana hari-ke-hari pembangunan Day 2.
        """
        untaian_tahap_kerja = bentuk_semua_raw.get("pipeline", [])
        for tahap_satu_kerja_potong_raw in untaian_tahap_kerja:
            if not isinstance(tahap_satu_kerja_potong_raw, dict):
                continue
            if "$group" not in tahap_satu_kerja_potong_raw:
                continue
            blok_kelompok = tahap_satu_kerja_potong_raw["$group"]
            if not isinstance(blok_kelompok, dict) or "_id" not in blok_kelompok:
                continue
            teks_kerangka_id_kepungan = blok_kelompok["_id"]
            # Hanya pola string seperti "$customerId"; diabaikan struktur gabungan lebih rumit masa depannya.
            if isinstance(teks_kerangka_id_kepungan, str):
                teks_kerangka_id_kepungan_str = teks_kerangka_id_kepungan
                ada_satupun_rujukan_tenant_tersebet = False
                for nama_rujukan_tenant_tersebet in self.TENANT_FIELD_NAMES:
                    if nama_rujukan_tenant_tersebet in teks_kerangka_id_kepungan_str:
                        ada_satupun_rujukan_tenant_tersebet = True
                        break
                if not ada_satupun_rujukan_tenant_tersebet:
                    return True
        return False


query_analyzer = MongoDBQueryAnalyzer()
