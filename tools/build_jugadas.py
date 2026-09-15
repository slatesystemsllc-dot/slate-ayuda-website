#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_jugadas.py: splits mas-clientes.html (the long leads guide) into a play-by-play site under jugadas/.
Dan 2026-09-15: "too long, they won't read it... a website with an initial catching page, then links to sections,
and CLEAR buttons to go home or next". The long page stays as "Leer todo"; this is GENERATED from it, never hand-edited.
Usage: python3 tools/build_jugadas.py   (run from the repo root; writes jugadas/index.html + jugadas/<n>.html)"""
import re, os, html
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
</style>
"""
JS = """
<script>
(function(){
  var q=new URLSearchParams(location.search);
  var of=q.get('oficio')||localStorage.getItem('oficio')||'';
  if(q.get('c')) localStorage.setItem('cid',q.get('c'));
  if(of){ localStorage.setItem('oficio',of);
    document.querySelectorAll('main, .cover').forEach(function(el){ el.innerHTML=el.innerHTML.replace(/\\[pintura\\]/g,of); });
    var s=document.getElementById('oficio'); if(s){ s.value=of; }
    var nt=document.getElementById('oficio-note'); if(nt){ document.getElementById('oficio-txt').textContent=of; nt.hidden=false; }
  }
  var s=document.getElementById('oficio'); if(s){ s.addEventListener('change',function(){ localStorage.setItem('oficio',s.value); location.reload(); }); }
})();
</script>
"""
OFICIOS = ["pintura","poda de árboles","acarreo","limpieza de basura","plomería","techos","jardinería","limpieza","clima","electricidad","handyman","pisos","concreto","cercas","lavado a presión","control de plagas","puertas de garaje","remodelación","reparación de electrodomésticos","cerrajería","mudanzas","detallado de autos","grúas","limpieza de ventanas","tablaroca","mecánico móvil","construcción","aislamiento"]
sel = '<p class="oficio">Los ejemplos dicen [pintura]. Pon tu oficio y se cambia en todas las jugadas: <select id="oficio"><option value="">[pintura] (cámbialo)</option>' + "".join('<option value="%s">%s</option>' % (o, o) for o in OFICIOS) + "</select></p>"

def page(n, cid, title, seg):
    prev_href = "%d.html" % (n - 1) if n > 1 else "index.html"
    next_href = "%d.html" % (n + 1) if n < N else "index.html"
    next_lbl = "Siguiente jugada →" if n < N else "Volver al inicio"
    return (head.replace("<title>", "<title>Jugada %d de %d: " % (n, N)).replace("</head>", EXTRA_CSS + "</head>")
            + '\n<div class="jbar"><div class="wrap"><a href="index.html">← Inicio</a><span class="jprog">Jugada %d de %d</span><a href="../mas-clientes">Leer todo</a></div></div>\n' % (n, N)
            + '<main><div class="wrap">' + '<p class="oficio-note" id="oficio-note" hidden>Ejemplos con tu oficio: <b id="oficio-txt"></b> · <a href="index.html#oficio">cambiar</a></p>' + seg
            + '</div></main>\n<div class="jnav"><div class="wrap"><a class="jbtn" href="%s">← Anterior</a><a class="jbtn primary" href="%s">%s</a></div></div>\n' % (prev_href, next_href, next_lbl)
            + script + JS + "</body></html>\n")

for k, (cid, title, seg) in enumerate(chapters, 1):
    open(os.path.join(OUT, "%d.html" % k), "w", encoding="utf-8").write(page(k, cid, title, seg))

items = "".join('<li><a href="%d.html"><span class="n">%d</span>%s</a></li>' % (k, k, html.escape(t)) for k, (cid, t, _) in enumerate(chapters, 1))
index = (head.replace("</head>", EXTRA_CSS + "</head>")
         + cover
         + '<main><div class="wrap">' + onepager + sel
         + '<h2 class="cap" id="jugadas"><span class="capnum">→</span> Las jugadas, una por página</h2><p>Toca una. Cada página es una jugada completa con su guion para copiar. Al final, «Siguiente jugada».</p><ul class="jlist">%s</ul>' % (items)
         + '<p><a class="jbtn primary" href="1.html">Empezar por la jugada 1 →</a></p><p style="margin-top:10px"><a class="jbtn" href="../mas-clientes">Leer la guía completa en una sola página</a></p>'
         + '<details class="jsrc"><summary>Fuentes</summary>' + fuentes + '</details>'
         + '</div></main>' + script + JS + "</body></html>\n")
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(index)
print("jugadas/: index + %d pages" % N)
for k, (cid, t, seg) in enumerate(chapters, 1):
    print("  %2d %-10s %5d chars  %s" % (k, cid, len(seg), t))
