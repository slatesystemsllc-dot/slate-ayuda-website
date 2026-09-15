#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mirror_jugadas.py: tools/jugadas_por_oficio.json (the source) -> Baserow T.1100 "Jugadas por oficio" (rows, idempotent
by Oficio + Jugada) AND /root/state/jugadas-por-oficio.json on the VPS (Alfred reads that file, never Baserow, in a pass).
Run on the Mac: python3 tools/mirror_jugadas.py [--dry]. Needs ssh slate (the Baserow token lives there)."""
import json, os, sys, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "tools", "jugadas_por_oficio.json"), encoding="utf-8"))
plays, url = d["_plays"], d["_url"]
rows, flat = [], {"_source": "slate-ayuda-website tools/jugadas_por_oficio.json", "_url": url, "oficios": {}}
for oficio, conf in d.items():
    if oficio.startswith("_"): continue
    lst = []
    if conf.get("especial"):
        rows.append({"Oficio": oficio, "Orden": 0, "Jugada": "especial", "Titulo ES": "Solo tu oficio puede hacer esto", "Titulo EN": "Only your trade can do this",
                     "Linea SMS ES": "", "Linea SMS EN": "", "Activo": False, "Especial": conf["especial"]})
    for i, slug in enumerate(conf["orden"], 1):
        p = plays[slug]
        rows.append({"Oficio": oficio, "Orden": i, "Jugada": slug, "Titulo ES": p["es"], "Titulo EN": p["en"],
                     "Linea SMS ES": p["sms_es"], "Linea SMS EN": p["sms_en"], "Activo": True, "Especial": ""})
        lst.append({"orden": i, "jugada": slug, "titulo_es": p["es"], "titulo_en": p["en"], "sms_es": p["sms_es"], "sms_en": p["sms_en"],
                    "url": "%s%s?oficio=%s" % (url, slug, oficio) if oficio != "default" else "%s%s" % (url, slug), "activo": True})
    flat["oficios"][oficio] = {"especial": conf.get("especial", ""), "jugadas": lst}
dry = "--dry" in sys.argv
print("rows", len(rows), "oficios", len(flat["oficios"]), "DRY" if dry else "")
payload = json.dumps({"rows": rows, "flat": flat, "dry": dry}, ensure_ascii=False)
REMOTE = os.path.join(ROOT, "tools", "mirror_jugadas_remote.py")
subprocess.run(["scp", "-q", REMOTE, "slate:/root/state/mirror_jugadas_remote.py"], check=True)
r = subprocess.run(["ssh", "slate", "python3", "/root/state/mirror_jugadas_remote.py"], input=payload, text=True, capture_output=True)
print(r.stdout.strip()); print(r.stderr.strip()[-600:] if r.returncode else "")
sys.exit(r.returncode)
