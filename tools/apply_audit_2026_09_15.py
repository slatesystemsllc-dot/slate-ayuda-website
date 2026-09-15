#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apply_audit_2026_09_15.py: applies the 2026-09-15 audit (slate-ghl/leads-guide-audit-2026-09-15/research.md) to
mas-clientes.html: a Google chapter, a returning-customers chapter, the realtor and property-manager scripts, the
review-in-person script with the no-discount warning, two number fixes, the "hoy en 20 minutos" box, the new order,
and a phone-width fix for the cover cards. Idempotent (marker AUDIT-2026-09-15). Run once, then tools/build_jugadas.py."""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "mas-clientes.html")
s = open(P, encoding="utf-8").read()
if "AUDIT-2026-09-15" in s:
    raise SystemExit("ya aplicado")

def sub1(a, b, name):
    global s
    n = s.count(a)
    if n != 1: raise SystemExit("ANCLA x%d: %s" % (n, name))
    s = s.replace(a, b)

# 1. number fixes in the base chapter
sub1('Como 4 de cada 10 llamadas a negocios nunca llegan a una persona.',
     'Casi la mitad de las llamadas a negocios de servicio a domicilio (48%) nunca las contesta una persona.', "48%")
sub1('contactar en 5 minutos en vez de 30 te hace <em>21 veces más probable</em> ganarte a ese cliente.',
     'contactar en 5 minutos en vez de 30 te hace <em>21 veces más probable</em> ganarte a ese cliente (estudio de 2007). El dato de hoy es más simple: el 55% de los clientes espera respuesta dentro de una hora, y solo el 20% de los dueños la da.', "21x")

# 2. the "hoy en 20 minutos" box at the end of the one-page plan
i = s.index('<section class="onepager">'); j = s.index('</section>', i)
HOY = '''
<div class="win" id="hoy20"><b>Hoy, en 20 minutos, antes que todo lo demás:</b> abre tu perfil de Google y revisa dos cosas. Que el nombre del negocio sea exactamente el de tu LLC. Y que la categoría principal sea la misma que usan los tres negocios que salen arriba cuando buscas tu oficio más tu ciudad. Esas dos cosas son el factor número uno del ranking local, y las cambias en un minuto. El capítulo 2 te lleva paso a paso.</div>
'''
s = s[:j] + HOY + s[j:]

# 3. split chapters
caps = [m.start() for m in re.finditer(r'<h2 class="cap" id="', s)]
src_i = s.rfind("<div", 0, s.rindex("Fuentes"))
ch = {}
order_old = []
for k, st in enumerate(caps):
    e = caps[k + 1] if k + 1 < len(caps) else src_i
    seg = s[st:e]
    cid = re.search(r'id="([^"]+)"', seg).group(1)
    ch[cid] = seg; order_old.append(cid)
head_part = s[:caps[0]]; tail_part = s[src_i:]

GOOGLE = '''<h2 class="cap" id="google"><span class="capnum">2</span> Tu perfil de Google: el lugar donde aterrizan todas las jugadas</h2>
<p class="h2sub">Cada letrero, cada vecino, cada etiqueta en Facebook manda a esa persona a buscarte en Google. Cinco cosas que sí mueven el ranking, y dos que no.</p>
<div class="bulb"><div class="big">74%</div><div class="txt">de la gente solo lee reseñas de los últimos tres meses. Las reseñas se echan a perder: por eso la petición es cada semana, no una vez.<span class="src">BrightLocal, encuesta de consumidores 2026</span></div></div>
<h3>1. La categoría principal (1 minuto)</h3>
<p>Es el factor número uno de todo el ranking local, por encima de qué tan cerca estás del que busca. Busca tu oficio más tu ciudad en Google Maps, mira qué categoría usan los tres que salen arriba, y pon exactamente esa como principal. "Contratista" en vez de "Pintor" te saca del mapa.</p>
<h3>2. El nombre del negocio, igual que tu LLC (1 minuto)</h3>
<p>Si el nombre del perfil no coincide con tu papel legal y Google te suspende, la recuperación puede tardar meses o no llegar. Nada de "Pintores Ramírez | Austin | Mejor precio". Solo el nombre.</p>
<h3>3. Contesta TODAS las reseñas, las buenas y las malas</h3>
<p>El 89% de la gente espera que el dueño conteste, y el 80% es más propenso a contratar a un negocio que contesta todas. Dos renglones bastan: gracias por el nombre, y qué trabajo fue. A una mala, sin pelear: "Lamento que quedara así. Le llamo hoy para arreglarlo".</p>
<h3>4. La reseña se pide en persona, antes de subirte al camión</h3>
<div class="script"><button class="copybtn" onclick="cp(this)">Copiar</button><span class="lang">Español, dilo en persona</span><span class="cptext">Me da mucho gusto que haya quedado contento. Le voy a mandar un mensajito de texto con un enlace para dejarnos una reseña en Google. Son treinta segundos y a un negocio como el mío le ayuda muchísimo. Si quiere, lo abrimos aquí mismo y yo le muestro dónde darle.</span></div>
<p>El momento lo es todo: si no saca el teléfono mientras todavía estás ahí parado, casi nunca pasa después. Tu sistema manda el enlace solo; tu trabajo es avisar de frente.</p>
<div class="warn"><b>Nunca ofrezcas descuento a cambio de una reseña.</b> Google lo prohíbe. Cuando lo detecta borra todas las reseñas de un jalón y puede marcar el perfil. Se pide, no se compra.</div>
<h3>5. Servicios, zona y fotos reales</h3>
<p>Llena la lista de servicios con lo que de verdad haces, marca tu zona de trabajo, y sube fotos de trabajos tuyos, no de catálogo. Las fotos no suben el ranking (eso es cuento de agencias), pero son lo primero que ve el dueño de casa antes de decidir a quién llamar.</p>
<div class="slateline"><div class="dot">S</div><div><b>Tu sistema de Slate</b> vigila la posición de tu perfil en el mapa cada semana y te avisa cuando algo cambia. Los puntos 1 y 2 los cambias tú en un minuto; si no sabes dónde, mándanos un texto y lo hacemos contigo en la llamada.</div></div>
'''
REGRESAN = '''<h2 class="cap" id="regresan"><span class="capnum">5</span> Los clientes que ya te pagaron: el año dos vive en tu teléfono</h2>
<p class="h2sub">El capítulo 3 es para arrancar. Este es para sostener: la gente que ya te conoce y ya te pagó.</p>
<div class="bulb"><div class="big">59%</div><div class="txt">del trabajo nuevo viene de clientes que regresan, empatado con los referidos. Google Search: 20%. Nadie vende más barato que un cliente que ya te pagó una vez.<span class="src">Jobber, reporte de tendencias 2026 (1,050 dueños)</span></div></div>
<h3>Sube tu lista de clientes viejos al sistema</h3>
<p>Nombre y teléfono de cada persona a la que le hiciste un trabajo. La subes una vez en tu portal de Slate (la página de "contactos"). El sistema les pide la reseña que nunca les pediste, y durante un año les manda, con tu nombre, la oferta de referidos: "¿quién de tus conocidos necesita esto?". Tú no tocas nada.</p>
<h3>El recordatorio de temporada, con tu oficio</h3>
<p>Cada oficio tiene una fecha en la que la casa vuelve a necesitarte: canaletas y techos antes de las lluvias, el clima antes del calor, la pintura exterior antes del frío, el jardín en primavera. Un texto a tus clientes de hace un año, el mes antes:</p>
<div class="script"><button class="copybtn" onclick="cp(this)">Copiar</button><span class="lang">Español</span><span class="cptext">Hola [Nombre], soy [tu nombre], el de [pintura]. Le hice [el trabajo] el año pasado. Se acerca [la temporada] y ando por su zona la semana que viene. Si quiere que le dé una revisada sin costo, dígame qué día le queda.</span></div>
<h3>El aniversario del trabajo</h3>
<p>Doce meses después de terminar, un texto de tres renglones: "¿cómo sigue [el trabajo]? Cualquier detalle, me dice". No vende nada y por eso funciona: el que contesta "todo bien" es el mismo que te manda al vecino la semana siguiente.</p>
<div class="slateline"><div class="dot">S</div><div><b>Lo que ya hace tu sistema:</b> la reseña y la cadena de referidos de un año, solos, a cada cliente que agregas. El recordatorio de temporada lo mandas tú con el texto de arriba; dinos tu temporada y lo dejamos programado.</div></div>
'''
# 4. scripts into feeders (append at the end of the chapter)
FEED_SCRIPTS = '''
<h3>Qué decirle, palabra por palabra</h3>
<div class="script"><button class="copybtn" onclick="cp(this)">Copiar</button><span class="lang">Al agente de bienes raíces</span><span class="cptext">Hola, soy [Nombre], de [Negocio]. Hago [pintura] aquí en [ciudad]. No vengo a pedirle trabajo. Vengo a ofrecerle dos cosas que a usted le sirven en cada cierre. Uno: si me manda una casa que va a salir a la venta, yo la camino sin costo y le entrego por escrito, en veinticuatro horas, qué hay que arreglar antes de las fotos y qué no vale la pena tocar. Esa lista se la queda usted, la use conmigo o no. Dos: cuando un comprador suyo pregunte por [pintura], yo contesto el teléfono el mismo día y nunca lo dejo quedar mal. Nunca le voy a ofrecer dinero por recomendarme, porque la ley federal no lo permite. Lo único que le ofrezco es rapidez y que usted quede bien.</span></div>
<div class="script"><button class="copybtn" onclick="cp(this)">Copiar</button><span class="lang">Al administrador de propiedades</span><span class="cptext">Hola, soy [Nombre], de [Negocio]. Hago [pintura] en [ciudad] y trabajo con propiedades de renta. Le mando hoy mismo un solo PDF con todo lo que su departamento de papeles necesita: el seguro con el endoso de asegurado adicional, la licencia, la W-9 y mi lista de precios. Y le hago una promesa concreta: usted me textea una salida de inquilino y yo la camino en veinticuatro horas y le mando el precio por escrito. Si le sirve, empezamos con una sola unidad para que me vea trabajar.</span></div>
'''
ch["feeders"] = ch["feeders"].rstrip() + "\n" + FEED_SCRIPTS
# 5. new order + renumber
order = ["base", "google", "warm", "job", "regresan", "comunidad", "facebook", "nextdoor", "feeders", "partners", "paid", "presence", "referral", "rhythm"]
ch["google"] = GOOGLE; ch["regresan"] = REGRESAN
titles = {}
body = ""
for n, cid in enumerate(order, 1):
    seg = ch[cid]
    seg = re.sub(r'<span class="capnum">[^<]*</span>', '<span class="capnum">%d</span>' % n, seg, count=1)
    titles[cid] = re.sub(r"<[^>]+>", "", re.search(r"<h2[^>]*>(.*?)</h2>", seg, re.S).group(1)).strip()
    titles[cid] = re.sub(r"^\d+\s*", "", titles[cid])
    body += seg
# cross-references that named a chapter number
body = body.replace("La lista de permisos de tu oficio (cap. 8)", "La lista de permisos de tu oficio (cap. 9)")
body = body.replace("Y el capítulo 8 te acaba de armar la lista perfecta", "Y el capítulo 10 te acaba de armar la lista perfecta")
s = head_part + body + tail_part
# toc rebuilt
ti = s.index('<div class="toc">'); tj = s.index('</div>', ti) + len('</div>')
toc = '<div class="toc">\n' + "".join('  <li><span class="tn">%d</span><a href="#%s">%s</a></li>\n' % (n, cid, titles[cid]) for n, cid in enumerate(order, 1)) + '</div>'
s = s[:ti] + toc + s[tj:]
# 6. phone-width fix for the cover cards + marker
sub1('</style>', '  /* AUDIT-2026-09-15: phone width, the cover cards wrap instead of overflowing */\n  @media (max-width:520px){ .statrow{flex-wrap:wrap} .stat{flex:1 1 100%; min-width:0} .wrap{padding:0 16px} }\n</style>', "style")
# 7. sources: add the new ones
sub1('<li>Hilos reales en r/sweatystartup',
     '<li>Whitespark Local Search Ranking Factors 2026 (categoría principal = factor #1) · Jobber 2026 (clientes que regresan 59%, respuesta en 1 hora 55% vs 20%) · BrightLocal 2026 (74% solo lee reseñas de 3 meses; 89% espera respuesta del dueño) · Invoca 2026 (48% de llamadas sin contestar, 70M llamadas) · Política de reseñas de Google (sin incentivos)</li>\n<li>Hilos reales en r/sweatystartup', "srcs")
open(P, "w", encoding="utf-8").write(s)
print("audit applied:", " > ".join("%d %s" % (n, c) for n, c in enumerate(order, 1)))
