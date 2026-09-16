// Shared by the printables. The client's data arrives on the link from his links page (GHL fills the custom values).
// '#' in a hex color starts the URL fragment, so colors are read from search + hash together. No data = grey blanks + notice.
(function(){
var raw=(location.search||'')+(location.hash||'');
function grab(k){var m=raw.match(new RegExp('[?&#]'+k+'=([^&#]*)'));return m?decodeURIComponent(m[1].replace(/\+/g,' ')):'';}
['oficio','negocio','tel','web','logo','ciudad'].forEach(function(k){var v=grab(k);if(v){try{localStorage.setItem(k,v)}catch(e){}}});
var hx=raw.match(/c1=(?:%23|#)?([0-9a-fA-F]{6})/); if(hx){try{localStorage.setItem('c1','#'+hx[1])}catch(e){}}
var hy=raw.match(/c2=(?:%23|#)?([0-9a-fA-F]{6})/); if(hy){try{localStorage.setItem('c2','#'+hy[1])}catch(e){}}
function g(k){try{return localStorage.getItem(k)||''}catch(e){return ''}}
function lum(h){var r=parseInt(h.substr(1,2),16),g2=parseInt(h.substr(3,2),16),b=parseInt(h.substr(5,2),16);return (0.299*r+0.587*g2+0.114*b)/255;}
var c1=g('c1'),c2=g('c2');
if(/^#[0-9a-fA-F]{6}$/.test(c1)&&lum(c1)<0.6){document.documentElement.style.setProperty('--navy',c1);}
if(/^#[0-9a-fA-F]{6}$/.test(c2)&&lum(c2)<0.75&&c2.toLowerCase()!==c1.toLowerCase()){document.documentElement.style.setProperty('--orange',c2);}
var web=g('web').replace(/^https?:\/\//i,'').replace(/\/+$/,'');
var EN={'pintura':'Painting','poda de arboles':'Tree service','acarreo':'Junk removal','limpieza de basura':'Junk removal','plomeria':'Plumbing','techos':'Roofing','jardineria y paisajismo':'Landscaping','limpieza':'Cleaning','climas y calefaccion':'HVAC','instalaciones electricas':'Electrical','handyman':'Handyman','pisos':'Flooring','concreto':'Concrete','cercas':'Fencing','control de plagas':'Pest control','remodelacion':'Remodeling','construccion general':'General contractor','aislamiento':'Insulation','pavimento y asfalto':'Paving','constructores de casas':'Home builder','ventanas y puertas':'Windows & doors','solar':'Solar','terrazas y patios':'Decks & patios'};
function norm(v){return String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
var ofn=norm(g('oficio')),ofEN='';Object.keys(EN).forEach(function(k){if(!ofEN&&(ofn.indexOf(k)>=0||k.indexOf(ofn)>=0)&&ofn)ofEN=EN[k];});
var m={negocio:g('negocio'),tel:g('tel'),web:web,oficio:ofEN||g('oficio'),ciudad:g('ciudad')};
document.querySelectorAll('[data-k]').forEach(function(el){var v=m[el.getAttribute('data-k')];if(v){el.textContent=(el.getAttribute('data-prefix')||'')+v;el.classList.remove('fill');}else if(el.hasAttribute('data-hide')){el.hidden=true;}});
var logo=g('logo');
document.querySelectorAll('[data-logo]').forEach(function(box){var name=box.querySelector('[data-k="negocio"]');
  if(/^https?:\/\//i.test(logo)){var im=new Image();im.alt=m.negocio||'';im.onload=function(){box.classList.add('has-logo');box.insertBefore(im,box.firstChild);};im.src=logo;}});
if(!m.negocio&&!m.tel){var h=document.getElementById('sin-datos');if(h)h.hidden=false;}
})();

// Screen sizing without cqw: some browsers showed the hanger text 3x too big (Dan, 2026-09-16). Size from the measured
// width on screen; on paper the cqw rule takes over (inline style cleared before print, restored after).
(function(){function fit(){document.querySelectorAll('[data-fit]').forEach(function(el){el.style.fontSize=(el.clientWidth*parseFloat(el.getAttribute('data-fit')))+'px';});}
function clear(){document.querySelectorAll('[data-fit]').forEach(function(el){el.style.fontSize='';});}
fit();window.addEventListener('resize',fit);window.addEventListener('beforeprint',clear);window.addEventListener('afterprint',fit);
if(window.matchMedia){var mq=window.matchMedia('print');mq.addEventListener?mq.addEventListener('change',function(e){e.matches?clear():fit();}):mq.addListener(function(e){e.matches?clear():fit();});}})();
