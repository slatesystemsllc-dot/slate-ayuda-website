#!/usr/bin/env python3
# LIVE builder again (2026-09-15 rollback). build_jugadas_v2.py + plays.json are a DRAFT, not live: Dan rejected the short version.
# -*- coding: utf-8 -*-
"""build_jugadas.py: splits mas-clientes.html (the long leads guide) into a play-by-play site under jugadas/.
Dan 2026-09-15: "too long, they won't read it... a website with an initial catching page, then links to sections,
and CLEAR buttons to go home or next". The long page stays as "Leer todo"; this is GENERATED from it, never hand-edited.
Usage: python3 tools/build_jugadas.py   (run from the repo root; writes jugadas/index.html + jugadas/<n>.html)"""
import re, os, html, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BILINGUAL 2026-09-16 (Dan: "make the english version of this whole guide"). GUIDE_LANG=en builds the twin from the help
# repo: same builder, same markup, English strings. Trade keys stay Spanish (company_trade carries the Spanish slug);
# the EN pages show the English trade name from T_EN.
LANG = os.environ.get("GUIDE_LANG", "es")
CFG = {
  "es": dict(src="mas-clientes.html", out="jugadas", root=ROOT, long="../mas-clientes", print_dir="imprimir",
             title_pre="Jugada %d de %d: ", home="← Inicio", prog="Jugada %d de %d", readall="Leer todo",
             prev="← Anterior", nxt="Siguiente jugada →", back_home="Volver al inicio",
             route_h="Para tu oficio: ", route_sub="Empieza por estas 5, en este orden", route_esp="Lo que solo tu oficio puede hacer:",
             route_rest="Las demás jugadas están abajo. Todas sirven; estas cinco primero.", note="Ejemplos para tu oficio: ",
             print_h="Para imprimir, con tus datos", print_h2="Para imprimir", p_sign="Letrero de jardín", p_hang="Volante colgante",
             p_card="Tarjeta a mano", p_list="La hoja de 100 nombres", p_docs="Tu hoja de papeles (una página)",
             list_h="Las jugadas, una por página", list_p="Toca una. Cada página es una jugada completa con su guion para copiar. Al final, «Siguiente jugada».",
             week="¿Acabas de empezar? Tu primera semana, día por día →", start="Empezar por la jugada 1 →", readlong="Leer la guía completa en una sola página",
             sources="Fuentes", fill_trade="[tu oficio]", fill_biz="[Negocio]", fill_tel="[tu teléfono]", fill_web="[tu página]"),
  "en": dict(src="more-jobs.html", out="plays", root=os.path.expanduser("~/slate-help-repo"), long="../more-jobs", print_dir="print",
             title_pre="Play %d of %d: ", home="← Home", prog="Play %d of %d", readall="Read it all",
             prev="← Previous", nxt="Next play →", back_home="Back to the start",
             route_h="For your trade: ", route_sub="Start with these 5, in this order", route_esp="What only your trade can do:",
             route_rest="The other plays are below. They all work; these five first.", note="Examples for your trade: ",
             print_h="Print, with your data", print_h2="Print", p_sign="Yard sign", p_hang="Door hanger",
             p_card="Handwritten card", p_list="The 100-name sheet", p_docs="Your paperwork sheet (one page)",
             list_h="The plays, one per page", list_p="Tap one. Each page is a complete play with the script to copy. At the end, \u201cNext play\u201d.",
             week="Just starting? Your first week, day by day →", start="Start with play 1 →", readlong="Read the whole guide on one page",
             sources="Sources", fill_trade="[your trade]", fill_biz="[Company]", fill_tel="[your phone]", fill_web="[your website]"),
}[LANG]
ROOT = CFG["root"]
SRC = open(os.path.join(ROOT, CFG["src"]), encoding="utf-8").read()
OUT = os.path.join(ROOT, CFG["out"]); os.makedirs(OUT, exist_ok=True)
T_EN = {"pintura":"painting","poda de árboles":"tree service","acarreo":"junk removal","limpieza de basura":"junk removal","plomería":"plumbing","techos":"roofing","jardinería y paisajismo":"landscaping","limpieza":"cleaning","climas y calefacción":"HVAC","instalaciones eléctricas":"electrical","handyman":"handyman","pisos":"flooring","concreto":"concrete","cercas":"fencing","control de plagas":"pest control","remodelación":"remodeling","construcción general":"general contracting","aislamiento":"insulation","pavimento y asfalto":"paving","constructores de casas":"home building","ventanas y puertas":"windows and doors","solar":"solar","terrazas y patios":"decks and patios"}

head = SRC[:SRC.index("<body>") + len("<body>")]
body = SRC[SRC.index("<body>") + len("<body>"):SRC.index("<script>")]
main_i = body.index("<main>")
onep_i = body.index('<section class="onepager">')
cover = body[:onep_i]                                   # the cover (stats, chips)
# 2026-09-16 Dan: the front page read like a Frankenstein. The play index keeps title, one line, the three numbers.
cover = re.sub(r'<p class="tag">.*?</p>\s*', '', cover, flags=re.S)
cover = re.sub(r'<div class="alltrades">.*?</div>\s*', '', cover, flags=re.S)
onepager = body[onep_i:main_i]                          # the 1-page plan (before <main> in the source)
main = body[main_i:]
caps = [m.start() for m in re.finditer(r'<h2 class="cap" id="', main)]
src_i = main.rfind("<div", 0, main.rindex(CFG["sources"]))
chapters = []
for k, s in enumerate(caps):
    e = caps[k + 1] if k + 1 < len(caps) else src_i
    seg = main[s:e]
    cid = re.search(r'id="([^"]+)"', seg).group(1)
    title = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<h2[^>]*>(.*?)</h2>", seg, re.S).group(1))).strip()
    title = re.sub(r"^\d+\s*", "", title)
    chapters.append((cid, title, seg))
fuentes = main[src_i:main.rindex("</main>")]
script = SRC[SRC.index("<script>"):SRC.index("</script>") + len("</script>")]
N = len(chapters)
# PERSONAL-2026-09-15: per-trade order + special play, read from tools/jugadas_por_oficio.json (Alfred reads the same file)
POR_OFICIO = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "jugadas_por_oficio.json"), encoding="utf-8"))
if LANG == "en":
    for _k, _v in POR_OFICIO.items():
        if isinstance(_v, dict) and _v.get("especial_en"): _v["especial"] = _v["especial_en"]
ID2N = {cid: k for k, (cid, _t, _s) in enumerate(chapters, 1)}
ID2T = {cid: t for (cid, t, _s) in chapters}
PO_JS = "<script>window.CFG=%s;window.T_EN=%s;</script>" % (json.dumps({k: CFG[k] for k in ("route_h","route_sub","route_esp","route_rest","note","fill_trade","fill_biz","fill_tel","fill_web")}, ensure_ascii=False), json.dumps(T_EN if LANG == "en" else {}, ensure_ascii=False)) + "<script>window.POR_OFICIO=%s;window.ID2N=%s;window.ID2T=%s;</script>" % (
    json.dumps({k: v for k, v in POR_OFICIO.items() if not k.startswith("_")}, ensure_ascii=False), json.dumps(ID2N), json.dumps(ID2T, ensure_ascii=False))

EXTRA_CSS = """
<style>
  .jbar{position:sticky;top:0;z-index:9;background:var(--navy);color:#fff;padding:14px 0}
  main .wrap > h2.cap{margin-top:26px}
  main .wrap > .h2sub{margin-bottom:22px}
  main .wrap h3{margin-top:28px}
  .bulb{margin:18px 0 22px}
  .script{margin:14px 0 18px}
  .warn,.win,.slateline{margin:18px 0}
  .oficio-note{margin:14px 0 0;font-size:14px;color:#5b6472}
  .oficio-note a{color:var(--orange);font-weight:800}
  .jbar .wrap{display:flex;align-items:center;justify-content:space-between;gap:10px}
  .jbar a{color:#fff;text-decoration:none;font-weight:800}
  .jprog{font-size:13px;color:var(--gold);font-weight:800;letter-spacing:.12em;text-transform:uppercase}
  .jnav{position:sticky;bottom:0;background:#fff;border-top:2px solid #e6e9ef;padding:12px 0;margin-top:28px}
  .jnav .wrap{display:flex;gap:10px}
  .jbtn{flex:1;display:block;text-align:center;padding:16px 12px;border-radius:12px;font-weight:900;font-size:17px;text-decoration:none;border:2px solid var(--navy);color:var(--navy);background:#fff}
  .jbtn.primary{background:var(--navy);color:#fff}
  .jbtn.done{background:#e9f7ee;border-color:#1f8a4c;color:#1f8a4c}
  .jlist{list-style:none;padding:0;margin:18px 0}
  .jlist li a{display:flex;align-items:center;gap:14px;padding:16px;margin:10px 0;border:2px solid #e6e9ef;border-radius:14px;text-decoration:none;color:var(--ink);font-weight:800;font-size:17px;background:#fff}
  .jlist .n{width:36px;height:36px;border-radius:50%;background:var(--navy);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;flex:none}
  .jlist .ok{margin-left:auto;color:#1f8a4c;font-weight:900}
  .oficio{margin:14px 0 0;font-size:15px}
  .oficio select{font-size:16px;padding:8px 10px;border-radius:8px;border:2px solid #cfd6e0}
  .jsrc{font-size:13px;color:#5b6472}
  .jsrc summary{cursor:pointer;font-weight:800;color:var(--ink)}
  .ruta{background:var(--navy);color:#fff;border-radius:14px;padding:18px 18px 8px;margin:18px 0}
  .ruta h3{color:var(--gold);margin:0 0 6px;font-size:14px;letter-spacing:.12em;text-transform:uppercase}
  .ruta .rt{font-size:20px;font-weight:900;margin:0 0 10px}
  .ruta ol{margin:0 0 10px;padding-left:22px}
  .ruta li{margin:6px 0}
  .ruta a{color:#fff;font-weight:800}
  .ruta .esp{background:rgba(255,255,255,.08);border-left:4px solid var(--orange);padding:10px 12px;border-radius:8px;margin:8px 0 12px;font-size:15px}
  .ruta .esp b{color:var(--gold)}
  .oficio-note{margin:14px 0 0;font-size:14px;color:#5b6472}
  .imprimir{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 18px}
  .imprimir a{flex:1 1 160px;text-align:center;padding:12px;border:2px solid var(--orange);border-radius:10px;color:var(--ink);font-weight:800;text-decoration:none;background:#fff}
</style>
"""
JS = """
<script>
(function(){
  // PERSONAL-2026-09-15: the link brings the trade (?oficio=pintura). Nothing to click. No trade = the general guide.
  // 2026-09-16: GHL writes the colors as '#0549AE', and '#' starts the URL fragment, so everything after c1= lands in
  // location.hash (c2, logo, ciudad included). Read search + hash as one string; URLSearchParams alone lost them (Jorge's
  // sign printed with Slate colors and no logo).
  var raw=(location.search||'')+(location.hash||'');
  function grab(k){ var m=raw.match(new RegExp('[?&#]'+k+'=([^&#]*)')); return m?decodeURIComponent(m[1].split('+').join(' ')):''; }
  var of=grab('oficio').trim().toLowerCase();
  if(of){ try{localStorage.setItem('oficio',of);}catch(e){} } else { try{of=localStorage.getItem('oficio')||'';}catch(e){} }
  ['negocio','tel','web','logo','ciudad'].forEach(function(k){ var v=grab(k); if(v){ try{localStorage.setItem(k,v);}catch(e){} } });
  var hx=raw.match(/c1=(?:%23|#)?([0-9a-fA-F]{6})/); if(hx){ try{localStorage.setItem('c1','#'+hx[1]);}catch(e){} }
  var hy=raw.match(/c2=(?:%23|#)?([0-9a-fA-F]{6})/); if(hy){ try{localStorage.setItem('c2','#'+hy[1]);}catch(e){} }
  function get(k){ try{return localStorage.getItem(k)||'';}catch(e){return '';} }
  var PO=window.POR_OFICIO||{}, key='';
  function norm(v){ return String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim(); }
  var ofn=norm(of);
  if(ofn){ Object.keys(PO).forEach(function(k){ var kn=norm(k); if(!key && k!=='default' && (ofn.indexOf(kn)>=0 || kn.indexOf(ofn)>=0)) key=k; }); }
  var conf = key ? PO[key] : null;
  // fill the blanks that we know
  var fills={}; fills[CFG.fill_trade]=key?(T_EN[key]||key):''; fills[CFG.fill_biz]=get('negocio'); fills[CFG.fill_tel]=get('tel'); fills[CFG.fill_web]=get('web');
  var main=document.querySelector('main'); 
  if(main){ var h=main.innerHTML, changed=false; Object.keys(fills).forEach(function(k){ if(fills[k]){ h=h.split(k).join(fills[k]); changed=true; } }); if(changed) main.innerHTML=h; }
  // the trade path on the landing
  var slot=document.getElementById('ruta'); 
  if(slot && conf){
    var ids=(conf.orden||[]).slice(0,5), n=window.ID2N||{}, t=window.ID2T||{};
    var html='<h3>'+CFG.route_h+(T_EN[key]||key)+'</h3><div class="rt">'+CFG.route_sub+'</div>';
    html+='<ol>'+ids.map(function(id){ return '<li><a href="'+n[id]+'.html">'+t[id]+'</a></li>'; }).join('')+'</ol>';
    if(conf.especial){ html+='<div class="esp"><b>'+CFG.route_esp+'</b> '+conf.especial+'</div>'; }
    html+='<p style="font-size:13px;opacity:.85">'+CFG.route_rest+'</p>';
    slot.innerHTML=html; slot.hidden=false;
  }
  var nt=document.getElementById('oficio-note'); if(nt && key){ nt.textContent=CFG.note+(T_EN[key]||key)+'.'; nt.hidden=false; }
})();
</script>
"""
OFICIOS = ["pintura","poda de árboles","acarreo","limpieza de basura","plomería","techos","jardinería","limpieza","clima","electricidad","handyman","pisos","concreto","cercas","lavado a presión","control de plagas","puertas de garaje","remodelación","reparación de electrodomésticos","cerrajería","mudanzas","detallado de autos","grúas","limpieza de ventanas","tablaroca","mecánico móvil","construcción","aislamiento"]
sel = '<p class="oficio">Los ejemplos dicen [pintura]. Pon tu oficio y se cambia en todas las jugadas: <select id="oficio"><option value="">[pintura] (cámbialo)</option>' + "".join('<option value="%s">%s</option>' % (o, o) for o in OFICIOS) + "</select></p>"

PRINTS = {
    "job": '<h3>%(print_h)s</h3><div class="imprimir"><a href="%(print_dir)s/letrero.html">%(p_sign)s</a><a href="%(print_dir)s/colgante.html">%(p_hang)s</a><a href="%(print_dir)s/tarjeta.html">%(p_card)s</a></div>' % CFG,
    "warm": '<h3>%(print_h2)s</h3><div class="imprimir"><a href="%(print_dir)s/lista-100.html">%(p_list)s</a></div>' % CFG,
    "feeders": '<h3>%(print_h)s</h3><div class="imprimir"><a href="%(print_dir)s/papeles.html">%(p_docs)s</a></div>' % CFG,
}


def page(n, cid, title, seg):
    prev_href = "%d.html" % (n - 1) if n > 1 else "index.html"
    next_href = "%d.html" % (n + 1) if n < N else "index.html"
    next_lbl = CFG["nxt"] if n < N else CFG["back_home"]
    return (head.replace("<title>", "<title>" + CFG["title_pre"] % (n, N)).replace("</head>", EXTRA_CSS + "</head>")
            + '\n<div class="jbar"><div class="wrap"><a href="index.html">%s</a><span class="jprog">%s</span><a href="%s">%s</a></div></div>\n' % (CFG["home"], CFG["prog"] % (n, N), CFG["long"], CFG["readall"])
            + '<main><div class="wrap">' + '<p class="oficio-note" id="oficio-note" hidden></p>' + seg + PRINTS.get(cid, "") + (('<hr style="border:0;border-top:2px solid var(--line);margin:28px 0">' + onepager) if cid == "rhythm" else "")
            + '</div></main>\n<div class="jnav"><div class="wrap"><a class="jbtn" href="%s">%s</a><a class="jbtn primary" href="%s">%s</a></div></div>\n' % (prev_href, CFG["prev"], next_href, next_lbl)
            + script + PO_JS + JS + "</body></html>\n")

for k, (cid, title, seg) in enumerate(chapters, 1):
    html_k = page(k, cid, title, seg)
    open(os.path.join(OUT, "%d.html" % k), "w", encoding="utf-8").write(html_k)
    # SLUG-PAGES: the same page under its stable name (google.html, warm.html), so Alfred's links survive a reorder
    open(os.path.join(OUT, "%s.html" % cid), "w", encoding="utf-8").write(html_k)

items = "".join('<li><a href="%d.html"><span class="n">%d</span>%s</a></li>' % (k, k, html.escape(t)) for k, (cid, t, _) in enumerate(chapters, 1))
index = (head.replace("</head>", EXTRA_CSS + "</head>")
         + cover
         + '<main><div class="wrap"><div class="ruta" id="ruta" hidden></div>'
         + '<h2 class="cap" id="jugadas"><span class="capnum">→</span> %s</h2><p>%s</p><ul class="jlist">%s</ul>' % (CFG["list_h"], CFG["list_p"], items)
         + '<p><a class="jbtn" href="14.html#semana1">%s</a></p>' % CFG["week"]
         + '<p><a class="jbtn primary" href="1.html">%s</a></p><p style="margin-top:10px"><a class="jbtn" href="%s">%s</a></p>' % (CFG["start"], CFG["long"], CFG["readlong"])
         + '<details class="jsrc"><summary>%s</summary>' % CFG["sources"] + fuentes + '</details>'
         + '</div></main>' + script + PO_JS + JS + "</body></html>\n")
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(index)
print("%s/: index + %d pages" % (CFG["out"], N))
for k, (cid, t, seg) in enumerate(chapters, 1):
    print("  %2d %-10s %5d chars  %s" % (k, cid, len(seg), t))
