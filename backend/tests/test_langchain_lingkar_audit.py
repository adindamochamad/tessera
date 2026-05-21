"""Tes jalur LangChain ringkas (tool + jejak deterministik)."""

import json

from app.agent.langchain_lingkar_audit import (
    langkah_reka_lingkar_sederhana_tersebet,
    perkakas_analisis_query_tessera_tersebet,
)


def test_perkakas_tersebut_memberi_pelanggaran_json():
    perkakas_dicicip = perkakas_analisis_query_tessera_tersebet()
    teks_keluar_dicicip = perkakas_dicicip.invoke(
        {
            "bentuk_query_json": json.dumps(
                {"collection": "orders", "command": "find", "filter": {"status": "x"}}
            )
        }
    )
    objek_rangkuman_dicicip = json.loads(teks_keluar_dicicip)
    assert objek_rangkuman_dicicip["koleksi"] == "orders"
    assert "missing_tenant_filter" in objek_rangkuman_dicicip["pelanggaran_polanya"]


def test_perkakas_menolak_massukan_bukan_dic():
    perkakas_dicicip = perkakas_analisis_query_tessera_tersebet()
    teks_kegagalan_dicicip = perkakas_dicicip.invoke({"bentuk_query_json": "[1,2,3]"})
    rangkuman_dicicip = json.loads(teks_kegagalan_dicicip)
    assert rangkuman_dicicip.get("galat") == "massukan_bukan_objek_dic"


def test_lingkar_deterministik_jejak_dua_langkah():
    hasil_bundel_dicicip = langkah_reka_lingkar_sederhana_tersebet(
        [
            {"collection": "orders", "command": "find", "filter": {"tenant_id": "a", "status": "ok"}},
            {"collection": "orders", "command": "find", "filter": {"status": "z"}},
        ]
    )
    assert hasil_bundel_dicicip["jumlah_kuerinya"] == 2
    rantai_dicicip = hasil_bundel_dicicip["rantai_tersebet"]
    assert rantai_dicicip[0]["Observation"]["ada_penapis_tenant"] is True
    assert rantai_dicicip[1]["Observation"]["ada_penapis_tenant"] is False
