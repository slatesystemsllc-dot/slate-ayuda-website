#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apply_audit_2026_09_15c.py: round 3 of the 2026-09-15 audit (section 6, smart plays with proof + two Nextdoor corrections).
Client-side only; the Google profile plays (predefined services, keywords in the owner's reply) went to the internal GBP SOP.
Idempotent (marker AUDIT-2026-09-15c)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "mas-clientes.html"); s = open(P, encoding="utf-8").read()
if "AUDIT-2026-09-15c" in s: raise SystemExit("ya aplicado")
def sub1(a, b, name):
    global s
    n = s.count(a)
    if n != 1: raise SystemExit("ANCLA x%d: %s" % (n, name))
    s = s.replace(a, b)
# 1. Nextdoor: the voting window exists now, and the owner never answers "that's me" from his personal account
sub1('El premio Neighborhood Faves cuenta cada recomendación de los últimos 365 días. No hay semana de votación: una petición por semana, cada semana, es toda la estrategia.',
     'El premio Neighborhood Faves se decide con una votación al año (la de 2026 cierra el 30 de septiembre), y las recomendaciones que juntas todo el año son las que te ponen en la boleta. Una petición por semana, cada semana, es toda la estrategia. Y desde agosto de 2026, Nextdoor le baja el alcance al dueño que contesta "ese soy yo, llámame" desde su cuenta personal: la promoción sale de tu página de negocio, y en los hilos de "¿a quién me recomiendan?" el que te nombra es tu cliente, nunca tú.', "nextdoor")
# 2. realtor red box: the exact line
sub1('Pagarle a un <b>agente de bienes raíces</b> en efectivo o regalos choca con la ley federal de comisiones ocultas; los reguladores dicen que hasta un patrón de regalitos cuenta.',
     'Pagarle a un <b>agente de bienes raíces</b> por mandarte clientes choca con la ley federal de comisiones ocultas (RESPA): nada de dinero ni de cosas de valor ligadas al cierre, al préstamo, al avalúo o a la inspección. Lo que sí es legal, porque tu oficio no es un servicio de cierre: que el agente te compre a ti el regalo de cierre para su comprador (una limpieza, una pintada de un cuarto, una revisión), pagado a precio normal.', "respa")
# 3. adjusters: the statute line
sub1('Pagarle a un <b>ajustador de seguros</b> por referidos se trata como soborno o fraude en varios estados.',
     'Pagarle a un <b>ajustador de seguros</b> por referidos se trata como soborno o fraude en varios estados: es delito en California y está prohibido por ley en Virginia, Luisiana y Texas.', "adjuster")
# 4. neighbor card with the photo
sub1('<h3>La tarjeta escrita a mano para las puertas que no abrieron</h3>',
     '<h3>La tarjeta escrita a mano, con la foto, para las puertas que no abrieron</h3>', "card h3")
sub1('Dóblala en el marco de la puerta. Nadie más en esa calle escribe nada a mano.',
     'Engrápale la foto del trabajo terminado, impresa en la farmacia por unos centavos. Dóblala en el marco de la puerta. Nadie más en esa calle escribe nada a mano, y una foto de la casa de al lado vale más que cualquier volante.', "card body")
# 5. HOA through the management company + Trade Ally network, in the feeders chapter (before the scripts block)
sub1('<h3>Qué decirle, palabra por palabra</h3>',
     '''<h3>Dos puertas más que casi nadie toca</h3>
<p><b>La lista de proveedores de las asociaciones (HOA).</b> No vayas a la mesa directiva: ve a la empresa que ADMINISTRA la asociación. Una sola empresa lleva docenas de HOA, y su lista de proveedores aprobados es una sola. Mismo PDF que a los administradores de propiedades.</p>
<p><b>La red de contratistas de la compañía de luz (Trade Ally), solo clima, plomería e aislamiento.</b> Es gratis inscribirse y en varios estados el reembolso del cliente (más de $1,500 en una bomba de calor, por ejemplo) solo se paga si el trabajo lo hizo un contratista inscrito. Busca "[tu compañía de luz] trade ally" y llena la solicitud una vez.</p>
<h3>Qué decirle, palabra por palabra</h3>''', "feeders extra")
# 6. church bulletin ad: honest
sub1('Casi todas lo publican gratis o por una donación chica.',
     'Casi todas lo publican gratis o por una donación chica. Honesto: el anuncio por sí solo casi no trae llamadas; lo que trae trabajo es que te vean participar. Si te cobran cientos al año por la línea, di que no.', "church")
# 7. texting law box in the returning-customers chapter
sub1('<div class="slateline"><div class="dot">S</div><div><b>Lo que ya hace tu sistema:</b> la reseña y la cadena de referidos de un año, solos, a cada cliente que agregas. El recordatorio de temporada lo mandas tú con el texto de arriba; dinos tu temporada y lo dejamos programado.</div></div>',
     '''<div class="warn"><b>Ojo con los textos en masa.</b> Un texto de promoción a una lista de clientes tiene reglas en Estados Unidos: consentimiento por escrito, solo de 8 am a 9 pm en su hora, baja por cualquier medio y número registrado con las telefónicas (desde 2025 bloquean el 100% de lo que no está registrado). Un texto tuyo, a una persona, desde tu teléfono, está bien. Una lista entera, no: eso lo manda el sistema, que ya cumple todo lo anterior.</div>
<div class="slateline"><div class="dot">S</div><div><b>Lo que ya hace tu sistema:</b> la reseña y la cadena de referidos de un año, solos, a cada cliente que agregas, con el consentimiento, el horario y la baja resueltos. El recordatorio de temporada lo mandas tú con el texto de arriba, uno por uno; si quieres que salga solo a toda tu lista, dinos tu temporada y lo dejamos programado.</div></div>''', "texting")
# 8. sources
sub1('<li>Jobber 2026 (clientes que regresan 59%',
     '<li>Sterling Sky, pruebas controladas del perfil de Google (2025-2026) · Nextdoor, votación Fave Awards 2026 y reglas de autopromoción del 19 de agosto de 2026 · CFPB, RESPA (qué es un servicio de cierre) · Programas Trade Ally de Puget Sound Energy, Consumers Energy y Focus on Energy (2026) · FCC/TCPA y reglas de las telefónicas para A2P 10DLC (2025)</li>\n<li>Jobber 2026 (clientes que regresan 59%', "srcs")
s = s.replace('/* AUDIT-2026-09-15 + AUDIT-2026-09-15b: phone width', '/* AUDIT-2026-09-15 + AUDIT-2026-09-15b + AUDIT-2026-09-15c: phone width')
open(P, "w", encoding="utf-8").write(s); print("applied c")
