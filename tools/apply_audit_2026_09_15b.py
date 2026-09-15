#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apply_audit_2026_09_15b.py: Dan 2026-09-15 "category and LLC name are our internal stuff, we do their GBP, out of scope".
The Google chapter keeps only what the CLIENT does (ask the review in person, reply to reviews, no discount for reviews);
the profile setup (category, name, services, photos, position) is named as Slate's job. The "hoy en 20 minutos" box
becomes a client action. Idempotent (marker AUDIT-2026-09-15b)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "mas-clientes.html"); s = open(P, encoding="utf-8").read()
if "AUDIT-2026-09-15b" in s: raise SystemExit("ya aplicado")
def sub1(a, b, name):
    global s
    n = s.count(a)
    if n != 1: raise SystemExit("ANCLA x%d: %s" % (n, name))
    s = s.replace(a, b)
# the box
sub1('''<div class="win" id="hoy20"><b>Hoy, en 20 minutos, antes que todo lo demás:</b> abre tu perfil de Google y revisa dos cosas. Que el nombre del negocio sea exactamente el de tu LLC. Y que la categoría principal sea la misma que usan los tres negocios que salen arriba cuando buscas tu oficio más tu ciudad. Esas dos cosas son el factor número uno del ranking local, y las cambias en un minuto. El capítulo 2 te lleva paso a paso.</div>''',
     '''<div class="win" id="hoy20"><b>Hoy, en 20 minutos, antes que todo lo demás:</b> teléfono en mano, escribe en papel los primeros 30 nombres de tu lista de 100 (capítulo 3) y mándale el texto de anuncio a los primeros 10. Mañana, otros 10. Tu perfil de Google ya lo tenemos cuidado nosotros; lo tuyo es que la gente diga tu nombre.</div>''', "box")
# the Google chapter: client actions only
i = s.index('<h2 class="cap" id="google">'); j = s.index('<h2 class="cap" id="warm">')
GOOGLE = '''<h2 class="cap" id="google"><span class="capnum">2</span> Tu perfil de Google: nosotros lo armamos, tú lo alimentas</h2>
<p class="h2sub">Cada letrero, cada vecino, cada etiqueta en Facebook manda a esa persona a buscarte en Google. El perfil (nombre, categoría, servicios, zona, fotos, posición en el mapa) lo cuidamos nosotros. Lo que solo tú puedes hacer son dos cosas.</p>
<div class="bulb"><div class="big">74%</div><div class="txt">de la gente solo lee reseñas de los últimos tres meses. Las reseñas se echan a perder: por eso la petición es en cada trabajo, no una vez.<span class="src">BrightLocal, encuesta de consumidores 2026</span></div></div>
<h3>1. La reseña se pide en persona, antes de subirte al camión</h3>
<div class="script"><button class="copybtn" onclick="cp(this)">Copiar</button><span class="lang">Español, dilo en persona</span><span class="cptext">Me da mucho gusto que haya quedado contento. Le voy a mandar un mensajito de texto con un enlace para dejarnos una reseña en Google. Son treinta segundos y a un negocio como el mío le ayuda muchísimo. Si quiere, lo abrimos aquí mismo y yo le muestro dónde darle.</span></div>
<p>El momento lo es todo: si no saca el teléfono mientras todavía estás ahí parado, casi nunca pasa después. Tu sistema manda el enlace solo; tu trabajo es avisar de frente.</p>
<div class="warn"><b>Nunca ofrezcas descuento a cambio de una reseña.</b> Google lo prohíbe. Cuando lo detecta borra todas las reseñas de un jalón y puede marcar el perfil. Se pide, no se compra.</div>
<h3>2. Contesta las reseñas, las buenas y las malas</h3>
<p>El 89% de la gente espera que el dueño conteste, y el 80% es más propenso a contratar a un negocio que contesta todas. Dos renglones bastan: gracias por el nombre, y qué trabajo fue. A una mala, sin pelear: "Lamento que quedara así. Le llamo hoy para arreglarlo". Si prefieres, nos dices y las contestamos nosotros con tu voz.</p>
<div class="slateline"><div class="dot">S</div><div><b>Lo que ya hace tu sistema de Slate:</b> el perfil bien armado, las fotos de tus trabajos, la posición en el mapa vigilada cada semana, y el enlace de reseña que sale solo después de cada trabajo. No tienes que tocar el perfil.</div></div>
'''
s = s[:i] + GOOGLE + s[j:]
# sources: drop the Whitespark line (internal, moved to the wiki GBP checklist)
sub1('<li>Whitespark Local Search Ranking Factors 2026 (categoría principal = factor #1) · Jobber 2026', '<li>Jobber 2026', "srcs")
s = s.replace('/* AUDIT-2026-09-15: phone width', '/* AUDIT-2026-09-15 + AUDIT-2026-09-15b: phone width')
open(P, "w", encoding="utf-8").write(s); print("applied b")
