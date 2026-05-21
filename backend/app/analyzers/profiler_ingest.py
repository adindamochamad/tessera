"""
Konversi dokumen koleksi sistem `system.profile` MongoDB ke bentuk serial
yang dipahami `MongoDBQueryAnalyzer` (`collection`, `command`, `filter` / `pipeline`).

MongoDB bisa mengubah struktur profiler antar versi; parser ini konservatif:
hanya `find` dan `aggregate` dari field `command` yang didukung penuh.
"""

from typing import Any, Dict, List, Mapping, Optional, Tuple


def bagi_string_ns_jadi_basis_dan_koleksi(teks_ns: Optional[str]) -> Tuple[str, str]:
    """Pisahkan `basis_data.koleksi` dari profiler `ns`; aman walau koleksi bernama aneh."""
    if not teks_ns or not isinstance(teks_ns, str):
        return "", ""
    posisi_ttik_pertama = teks_ns.find(".")
    if posisi_ttik_pertama < 0:
        return teks_ns.strip(), ""
    nama_basis = teks_ns[:posisi_ttik_pertama].strip()
    nama_koleksi = teks_ns[posisi_ttik_pertama + 1 :].strip()
    return nama_basis, nama_koleksi


def _ambil_filter_dari_legacy_query(perintah: Mapping[str, Any]) -> Dict[str, Any]:
    """Ambil dokumen filter dari bentuk profiler lama bila ada (bukan prioritas utama)."""
    blok_query_lama = perintah.get("query") if isinstance(perintah.get("query"), dict) else None
    if not blok_query_lama:
        return {}
    # Profiler kadang menyimpan pola {$query: {...}, $orderby: ...}
    inti_legacy = blok_query_lama.get("$query")
    if isinstance(inti_legacy, dict):
        return inti_legacy
    return blok_query_lama


def entri_audit_dari_dok_profiler(dok_profiler: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Ubah satu entri profiler menjadi dict analyzer.

    Mengembalikan None bila tidak ada `command` bermakna atau operasi tidak didukung
    (`getmore`, `insertMany`, dll.) agar pemanggil bisa memilah.
    """
    if not isinstance(dok_profiler, Mapping):
        return None

    perintah_utama = dok_profiler.get("command")
    if not isinstance(perintah_utama, dict):
        return None

    nama_basis_dari_ns, nama_koleksi_dari_ns = bagi_string_ns_jadi_basis_dan_koleksi(
        dok_profiler.get("ns") if isinstance(dok_profiler.get("ns"), str) else None
    )

    nama_basis_dari_perintah = perintah_utama.get("$db")
    if isinstance(nama_basis_dari_perintah, str) and nama_basis_dari_perintah.strip():
        nama_basis_terpilih = nama_basis_dari_perintah.strip()
    else:
        nama_basis_terpilih = nama_basis_dari_ns

    # Aggregate modern: { aggregate: "coll", pipeline: [...], ... }
    target_agregasi = perintah_utama.get("aggregate")
    if isinstance(target_agregasi, str) and target_agregasi.strip():
        untaian_tahapan = perintah_utama.get("pipeline")
        if not isinstance(untaian_tahapan, list):
            untaian_tahapan = []
        return {
            "collection": target_agregasi.strip(),
            "command": "aggregate",
            "database": nama_basis_terpilih,
            "filter": {},
            "pipeline": untaian_tahapan,
        }

    # Find modern: { find: "coll", filter: {...}, ... }
    target_carikan = perintah_utama.get("find")
    if isinstance(target_carikan, str) and target_carikan.strip():
        obj_filter = perintah_utama.get("filter")
        if not isinstance(obj_filter, dict):
            obj_filter = _ambil_filter_dari_legacy_query(perintah_utama)
        return {
            "collection": target_carikan.strip(),
            "command": "find",
            "database": nama_basis_terpilih,
            "filter": obj_filter if isinstance(obj_filter, dict) else {},
            "pipeline": [],
        }

    return None


def daftar_entri_audit_dari_batch_profiler(
    daftar_profiler: List[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    """Bangun daftar query audit dari banyak dok profiler; tiap dok gagal dibuang (None)."""
    hasil_terkumpul: List[Dict[str, Any]] = []
    for satu_dok in daftar_profiler:
        satu_entri_diubah = entri_audit_dari_dok_profiler(satu_dok)
        if satu_entri_diubah is not None:
            hasil_terkumpul.append(satu_entri_diubah)
    return hasil_terkumpul
