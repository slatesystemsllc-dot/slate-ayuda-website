#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_jugadas_v2.py: tools/plays.json (14 one-screen plays, third-grade Spanish) -> jugadas/ (index + N.html + <id>.html).
Dan 2026-09-15: "3rd grade level, SIMPLE and effective, short and sweet, worth MONEY". One screen per play: what you do,
why (one number, its source), three steps, what to say (copy), do this today. The long guide stays at /mas-clientes as
"leer todo". Personalization by link only: ?oficio=&negocio=&tel=&web=&c1=&c2= (from the links page button); no data = the
general guide. Trade route from tools/jugadas_por_oficio.json; trade cards from plays.json "oficios". Never hand-edit output."""
import json, os, html, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "tools", "plays.json"), encoding="utf-8"))
PO = json.load(open(os.path.join(ROOT, "tools", "jugadas_por_oficio.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "jugadas"); os.makedirs(OUT, exist_ok=True)
plays = D["plays"]; N = len(plays); META = D["meta"]
ID2N = {p["id"]: p["n"] for p in plays}; ID2T = {p["id"]: p["titulo"] for p in plays}
PO_JS = "<script>window.POR_OFICIO=%s;window.ID2N=%s;window.ID2T=%s;window.OFICIOS=%s;</script>" % (
    json.dumps({k: v for k, v in PO.items() if not k.startswith("_")}, ensure_ascii=False), json.dumps(ID2N),
    json.dumps(ID2T, ensure_ascii=False), json.dumps(D.get("oficios", {}), ensure_ascii=False))
E = html.escape
IMPR = {"letrero": "Letrero de jardín", "colgante": "Volante colgante", "tarjeta": "Tarjeta a mano", "lista-100": "La hoja de 100 nombres", "papeles": "Tu hoja de papeles"}

CSS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root{--navy:#152a45;--orange:#ee7000;--ink:#1c2733;--sub:#5b6673;--line:#e5e9ee;--soft:#f5f7fa;--gold:#ffb066;--red:#b42318}
*{box-sizing:border-box}body{font-family:Inter,-apple-system,sans-serif;color:var(--ink);background:var(--soft);margin:0;line-height:1.5;font-size:17px}
.wrap{max-width:720px;margin:0 auto;padding:0 18px}
.bar{position:sticky;top:0;z-index:9;background:var(--navy);color:#fff;padding:14px 0}.bar .wrap{display:flex;align-items:center;justify-content:space-between;gap:10px}.bar a{color:#fff;font-weight:800;text-decoration:none}.bar .p{font-size:12px;color:var(--gold);font-weight:800;letter-spacing:.14em;text-transform:uppercase}
h1{font-size:clamp(28px,7vw,40px);line-height:1.08;margin:22px 0 8px;font-weight:900;letter-spacing:-.5px}
.sub{color:var(--sub);font-size:17px;margin:0 0 18px}
.k{font-size:12px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:var(--orange);margin:22px 0 6px}
.que{font-size:clamp(20px,5vw,24px);font-weight:800;line-height:1.3;margin:0}
.por{background:#fff;border:2px solid var(--navy);border-radius:14px;padding:14px 16px;margin:6px 0 0}.por .n{font-size:17px;font-weight:700}.por .f{display:block;font-size:13px;color:var(--sub);margin-top:6px}
ol.pasos{margin:6px 0 0;padding-left:26px}ol.pasos li{margin:8px 0;font-size:18px;font-weight:600}
.di{background:#fff;border-left:5px solid var(--orange);border-radius:0 12px 12px 0;padding:12px 14px;margin:6px 0 0;position:relative}.di .et{font-size:12px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;color:var(--orange)}.di .tx{margin:6px 0 0;font-size:17px}.di button{position:absolute;right:10px;top:10px;background:#fff;border:2px solid var(--navy);border-radius:8px;padding:6px 12px;font-weight:800;font-size:13px;color:var(--navy)}
.hoy{background:var(--navy);color:#fff;border-radius:14px;padding:16px;margin:6px 0 0;font-size:18px;font-weight:700}.hoy .k{color:var(--gold);margin:0 0 6px}
.meta{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 0}.meta span{background:#fff;border:1px solid var(--line);border-radius:99px;padding:6px 12px;font-size:14px;font-weight:700}
.aviso{background:#fff3f1;border-left:5px solid var(--red);padding:12px 14px;border-radius:0 12px 12px 0;margin:14px 0 0;font-size:16px}
.slate{display:flex;gap:10px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:14px 0 0;font-size:15px;color:var(--sub)}.slate b{color:var(--navy)}.slate .dot{flex:none;width:22px;height:22px;border-radius:6px;background:var(--navy);color:var(--gold);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:12px}
.imprimir{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0 0}.imprimir a{flex:1 1 150px;text-align:center;padding:12px;border:2px solid var(--orange);border-radius:10px;color:var(--ink);font-weight:800;text-decoration:none;background:#fff}
.nav{position:sticky;bottom:0;background:#fff;border-top:2px solid var(--line);padding:12px 0;margin-top:28px}.nav .wrap{display:flex;gap:10px}.btn{flex:1;display:block;text-align:center;padding:16px 12px;border-radius:12px;font-weight:900;font-size:17px;text-decoration:none;border:2px solid var(--navy);color:var(--navy);background:#fff}.btn.primary{background:var(--navy);color:#fff}
.cover{background:linear-gradient(160deg,var(--navy) 0%,#1e3a5f 100%);color:#fff;padding:34px 0 26px}.cover h1{margin:8px 0}.cover .sub{color:#c7d2e0}.cover .chip{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);border:1px solid rgba(255,176,102,.45);border-radius:99px;padding:6px 14px}
.reglas{background:#fff;border-radius:14px;padding:6px 16px;margin:18px 0}.reglas p{margin:12px 0;font-size:17px;font-weight:700}.reglas b{color:var(--orange);margin-right:6px}
.hoy20{background:#fff8ec;border:2px solid var(--orange);border-radius:14px;padding:14px 16px;margin:14px 0;font-size:17px}.hoy20 b{color:var(--orange)}
.semana{background:#fff;border-radius:14px;padding:12px 16px;margin:14px 0}.semana h3{margin:6px 0 8px;font-size:16px}.semana ol{margin:0;padding-left:22px}.semana li{margin:6px 0;font-size:16px}
.ruta{background:var(--navy);color:#fff;border-radius:14px;padding:16px 18px 10px;margin:14px 0}.ruta .k{color:var(--gold);margin:0 0 4px}.ruta .rt{font-size:19px;font-weight:900;margin:0 0 8px}.ruta ol{margin:0 0 8px;padding-left:22px}.ruta li{margin:6px 0}.ruta a{color:#fff;font-weight:800}.ruta .esp{background:rgba(255,255,255,.08);border-left:4px solid var(--orange);padding:10px 12px;border-radius:8px;margin:8px 0 10px;font-size:15px}.ruta .esp b{color:var(--gold)}
ul.lista{list-style:none;padding:0;margin:14px 0}ul.lista li a{display:flex;align-items:center;gap:14px;padding:14px 16px;margin:8px 0;border:2px solid var(--line);border-radius:14px;text-decoration:none;color:var(--ink);font-weight:800;font-size:17px;background:#fff}ul.lista .n{width:34px;height:34px;border-radius:50%;background:var(--navy);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;flex:none}
.foot{color:var(--sub);font-size:14px;margin:22px 0 30px}
</style>'''
JS = '''<script>
function cp(b){var t=b.parentElement.querySelector('.tx').innerText;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){var o=b.innerText;b.innerText='¡Copiado!';setTimeout(function(){b.innerText=o},1600)},function(){var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(ta);b.innerText='¡Copiado!'});}
(function(){
  var raw=(location.search||'')+(location.hash||'');
  function grab(k){var m=raw.match(new RegExp('[?&#]'+k+'=([^&#]*)'));return m?decodeURIComponent(m[1].replace(/\\+/g,' ')):'';}
  ['oficio','negocio','tel','web'].forEach(function(k){var v=grab(k);if(v){try{localStorage.setItem(k,v)}catch(e){}}});
  var hx=raw.match(/c1=%23?#?([0-9a-fA-F]{6})/);if(hx){try{localStorage.setItem('c1','#'+hx[1])}catch(e){}}
  var hy=raw.match(/c2=%23?#?([0-9a-fA-F]{6})/);if(hy){try{localStorage.setItem('c2','#'+hy[1])}catch(e){}}
  function g(k){try{return localStorage.getItem(k)||''}catch(e){return ''}}
  function norm(v){return String(v||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
  var of=norm(g('oficio')), PO=window.POR_OFICIO||{}, key='';
  if(of){Object.keys(PO).forEach(function(k){var kn=norm(k);if(!key&&k!=='default'&&(of.indexOf(kn)>=0||kn.indexOf(of)>=0))key=k;});}
  var fills={'[tu oficio]':key||'','[Negocio]':g('negocio'),'[tu teléfono]':g('tel'),'[tu página]':g('web')};
  var main=document.querySelector('main');if(main){var h=main.innerHTML,ch=false;Object.keys(fills).forEach(function(k){if(fills[k]){h=h.split(k).join(fills[k]);ch=true;}});if(ch)main.innerHTML=h;}
  var slot=document.getElementById('ruta'),conf=key?PO[key]:null,OF=(window.OFICIOS||{})[key];
  if(slot&&conf){var ids=(conf.orden||[]).slice(0,5),n=window.ID2N||{},t=window.ID2T||{};
    var x='<div class="k">Para tu oficio: '+key+'</div><div class="rt">Empieza por estas 5, en este orden</div><ol>'+ids.map(function(id){return '<li><a href="'+n[id]+'.html">'+t[id]+'</a></li>';}).join('')+'</ol>';
    var esp=(OF&&OF.especial)||conf.especial;if(esp){x+='<div class="esp"><b>Lo que solo tu oficio puede hacer:</b> '+esp+'</div>';}
    if(OF&&OF.socios){x+='<div class="esp"><b>Tus socios:</b> '+OF.socios+'</div>';}
    slot.innerHTML=x;slot.hidden=false;}
  var card=document.getElementById('oficio-card');if(card&&OF){card.innerHTML='<div class="k">Para tu oficio: '+key+'</div><p><b>Tus socios:</b> '+OF.socios+'</p><p><b>Lo que solo tu oficio puede hacer:</b> '+OF.especial+'</p>';}
  var pf=document.getElementById('print-links');if(pf){var qs='';['oficio','negocio','tel','web','c1','c2'].forEach(function(k){var v=g(k);if(v)qs+=(qs?'&':'?')+k+'='+encodeURIComponent(v);});pf.querySelectorAll('a').forEach(function(a){a.href=a.getAttribute('href')+qs;});}
})();
</script>'''
def head(title):
    return '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>%s</head><body>' % (E(title), CSS)
def page(p):
    n = p["n"]; prev_ = "%d.html" % (n - 1) if n > 1 else "index.html"; next_ = "%d.html" % (n + 1) if n < N else "index.html"
    b = head("Jugada %d: %s" % (n, p["titulo"]))
    b += '<div class="bar"><div class="wrap"><a href="index.html">← Inicio</a><span class="p">Jugada %d de %d</span><a href="../mas-clientes">Leer todo</a></div></div><main><div class="wrap">' % (n, N)
    b += '<h1>%s</h1>' % E(p["titulo"])
    b += '<div class="k">Qué haces</div><p class="que">%s</p>' % E(p["que"])
    b += '<div class="k">Por qué</div><div class="por"><div class="n">%s</div><span class="f">Fuente: %s</span></div>' % (E(p["por_que"]), E(p["fuente"]))
    if p["id"] == "partners": b += '<div class="por" id="oficio-card" style="margin-top:14px"><div class="k" style="margin:0 0 6px">Tu tarjeta de oficio</div><p style="margin:0">Abre esta guía desde el botón naranja de tu página de enlaces y aquí aparece tu oficio, con sus socios.</p></div>'
    b += '<div class="k">Cómo</div><ol class="pasos">%s</ol>' % "".join("<li>%s</li>" % E(s) for s in p["pasos"])
    if p.get("di_esto"):
        b += '<div class="k">Di esto</div><div class="di"><button onclick="cp(this)">Copiar</button><div class="et">%s</div><div class="tx">%s</div></div>' % (E(p["di_esto"]["etiqueta"]), E(p["di_esto"]["texto"]))
    b += '<div class="hoy"><div class="k">Hoy</div>%s</div>' % E(p["hoy"])
    b += '<div class="meta"><span>⏱ %s</span></div>' % E(p["tiempo"])
    if p.get("aviso"): b += '<div class="aviso"><b>Ojo:</b> %s</div>' % E(p["aviso"])
    if p.get("slate"): b += '<div class="slate"><div class="dot">S</div><div><b>Tu sistema ya hace esto:</b> %s</div></div>' % E(p["slate"])
    if p.get("imprimir"): b += '<div class="k">Para imprimir, con tus datos</div><div class="imprimir" id="print-links">%s</div>' % "".join('<a href="imprimir/%s.html">%s</a>' % (k, IMPR[k]) for k in p["imprimir"])
    b += '</div></main><div class="nav"><div class="wrap"><a class="btn" href="%s">← Anterior</a><a class="btn primary" href="%s">%s</a></div></div>' % (prev_, next_, "Siguiente jugada →" if n < N else "Volver al inicio")
    return b + PO_JS + JS + "</body></html>\n"
for p in plays:
    h = page(p)
    open(os.path.join(OUT, "%d.html" % p["n"]), "w", encoding="utf-8").write(h)
    open(os.path.join(OUT, "%s.html" % p["id"]), "w", encoding="utf-8").write(h)
idx = head(META["title"])
idx += '<div class="cover"><div class="wrap"><span class="chip">Una guía de Slate Systems</span><h1>%s</h1><p class="sub">%s</p></div></div><main><div class="wrap">' % (E(META["title"]), E(META["sub"]))
idx += '<div class="reglas">%s</div>' % "".join('<p><b>%d.</b> %s</p>' % (i, E(r)) for i, r in enumerate(META["reglas"], 1))
idx += '<div class="hoy20"><b>Hoy, en 20 minutos:</b> %s</div>' % E(META["hoy20"])
idx += '<div class="ruta" id="ruta" hidden></div>'
idx += '<div class="semana"><h3>Si acabas de empezar: la primera semana</h3><ol>%s</ol></div>' % "".join("<li>%s</li>" % E(s) for s in META["semana1"])
idx += '<div class="k">Las jugadas, una por pantalla</div><ul class="lista">%s</ul>' % "".join('<li><a href="%d.html"><span class="n">%d</span>%s</a></li>' % (p["n"], p["n"], E(p["titulo"])) for p in plays)
idx += '<a class="btn primary" href="1.html">Empezar por la jugada 1 →</a><p class="foot">La versión larga, con todas las fuentes: <a href="../mas-clientes">leer todo</a>. Hecho por Slate Systems, 2026.</p>'
idx += '</div></main>' + PO_JS + JS + "</body></html>\n"
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(idx)
print("jugadas v2: index + %d plays" % N)
