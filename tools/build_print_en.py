#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_print_en.py: copies jugadas/imprimir/ (Spanish page chrome, English printed piece) into the help repo's
plays/print/ and translates the page chrome. 2026-09-16: keeps EN and ES printables in lockstep; edit imprimir/ only,
then run this. Usage: python3 tools/build_print_en.py"""
import os, re, shutil, glob
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jugadas", "imprimir")
DST = os.path.expanduser("~/slate-help-repo/plays/print")
os.makedirs(DST, exist_ok=True)
T = [
 ('<title>Letrero de jardín</title>', '<title>Yard sign</title>'), ('<title>Volante colgante</title>', '<title>Door hanger</title>'),
 ('<title>Tarjeta escrita a mano</title>', '<title>Handwritten card</title>'), ('<title>La hoja de 100 nombres</title>', '<title>The 100-name sheet</title>'),
 ('<title>Tu hoja de papeles</title>', '<title>Your paperwork sheet</title>'),
 ('← Volver a la jugada', '← Back to the play'), ('Imprimir o guardar PDF', 'Print or save as PDF'),
 ('El letrero va en inglés: lo lee el vecino, no tú. Guárdalo en PDF y mándalo a la imprenta: letrero de 24 x 18 pulgadas (coroplast) con estaca de alambre, de 2 a 4 dólares cada uno. Pide 20. Si algo sale en gris claro, es un espacio que la imprenta te rellena.',
  'Save it as a PDF and send it to the print shop: 24 x 18 inch coroplast yard sign with a wire stake, 2 to 4 dollars each. Order 20. Anything in light gray is a blank the print shop fills in.'),
 ('Volante de perilla (door hanger), un lado, en inglés: lo lee el vecino.  500 impresos cuestan de 75 a 125 dólares. Cuélgalos el mismo día en las 100 a 200 puertas alrededor del trabajo, con la camioneta todavía ahí. Nunca en el buzón. Escribe a mano la calle y la fecha en cada uno, y engrapa la foto del trabajo.',
  'Door hanger, one side. 500 printed cost 75 to 125 dollars. Hang them the same day on the 100 to 200 doors around the job, with the truck still there. Never in the mailbox. Hand-write the street and the date on each one, and staple the photo of the job.'),
 ('<b>Esta hoja salió sin tus datos.</b> Ábrela desde el botón naranja de tu página de enlaces y sale con tu logo, tu nombre y tu teléfono.',
  '<b>This sheet came out without your data.</b> Open it from the orange button on your links page and it comes with your logo, your name and your phone.'),
 ('<b>Esta hoja salió sin tus datos.</b> Ábrela desde el botón naranja de tu página de enlaces y sale con tu nombre y tu teléfono. Si la quieres así, la imprenta te rellena los espacios en gris.',
  '<b>This sheet came out without your data.</b> Open it from the orange button on your links page and it comes with your name and your phone. If you want it like this, the print shop fills in the gray blanks.'),
 ('En inglés: la lee el vecino. Para las puertas que no abrieron. Escríbela con pluma azul, tres renglones, y engrápale la foto del trabajo. Esta hoja es la plantilla: cópiala a mano, no la imprimas.',
  'For the doors that did not open. Write it with a blue pen, three lines, and staple the photo of the job. This sheet is the template: copy it by hand, do not print it.'),
 ('Dóblala en el marco de la puerta. Nadie más en esa calle escribe nada a mano. Di el color de la casa: así saben que estuviste ahí.', 'Fold it into the door frame. Nobody else on that street writes anything by hand. Name the color of the house: that is how they know you were there.'),
 ('Imprime dos copias. Una noche, teléfono en mano: contactos, WhatsApp, Facebook. Cuatro columnas. Marca la primera casilla cuando mandes el texto y la segunda cuando te contesten (10 por día).',
  'Print two copies. One evening, phone in hand: contacts, WhatsApp, Facebook. Four columns. Tick the first box when you send the text and the second when they answer (10 a day).'),
 ('Mis 100 nombres', 'My 100 names'), ('☐ texto enviado · ☐ contestó', '☐ text sent · ☐ answered'),
 ('No es una lista de favores. Es la gente que va a saber qué contestar cuando alguien pregunte «¿conoces a alguien?».', 'This is not a list of favors. These are the people who will know what to answer when somebody asks "do you know anyone?".'),
 ('>Familia<', '>Family<'), ('>Excompañeros y exjefes<', '>Old coworkers and bosses<'), ('>Iglesia y escuela<', '>Church and school<'), ('>Todos los demás<', '>Everyone else<'),
 ('Una sola página para administradores de propiedades, asociaciones (HOA) y contratistas generales. Junta con esta hoja el seguro (con el endoso de asegurado adicional), la licencia y la W-9 en un solo PDF.',
  'One page for property managers, HOAs and general contractors. Put this sheet, the insurance (with the additional-insured endorsement), the license and the W-9 together in one PDF.'),
 ('[Nombre del negocio]', '[Business name]'), ('[tu oficio]', '[your trade]'), ('[tu teléfono]', '[your phone]'), ('[tu página]', '[your website]'),
 ('>Licencia<', '>License<'), ('[número y estado]', '[number and state]'), ('>Seguro<', '>Insurance<'), ('[aseguradora y póliza]', '[carrier and policy]'),
 ('· endoso de asegurado adicional: sí', '· additional-insured endorsement: yes'), ('>adjunta<', '>attached<'), ('>Zona<', '>Service area<'), ('[ciudades o códigos postales]', '[towns or zip codes]'),
 ('>Precios<', '>Prices<'), ('[tus 5 servicios más comunes con precio]', '[your 5 most common services with prices]'),
 ('>Años en el oficio<', '>Years in the trade<'), ('[años]', '[years]'), ('>Trabajos por semana<', '>Jobs per week<'), ('[cuántos puedo tomar]', '[how many I can take]'),
 ('>Mi promesa (administradores y HOA)<', '>My promise (property managers and HOAs)<'),
 ('Usted me textea una salida de inquilino y yo la camino en 24 horas con precio por escrito. Foto al final de cada día.', 'You text me a tenant move-out and I walk it within 24 hours with a written price. A photo at the end of every day.'),
 ('>Mi promesa (contratistas generales)<', '>My promise (general contractors)<'),
 ('Cotización por escrito en 24 horas. Empiezo el lunes que usted diga y no dejo la obra a medias.', 'Written quote within 24 hours. I start the Monday you name and I never leave a job half done.'),
 ('>Referencias<', '>References<'), ('[dos clientes que den la cara]', '[two clients who will vouch for you]'),
 ('Escanea para ver mis trabajos', 'Scan to see my work'),
]
for f in glob.glob(os.path.join(SRC, "*")):
    name = os.path.basename(f)
    if name.endswith(".js"):
        shutil.copy(f, os.path.join(DST, name)); continue
    s = open(f, encoding="utf-8").read()
    for a, b in T:
        s = s.replace(a, b)
    open(os.path.join(DST, name), "w", encoding="utf-8").write(s)
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    left = re.findall(r"[áéíóúñ¿¡]", body)
    print("%-16s spanish chars left: %d" % (name, len(left)))
