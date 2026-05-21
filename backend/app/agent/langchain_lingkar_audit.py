"""
Integrasi LangChain ringkas untuk Tessera — pekakas (tool) atas query_analyzer dan
alur «Thought → Action → Observation» deterministik tanpa LLM supaya jalur utama lulus CI offline.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_core.tools import StructuredTool

from app.analyzers.query_analyzer import query_analyzer


def perkakas_analisis_query_tessera_tersebet() -> StructuredTool:
    """
    Perkakas tunggal: terima satu query Tessera sebagai string JSON lengkap dan keluarkan rangkuman pola.
    """

    def fungsi_tertutup_tersebet(bentuk_query_json: str) -> str:
        dic_masukan_parse = json.loads(bentuk_query_json)
        if not isinstance(dic_masukan_parse, dict):
            return json.dumps(
                {"galat": "massukan_bukan_objek_dic", "rincian_tersebet": type(dic_masukan_parse).__name__},
                ensure_ascii=False,
            )
        hasil_mesin_analis = query_analyzer.analyze(dic_masukan_parse)
        rekapan_jernih_tersebet: Dict[str, Any] = {
            "koleksi": hasil_mesin_analis.koleksi,
            "operasi": hasil_mesin_analis.operasi,
            "ada_penapis_tenant": hasil_mesin_analis.ada_tenant_filter,
            "nama_kolom_penghuni": hasil_mesin_analis.field_tenant,
            "pelanggaran_polanya": list(hasil_mesin_analis.pattern_violations or []),
            "severity_puncak_tersebet": hasil_mesin_analis.nama_severity_puncak,
            "ada_agg_melintas_tenant": hasil_mesin_analis.ada_cross_tenant,
        }
        return json.dumps(rekapan_jernih_tersebet, ensure_ascii=False)

    return StructuredTool.from_function(
        func=fungsi_tertutup_tersebet,
        name="analisis_polanya_koleksi_ke_tenant_tessera",
        description=(
            "Melihat struktur-serial query MongoDB Tessera (JSON) dan mengembalikan "
            "polanya isolasi multi-tenant menurut aturan query_analyzer."
        ),
    )


def langkah_reka_lingkar_sederhana_tersebet(
    daftar_query_terserialisasi: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Alur bergaya ReACT tetapi tanpa model bahasa: Thought tetap dokumentasi reasoning,
    Action selalu perkakas analisis atas, Observation berisi keluaran terstruktur parse JSON.
    """
    perkakas_dipilih = perkakas_analisis_query_tessera_tersebet()
    jejak_melengkung: List[Dict[str, Any]] = []

    for indeks_urutan, satu_kuerinya in enumerate(daftar_query_terserialisasi):
        nama_koleksi_cadang = satu_kuerinya.get("collection") or satu_kuerinya.get("koleksi")
        pikiran_orisinal = (
            f"Memutuskan menyuruh Tessera membaca koleksi bernilai penyewaan `{nama_koleksi_cadang}` "
            f"langsung secara aturan (langkah #{indeks_urutan})."
        )
        hasil_terlontar_str = perkakas_dipilih.invoke(
            {"bentuk_query_json": json.dumps(satu_kuerinya, default=str)}
        )
        hasil_terlontar_parsed = json.loads(hasil_terlontar_str)
        jejak_melengkung.append(
            {
                "langkah_nomor": indeks_urutan,
                "Thought": pikiran_orisinal,
                "Action": perkakas_dipilih.name,
                "Observation": hasil_terlontar_parsed,
            }
        )

    return {
        "metode_tersebet": "reakansi_deterministik_langchain_core_tool",
        "jumlah_kuerinya": len(daftar_query_terserialisasi),
        "rantai_tersebet": jejak_melengkung,
    }
