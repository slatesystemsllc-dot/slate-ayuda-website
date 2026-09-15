#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apply_action_cards.py (Dan 2026-09-15: "6.5/10, I want a 9, something SO valuable it could be worth money"):
every play opens with an ACTION CARD (what you do in one line, what it brings with its source, how long it takes,
the first step today), and the landing gets the "Semana 1" ladder for a brand-new client. Numbers come from
~/slate-ghl/leads-guide-audit-2026-09-15/research.md. Idempotent (marker ACTION-CARDS-2026-09-15)."""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "mas-clientes.html"); s = open(P, encoding="utf-8").read()
if "ACTION-CARDS-2026-09-15" in s: raise SystemExit("ya aplicado")

CARDS = {
 "base": ("Contesta. Y cuando no puedas, que el texto salga solo.",
          "Casi la mitad de las llamadas a negocios de servicio nunca las contesta una persona (48%). De las que sí, 38% son clientes reales y casi la mitad de esos agendan en esa misma llamada.", "Invoca 2026, 70 millones de llamadas",
          "Cero minutos. Tu sistema ya lo hace: el texto de llamada perdida sale en segundos.",
          "Llama a tu propio número desde otro teléfono y no contestes. Mira llegar el texto. Así sabes qué recibe tu cliente."),
 "google": ("Pide la reseña de frente, antes de subirte al camión. Y contesta cada reseña.",
          "El 74% de la gente solo lee reseñas de los últimos tres meses. Las reseñas viejas no cuentan: la petición es en cada trabajo.", "BrightLocal 2026, 1,002 adultos",
          "30 segundos por trabajo. El enlace lo manda el sistema.",
          "Hoy: contesta las reseñas que tienes sin responder, dos renglones cada una. Mañana: la frase de la reseña al terminar el primer trabajo."),
 "warm": ("Mándale el texto de anuncio a 10 personas que ya te conocen. Diez por día.",
          "El 59% del trabajo nuevo llega por referidos. Google Search: 20%. De 100 textos, espera 30 a 50 respuestas y de 2 a 5 trabajos el primer mes.", "Jobber 2026, 1,050 dueños",
          "Dos horas una vez para la lista. Después, 10 minutos al día.",
          "Hoy: escribe 30 nombres en papel y manda el texto a los primeros 10. No pidas favores, avisa."),
 "job": ("En cada trabajo: letrero el día uno, las 10 puertas que lo ven, nota a mano en las que no abren.",
          "Sin estudio, con muchos testimonios que coinciden: un contratista vendió cerca de $100,000 en decks con 25 letreros de $550. La nota escrita a mano da como 1 de cada 8 llamadas de vuelta; el volante genérico, casi cero.", "r/Contractor y r/sweatystartup, 2025-2026",
          "20 minutos por trabajo terminado.",
          "Hoy: pide 20 letreros con estaca (unos $3 cada uno). El próximo trabajo, el letrero entra cuando das la mano."),
 "regresan": ("Sube tu lista de clientes viejos al sistema. Ellos son el año dos.",
          "Los clientes que regresan traen tanto trabajo como los referidos: 59% cada uno. Nadie vende más barato que alguien que ya te pagó.", "Jobber 2026, 1,050 dueños",
          "Una hora, una vez. Después el sistema les pide la reseña y les manda la cadena de referidos de un año.",
          "Hoy: junta nombre y teléfono de tus últimos 50 clientes y súbelos en tu portal de contactos."),
 "comunidad": ("Avisa una sola vez en cada grupo donde ya te tienen confianza: parroquia, escuela, WhatsApp del pueblo.",
          "El 56% de los adultos hispanos en EE.UU. usa WhatsApp. Una sola publicación aprobada en un grupo activo de 200 trae de 5 a 20 mensajes en 48 horas.", "Pew Research 2025; testimonios de dueños",
          "Una tarde, una vez. Después solo contestas cuando alguien pregunte.",
          "Hoy: escríbele al admin de tu grupo más grande y pide permiso para publicar UNA vez."),
 "facebook": ("Únete a 12 grupos de tu ciudad y contesta el hilo de «¿a quién me recomiendan?» dentro de la primera hora.",
          "El 32% de los dueños nombran Facebook como fuente de trabajo, arriba del 20% de Google Search. En una prueba con 466 negocios, el 95% no contestó en 5 minutos: llegar primero gana.", "Jobber 2026; Valve+Meter",
          "Una hora a la semana.",
          "Hoy: busca «[ciudad] Recommendations» y «Latinos en [ciudad]», únete a dos, prende las notificaciones."),
 "nextdoor": ("Reclama tu página gratis y pide UNA recomendación por semana. Que te nombre el vecino, nunca tú.",
          "9 de cada 10 dicen que la recomendación de un vecino influye; el 41% contacta de inmediato cuando nota el problema. Diez recomendaciones en tu código postal te vuelven la respuesta de cajón.", "Nextdoor, Home Maintenance Report 2026",
          "15 minutos una vez, y un texto por semana.",
          "Hoy: busca tu negocio en Nextdoor, reclámalo (no lo dupliques) y súbele 6 fotos reales."),
 "feeders": ("Una mañana fija en la tienda de materiales, la lista de permisos, y un PDF de papeles para administradores.",
          "El 25% de los dueños nombran redes y alianzas locales como fuente de trabajo, arriba del 20% de Google Search. Esta gente coloca trabajos cada semana, no cada tres años.", "Jobber 2026",
          "Dos horas al mes.",
          "Hoy: arma el PDF único (seguro con endoso, licencia, W-9, precios). Mañana: la misma tienda, la misma hora, con tarjetas."),
 "partners": ("Mándale tú un cliente a un oficio socio primero. Luego pide.",
          "Las alianzas locales producen más clientes (25%) que Google (20%) y que los sitios que venden leads (16%). Y cada socio es un referido de Slate: $97 al mes para ti.", "Jobber 2026; programa de referidos de Slate",
          "Un cliente al mes a un socio, y avísale.",
          "Hoy: abre la tarjeta de tu oficio abajo y anota los tres socios que ya ven tus trabajos."),
 "paid": ("Si un día pagas, paga por llamada real (Local Services Ads), nunca por leads compartidos.",
          "En 888 contratistas, el 44% de los leads de Google agendan: sale a unos $233 por cliente que paga. Los sitios que venden leads los revenden a varios a la vez; la FTC multó a HomeAdvisor con hasta 7.2 millones por promesas falsas.", "SearchLight 2026; FTC 2023",
          "Nada hoy. Solo cuando la máquina gratis esté llena.",
          "Hoy: nada. Guarda esta página para el día que te sobre trabajo y quieras crecer."),
 "presence": ("Patrocina donde ya estás: el equipo de tu hijo, la barda del campo. Y párate ahí.",
          "Compra confianza, no clientes de este mes. La mayoría renuncia al día 60, justo antes de que arranque. Los datos de las cámaras de comercio los publica la propia cámara.", "testimonios de dueños; Schapiro Group (parte interesada)",
          "Dos veces al mes en persona, o no sirve.",
          "Hoy: pregunta cuánto cuesta la playera de la liga infantil de tu colonia. Suele ser de $100 a $500 por temporada."),
 "referral": ("Preséntanos a otro dueño de negocio. Te pagamos $97 al mes mientras él siga.",
          "Tres referidos son $291 al mes: tu sistema prácticamente se paga solo. Sin tope, pagado el día 1, directo a tu banco.", "programa de referidos de Slate",
          "Un mensaje.",
          "Hoy: pídenos tu enlace de referido y mándaselo al socio del capítulo 10 que más trabajo te pasa."),
 "rhythm": ("Cada trabajo: reseña, un nombre, 10 puertas, letrero, foto. Cada semana: una hora. Cada mes: la tienda y un socio.",
          "Nada de esto pide dinero. Pide 20 minutos por trabajo y una hora a la semana. Todo lo demás lo atrapa el sistema.", "esta guía",
          "20 minutos por trabajo, 1 hora por semana, 2 horas por mes.",
          "Hoy: imprime el Plan de 1 Página y pégalo en la camioneta."),
}
CSS = '''
  /* ACTION-CARDS-2026-09-15 */
  .accion{background:#fff;border:2px solid var(--navy);border-radius:14px;padding:16px 18px;margin:18px 0 24px}
  .accion .ar{display:grid;grid-template-columns:96px 1fr;gap:8px 12px;padding:8px 0;border-top:1px solid #e6e9ef;align-items:start}
  .accion .ar:first-child{border-top:0;padding-top:0}
  .accion .al{font-size:12px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;color:var(--orange);padding-top:3px}
  .accion .av{font-size:16px;line-height:1.45}
  .accion .av b{font-weight:800}
  .accion .asrc{display:block;font-size:12px;color:#5b6472;margin-top:4px}
  .semana1{background:#fff;border:2px solid var(--orange);border-radius:14px;padding:16px 18px;margin:18px 0}
  .semana1 h3{margin:0 0 8px}
  .semana1 ol{margin:0;padding-left:20px}
  .semana1 li{margin:6px 0}
  @media (max-width:520px){ .accion .ar{grid-template-columns:1fr} .accion .al{padding-top:0} }
'''
def card(c):
    que, trae, src, tiempo, hoy = c
    return ('<div class="accion">'
            '<div class="ar"><div class="al">Qué haces</div><div class="av"><b>%s</b></div></div>'
            '<div class="ar"><div class="al">Qué trae</div><div class="av">%s<span class="asrc">Fuente: %s</span></div></div>'
            '<div class="ar"><div class="al">Te toma</div><div class="av">%s</div></div>'
            '<div class="ar"><div class="al">Hoy</div><div class="av">%s</div></div>'
            '</div>\n') % (que, trae, src, tiempo, hoy)
n = 0
for cid, c in CARDS.items():
    m = re.search(r'(<h2 class="cap" id="%s">.*?</h2>\s*<p class="h2sub">.*?</p>\s*)' % cid, s, re.S)
    if not m: raise SystemExit("sin h2/h2sub: " + cid)
    s = s[:m.end()] + card(c) + s[m.end():]; n += 1
SEMANA = '''
<div class="semana1" id="semana1"><h3>Si acabas de empezar: la primera semana, día por día</h3>
<ol>
<li><b>Día 1 (20 min):</b> contesta las reseñas que tienes sin responder. Llama a tu propio número y mira llegar el texto de llamada perdida.</li>
<li><b>Día 2 (2 horas):</b> la lista de 100 nombres, en papel, con la familia. Texto de anuncio a los primeros 10.</li>
<li><b>Día 3 (1 hora):</b> sube tus últimos 50 clientes al portal de contactos. El sistema empieza a pedirles reseña.</li>
<li><b>Día 4 (30 min):</b> únete a dos grupos de Facebook de tu ciudad y reclama tu página de Nextdoor. Diez textos más.</li>
<li><b>Día 5 (30 min):</b> pide 20 letreros con estaca. Arma el PDF de papeles. Diez textos más.</li>
<li><b>Día 6 (1 hora):</b> pídele permiso al admin de tu grupo de WhatsApp y publica UNA vez. Diez textos más.</li>
<li><b>Día 7:</b> el primer trabajo terminado con la rutina completa: reseña de frente, un nombre, 10 puertas, letrero, foto.</li>
</ol></div>
'''
i = s.index('<div class="win" id="hoy20">'); j = s.index('</div>', i) + len('</div>')
s = s[:j] + SEMANA + s[j:]
s = s.replace('</style>', CSS + '</style>', 1)
open(P, "w", encoding="utf-8").write(s); print("action cards:", n, "+ semana 1")
