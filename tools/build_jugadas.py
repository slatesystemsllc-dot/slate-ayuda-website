#!/usr/bin/env python3
# LIVE builder again (2026-09-15 rollback). build_jugadas_v2.py + plays.json are a DRAFT, not live: Dan rejected the short version.
# -*- coding: utf-8 -*-
"""build_jugadas.py: splits mas-clientes.html (the long leads guide) into a play-by-play site under jugadas/.
Dan 2026-09-15: "too long, they won't read it... a website with an initial catching page, then links to sections,
and CLEAR buttons to go home or next". The long page stays as "Leer todo"; this is GENERATED from it, never hand-edited.
Usage: python3 tools/build_jugadas.py   (run from the repo root; writes jugadas/index.html + jugadas/<n>.html)"""
import re, os, html, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = open(os.path.join(ROOT, "mas-clientes.html"), encoding="utf-8").read()
OUT = os.path.join(ROOT, "jugadas"); os.makedirs(OUT, exist_ok=True)

head = SRC[:SRC.index("<body>") + len("<body>")]
body = SRC[SRC.index("<body>") + len("<body>"):SRC.index("<script>")]
main_i = body.index("<main>")
onep_i = body.index('<section class="onepager">')
cover = body[:onep_i]                                   # the cover (stats, chips)
onepager = body[onep_i:main_i]                          # the 1-page plan (before <main> in the source)
main = body[main_i:]
caps = [m.start() for m in re.finditer(r'<h2 class="cap" id="', main)]
src_i = main.rfind("<div", 0, main.rindex("Fuentes"))
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
POR_OFICIO = json.load(open(os.path.join(ROOT, "tools", "jugadas_por_oficio.json"), encoding="utf-8"))
ID2N = {cid: k for k, (cid, _t, _s) in enumerate(chapters, 1)}
ID2T = {cid: t for (cid, t, _s) in chapters}
PO_JS = "<script>window.POR_OFICIO=%s;window.ID2N=%s;window.ID2T=%s;</script>" % (
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
  var q=new URLSearchParams(location.search);
  var of=(q.get('oficio')||'').trim().toLowerCase();
  if(of){ try{localStorage.setItem('oficio',of);}catch(e){} } else { try{of=localStorage.getItem('oficio')||'';}catch(e){} }
  ['negocio','tel','web'].forEach(function(k){ var v=q.get(k); if(v){ try{localStorage.setItem(k,v);}catch(e){} } });
  function get(k){ try{return localStorage.getItem(k)||'';}catch(e){return '';} }
  var PO=window.POR_OFICIO||{}, key='';
  function norm(v){ return String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim(); }
  var ofn=norm(of);
  if(ofn){ Object.keys(PO).forEach(function(k){ var kn=norm(k); if(!key && k!=='default' && (ofn.indexOf(kn)>=0 || kn.indexOf(ofn)>=0)) key=k; }); }
  var conf = key ? PO[key] : null;
  // fill the blanks that we know
  var fills={'[tu oficio]': key||'', '[Negocio]': get('negocio'), '[tu teléfono]': get('tel'), '[tu página]': get('web')};
  var main=document.querySelector('main'); 
  if(main){ var h=main.innerHTML, changed=false; Object.keys(fills).forEach(function(k){ if(fills[k]){ h=h.split(k).join(fills[k]); changed=true; } }); if(changed) main.innerHTML=h; }
  // the trade path on the landing
  var slot=document.getElementById('ruta'); 
  if(slot && conf){
    var ids=(conf.orden||[]).slice(0,5), n=window.ID2N||{}, t=window.ID2T||{};
    var html='<h3>Para tu oficio: '+key+'</h3><div class="rt">Empieza por estas 5, en este orden</div>';
    html+='<ol>'+ids.map(function(id){ return '<li><a href="'+n[id]+'.html">'+t[id]+'</a></li>'; }).join('')+'</ol>';
    if(conf.especial){ html+='<div class="esp"><b>Lo que solo tu oficio puede hacer:</b> '+conf.especial+'</div>'; }
    html+='<p style="font-size:13px;opacity:.85">Las demás jugadas están abajo. Todas sirven; estas cinco primero.</p>';
    slot.innerHTML=html; slot.hidden=false;
  }
  var nt=document.getElementById('oficio-note'); if(nt && key){ nt.textContent='Ejemplos para tu oficio: '+key+'.'; nt.hidden=false; }
})();
</script>
"""
OFICIOS = ["pintura","poda de árboles","acarreo","limpieza de basura","plomería","techos","jardinería","limpieza","clima","electricidad","handyman","pisos","concreto","cercas","lavado a presión","control de plagas","puertas de garaje","remodelación","reparación de electrodomésticos","cerrajería","mudanzas","detallado de autos","grúas","limpieza de ventanas","tablaroca","mecánico móvil","construcción","aislamiento"]
sel = '<p class="oficio">Los ejemplos dicen [pintura]. Pon tu oficio y se cambia en todas las jugadas: <select id="oficio"><option value="">[pintura] (cámbialo)</option>' + "".join('<option value="%s">%s</option>' % (o, o) for o in OFICIOS) + "</select></p>"

PRINTS = {
    "job": '<h3>Para imprimir, con tus datos</h3><div class="imprimir"><a href="imprimir/letrero.html">Letrero de jardín</a><a href="imprimir/colgante.html">Volante colgante</a><a href="imprimir/tarjeta.html">Tarjeta a mano</a></div>',
    "warm": '<h3>Para imprimir</h3><div class="imprimir"><a href="imprimir/lista-100.html">La hoja de 100 nombres</a></div>',
    "feeders": '<h3>Para imprimir, con tus datos</h3><div class="imprimir"><a href="imprimir/papeles.html">Tu hoja de papeles (una página)</a></div>',
}


def page(n, cid, title, seg):
    prev_href = "%d.html" % (n - 1) if n > 1 else "index.html"
    next_href = "%d.html" % (n + 1) if n < N else "index.html"
    next_lbl = "Siguiente jugada →" if n < N else "Volver al inicio"
    return (head.replace("<title>", "<title>Jugada %d de %d: " % (n, N)).replace("</head>", EXTRA_CSS + "</head>")
            + '\n<div class="jbar"><div class="wrap"><a href="index.html">← Inicio</a><span class="jprog">Jugada %d de %d</span><a href="../mas-clientes">Leer todo</a></div></div>\n' % (n, N)
            + '<main><div class="wrap">' + '<p class="oficio-note" id="oficio-note" hidden></p>' + seg + PRINTS.get(cid, "")
            + '</div></main>\n<div class="jnav"><div class="wrap"><a class="jbtn" href="%s">← Anterior</a><a class="jbtn primary" href="%s">%s</a></div></div>\n' % (prev_href, next_href, next_lbl)
            + script + PO_JS + JS + "</body></html>\n")

for k, (cid, title, seg) in enumerate(chapters, 1):
    html_k = page(k, cid, title, seg)
    open(os.path.join(OUT, "%d.html" % k), "w", encoding="utf-8").write(html_k)
    # SLUG-PAGES: the same page under its stable name (google.html, warm.html), so Alfred's links survive a reorder
    open(os.path.join(OUT, "%s.html" % cid), "w", encoding="utf-8").write(html_k)

items = "".join('<li><a href="%d.html"><span class="n">%d</span>%s</a></li>' % (k, k, html.escape(t)) for k, (cid, t, _) in enumerate(chapters, 1))
index = (head.replace("</head>", EXTRA_CSS + "</head>")
         + cover
         + '<main><div class="wrap">' + onepager.replace('<div class="semana1"', '<div class="ruta" id="ruta" hidden></div>\n<div class="semana1"', 1)
         + '<h2 class="cap" id="jugadas"><span class="capnum">→</span> Las jugadas, una por página</h2><p>Toca una. Cada página es una jugada completa con su guion para copiar. Al final, «Siguiente jugada».</p><ul class="jlist">%s</ul>' % (items)
         + '<p><a class="jbtn primary" href="1.html">Empezar por la jugada 1 →</a></p><p style="margin-top:10px"><a class="jbtn" href="../mas-clientes">Leer la guía completa en una sola página</a></p>'
         + '<details class="jsrc"><summary>Fuentes</summary>' + fuentes + '</details>'
         + '</div></main>' + script + PO_JS + JS + "</body></html>\n")
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(index)
print("jugadas/: index + %d pages" % N)
for k, (cid, t, seg) in enumerate(chapters, 1):
    print("  %2d %-10s %5d chars  %s" % (k, cid, len(seg), t))
