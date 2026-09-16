
import json, sys, subprocess, urllib.request
P = json.load(sys.stdin); rows, flat, dry = P["rows"], P["flat"], P["dry"]
tok = subprocess.check_output(["/usr/local/bin/secret", "get", "baserow_token"]).decode().strip()
H = {"Authorization": "Token " + tok, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
T = "https://baserow.slatesystems.io/api/database/rows/table/1100/"
def req(url, method="GET", body=None):
    r = urllib.request.Request(url, data=(json.dumps(body).encode() if body is not None else None), headers=H, method=method)
    return json.loads(urllib.request.urlopen(r, timeout=40).read().decode() or "{}")
have = {}
page = 1
while True:
    d = req(T + "?user_field_names=true&size=200&page=%d" % page)
    for r in d.get("results", []):
        have[(str(r.get("Oficio") or ""), str(r.get("Jugada") or ""))] = r
    if not d.get("next"): break
    page += 1
n_post = n_patch = n_same = 0
for row in rows:
    key = (row["Oficio"], row["Jugada"]); cur = have.get(key)
    if cur and all(str(cur.get(k) or "") == str(v if v is not None else "") for k, v in row.items() if k not in ("Activo",)) and bool(cur.get("Activo")) == row["Activo"]:
        n_same += 1; continue
    if dry: print("  DRY", "PATCH" if cur else "POST", key); continue
    if cur: req(T + "%d/?user_field_names=true" % cur["id"], "PATCH", row); n_patch += 1
    else: req(T + "?user_field_names=true", "POST", row); n_post += 1
for k, r in list(have.items()):
    if k == ("", "") and not dry:
        req(T + "%d/" % r["id"], "DELETE"); print("  deleted empty default row", r["id"])
extra = [k for k in have if k not in {(r["Oficio"], r["Jugada"]) for r in rows} and k != ("", "")]
# 2026-09-16: a play dropped from the source is switched OFF (Activo False, Orden 99), never left with its old order:
# Alfred reads /root/state/jugadas-por-oficio.json by order and skips activo=false (projector line ~3248).
n_off = 0
for k in extra:
    r = have[k]
    if bool(r.get("Activo")) or int(r.get("Orden") or 0) != 99:
        if not dry: req(T + "%d/?user_field_names=true" % r["id"], "PATCH", {"Activo": False, "Orden": 99})
        n_off += 1
print("T.1100: %d POST, %d PATCH, %d same, %d rows not in source (switched off: %d): %s" % (n_post, n_patch, n_same, len(extra), n_off, extra[:5]))
if not dry:
    import os
    os.makedirs("/root/state", exist_ok=True)
    tmp = "/root/state/jugadas-por-oficio.json.tmp"
    open(tmp, "w", encoding="utf-8").write(json.dumps(flat, ensure_ascii=False, indent=1)); os.replace(tmp, "/root/state/jugadas-por-oficio.json")
    print("VPS mirror written: /root/state/jugadas-por-oficio.json", len(flat["oficios"]), "oficios")
