#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mirror_jugadas_from_source.py (runs ON THE VPS, called by /root/slate-deploy-watcher.sh after every slate-ayuda-website
deploy): <path to tools/jugadas_por_oficio.json> -> Baserow T.1100 + /root/state/jugadas-por-oficio.json, through
/root/state/mirror_jugadas_remote.py. Same payload as tools/mirror_jugadas.py (the Mac runner). 2026-09-16: a source edit
must never leave Alfred one day behind (the daily 05:10 cron stays as the safety net).
Usage: python3 /root/mirror-jugadas-from-source.py /path/to/jugadas_por_oficio.json [--dry]"""
import json, os, sys, subprocess, unicodedata, re
def slug_of(v):
    t = unicodedata.normalize("NFKD", v); t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")
src = sys.argv[1]; dry = "--dry" in sys.argv
d = json.load(open(src, encoding="utf-8"))
plays, url = d["_plays"], d["_url"]
rows, flat = [], {"_source": "slate-ayuda-website tools/jugadas_por_oficio.json (deploy hook)", "_url": url, "oficios": {}}
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
                    "url": "%s%s?oficio=%s" % (url, slug, slug_of(oficio)) if oficio != "default" else "%s%s" % (url, slug), "activo": True})
    flat["oficios"][oficio] = {"especial": conf.get("especial", ""), "jugadas": lst}
if len(rows) < 50 or len(flat["oficios"]) < 10:
    sys.exit("refusing: source looks truncated (%d rows, %d oficios)" % (len(rows), len(flat["oficios"])))
payload = json.dumps({"rows": rows, "flat": flat, "dry": dry}, ensure_ascii=False)
r = subprocess.run(["python3", "/root/state/mirror_jugadas_remote.py"], input=payload, text=True, capture_output=True)
print(r.stdout.strip())
if r.returncode:
    print(r.stderr.strip()[-600:]); sys.exit(r.returncode)
