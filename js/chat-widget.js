(function () {
  'use strict';

  var STORAGE_KEY = 'slate_chat';
  var MAX_TURNS = 10;
  var WELCOME_MSG = "Hey! I'm Sophie, your Slate support assistant. Ask me anything about your website, calls, reviews, referrals, or how to use the app. What can I help with?";
  var WELCOME_MSG_ES = "\u00a1Hola! Soy Sophie, tu asistente de soporte de Slate. Preg\u00fantame lo que quieras sobre tu p\u00e1gina web, llamadas, rese\u00f1as, referidos, o c\u00f3mo usar la app. \u00bfEn qu\u00e9 te puedo ayudar?";

  var IS_SPANISH = (document.documentElement.getAttribute('lang') || '').toLowerCase().indexOf('es') === 0
    || window.location.hostname.indexOf('ayuda') !== -1
    || window.location.pathname.indexOf('/es/') === 0
    || window.location.pathname === '/es';

  var style = document.createElement('style');
  style.textContent = [
    // Bubble
    '#slate-chat-bubble{position:fixed;bottom:24px;right:24px;width:56px;height:56px;border-radius:50%;background:#ee7000;color:#fff;border:none;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,0.2);z-index:9998;display:flex;align-items:center;justify-content:center;transition:transform .2s,box-shadow .2s;font-size:24px;line-height:1}',
    '#slate-chat-bubble:hover{transform:scale(1.08);box-shadow:0 6px 20px rgba(0,0,0,0.25)}',
    // Desktop panel
    '#slate-chat-panel{position:fixed;bottom:24px;right:24px;width:380px;max-width:calc(100vw - 48px);height:520px;max-height:calc(100vh - 48px);border-radius:12px;background:#fff;box-shadow:0 8px 32px rgba(0,0,0,0.18);z-index:9999;display:none;flex-direction:column;overflow:hidden;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;box-sizing:border-box}',
    '#slate-chat-panel *{box-sizing:border-box}',
    '#slate-chat-panel.open{display:flex}',
    // Header
    '.sc-header{background:#152a45;color:#fff;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;min-height:52px}',
    '.sc-header-left{display:flex;align-items:center;gap:8px}',
    '.sc-header-left span{font-weight:600;font-size:.95rem}',
    '.sc-header-dot{width:8px;height:8px;border-radius:50%;background:#4caf50;flex-shrink:0}',
    '.sc-header-actions{display:flex;gap:6px;align-items:center}',
    '.sc-header-btn{background:rgba(255,255,255,.12);border:none;color:#fff;width:32px;height:32px;border-radius:6px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;transition:background .15s}',
    '.sc-header-btn:hover{background:rgba(255,255,255,.25)}',
    '.sc-close-mobile{display:none}',
    // Messages
    '.sc-messages{flex:1;overflow-y:auto;overflow-x:hidden;padding:16px;display:flex;flex-direction:column;gap:12px;background:#f8f9fa;-webkit-overflow-scrolling:touch;min-height:0;overscroll-behavior:contain}',
    '.sc-msg{max-width:85%;padding:10px 14px;border-radius:12px;font-size:.9rem;line-height:1.5;word-wrap:break-word;flex-shrink:0}',
    '.sc-msg-user{align-self:flex-end;background:#fff3e8;color:#1a1a1a;border-bottom-right-radius:4px}',
    '.sc-msg-bot{align-self:flex-start;background:#fff;color:#1a1a1a;border:1px solid #e9ecef;border-bottom-left-radius:4px}',
    '.sc-msg-bot a{color:#ee7000;text-decoration:underline}',
    '.sc-msg-bot strong{font-weight:600}',
    '.sc-msg-bot ul,.sc-msg-bot ol{margin:4px 0 4px 18px;padding:0}',
    // Typing
    '.sc-typing{align-self:flex-start;padding:10px 14px;background:#fff;border:1px solid #e9ecef;border-radius:12px;border-bottom-left-radius:4px;display:none;flex-shrink:0}',
    '.sc-typing span{display:inline-block;width:7px;height:7px;border-radius:50%;background:#bbb;margin:0 2px;animation:sc-bounce .6s infinite alternate}',
    '.sc-typing span:nth-child(2){animation-delay:.2s}',
    '.sc-typing span:nth-child(3){animation-delay:.4s}',
    '@keyframes sc-bounce{to{opacity:.3;transform:translateY(-4px)}}',
    // Input
    '.sc-input-area{display:flex;padding:12px;border-top:1px solid #e9ecef;background:#fff;gap:8px;flex-shrink:0}',
    '.sc-input-area textarea{flex:1;border:1px solid #e9ecef;border-radius:8px;padding:10px 12px;font-size:16px;font-family:inherit;resize:none;outline:none;min-height:40px;max-height:80px;line-height:1.4}',
    '.sc-input-area textarea:focus{border-color:#ee7000}',
    '.sc-input-area button{background:#ee7000;color:#fff;border:none;border-radius:8px;width:40px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background .15s}',
    '.sc-input-area button:hover{background:#cc5d00}',
    '.sc-input-area button:disabled{background:#ccc;cursor:not-allowed}',
    // Escalation
    '.sc-escalation{text-align:center;padding:12px;font-size:.85rem;color:#525c69;background:#fff3e8;border-top:1px solid #fde5c8;flex-shrink:0}',
    '.sc-escalation a{color:#ee7000;font-weight:600}',
    // Body lock class — applied to html element
    '.sc-noscroll{overflow:hidden!important;position:fixed!important;width:100%!important;height:100%!important}',
    // Mobile: TRUE full-screen, cover everything including nav
    '@media(max-width:600px){',
    '  #slate-chat-panel.open{position:fixed!important;top:0!important;left:0!important;right:0!important;bottom:0!important;width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;border-radius:0!important;z-index:99999!important}',
    '  .sc-header{padding-top:env(safe-area-inset-top,0px)}',
    '  .sc-close-mobile{display:flex!important;align-items:center;gap:6px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.25);color:#fff;height:36px;padding:0 14px;border-radius:8px;cursor:pointer;font-size:15px;font-weight:500;font-family:inherit;white-space:nowrap}',
    '  .sc-header-btn#sc-close{display:none!important}',
    '  .sc-header-btn#sc-new{width:36px;height:36px;font-size:18px}',
    '  .sc-messages{padding:12px}',
    '  .sc-msg{max-width:92%}',
    '  .sc-input-area{padding:10px;padding-bottom:calc(10px + env(safe-area-inset-bottom,0px))}',
    '  #slate-chat-bubble{bottom:16px;right:16px;width:52px;height:52px}',
    '}'
  ].join('\n');
  document.head.appendChild(style);

  var state = loadState();
  var isOpen = false;
  var isStreaming = false;
  var savedScrollY = 0;

  function isMobile() { return window.innerWidth <= 600; }

  function loadState() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        var parsed = JSON.parse(saved);
        if (parsed && Array.isArray(parsed.messages)) return parsed;
      }
    } catch (e) {}
    return { messages: [], id: generateId() };
  }

  function saveState() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {}
  }

  function generateId() {
    return 'sc_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  }

  function userTurnCount() {
    return state.messages.filter(function (m) { return m.role === 'user'; }).length;
  }

  // Build DOM
  var bubble = document.createElement('button');
  bubble.id = 'slate-chat-bubble';
  bubble.setAttribute('aria-label', IS_SPANISH ? 'Abrir chat de soporte' : 'Open support chat');
  bubble.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>';

  var panel = document.createElement('div');
  panel.id = 'slate-chat-panel';
  panel.innerHTML = [
    '<div class="sc-header">',
    '  <div class="sc-header-left"><div class="sc-header-dot"></div><span>' + (IS_SPANISH ? 'Soporte Slate' : 'Slate Support') + '</span></div>',
    '  <div class="sc-header-actions">',
    '    <button class="sc-header-btn" id="sc-new" title="' + (IS_SPANISH ? 'Nueva conversaci\u00f3n' : 'New conversation') + '">&#x21bb;</button>',
    '    <button class="sc-header-btn" id="sc-close" title="' + (IS_SPANISH ? 'Cerrar' : 'Close') + '">&times;</button>',
    '    <button class="sc-close-mobile" id="sc-close-mobile">&larr; ' + (IS_SPANISH ? 'Cerrar' : 'Close') + '</button>',
    '  </div>',
    '</div>',
    '<div class="sc-messages" id="sc-messages"></div>',
    '<div class="sc-input-area">',
    '  <textarea id="sc-input" placeholder="' + (IS_SPANISH ? 'Haz una pregunta...' : 'Ask a question...') + '" rows="1"></textarea>',
    '  <button id="sc-send" aria-label="' + (IS_SPANISH ? 'Enviar' : 'Send') + '"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg></button>',
    '</div>'
  ].join('\n');

  var typingEl = document.createElement('div');
  typingEl.className = 'sc-typing';
  typingEl.innerHTML = '<span></span><span></span><span></span>';

  document.body.appendChild(bubble);
  document.body.appendChild(panel);

  var messagesEl = document.getElementById('sc-messages');
  var inputEl = document.getElementById('sc-input');
  var sendBtn = document.getElementById('sc-send');

  // iOS scroll prevention — block touchmove on everything except messages area
  function onTouchMove(e) {
    if (!isOpen || !isMobile()) return;
    var el = e.target;
    while (el && el !== document) {
      if (el === messagesEl) return; // allow scrolling inside messages
      el = el.parentElement;
    }
    e.preventDefault();
  }

  // Handle keyboard on iOS — adjust panel height to visual viewport
  function syncPanelToViewport() {
    if (!isOpen || !isMobile() || !window.visualViewport) return;
    var vvh = window.visualViewport.height;
    var vvTop = window.visualViewport.offsetTop;
    panel.style.height = vvh + 'px';
    panel.style.top = vvTop + 'px';
    panel.style.bottom = 'auto';
    scrollBottom();
  }

  // Render
  function render() {
    messagesEl.innerHTML = '';
    appendMessageEl('bot', IS_SPANISH ? WELCOME_MSG_ES : WELCOME_MSG);
    for (var i = 0; i < state.messages.length; i++) {
      var m = state.messages[i];
      appendMessageEl(m.role === 'user' ? 'user' : 'bot', m.content);
    }
    if (userTurnCount() >= MAX_TURNS) showEscalation();
    scrollBottom();
  }

  function appendMessageEl(type, text) {
    var div = document.createElement('div');
    div.className = 'sc-msg sc-msg-' + (type === 'user' ? 'user' : 'bot');
    if (type === 'bot') {
      div.innerHTML = formatMarkdown(text);
    } else {
      div.textContent = text;
    }
    messagesEl.appendChild(div);
    return div;
  }

  function formatMarkdown(text) {
    var html = escapeHtml(text);
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    html = html.replace(/(?<!="|'>)(\/[a-z0-9-]+\.html(?:#[a-z0-9-]*)?)/g, '<a href="$1">$1</a>');
    html = html.replace(/^- (.+)/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
    html = html.replace(/\n/g, '<br>');
    return html;
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function scrollBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function showEscalation() {
    var existing = panel.querySelector('.sc-escalation');
    if (existing) existing.remove();
    var esc = document.createElement('div');
    esc.className = 'sc-escalation';
    var smsNum = IS_SPANISH ? '+18312267831' : '+18312308743';
    var smsLabel = IS_SPANISH ? 'Escr\u00edbenos' : 'Text us';
    var moreHelp = IS_SPANISH ? '\u00bfNecesitas m\u00e1s ayuda?' : 'Need more help?';
    var contactLabel = IS_SPANISH ? 'Contactar Soporte' : 'Contact Support';
    var contactHref = IS_SPANISH ? '/es/contact.html' : '/contact.html';
    var orWord = IS_SPANISH ? 'o visita' : 'or visit';
    esc.innerHTML = moreHelp + ' <a href="sms:' + smsNum + '">' + smsLabel + '</a> ' + orWord + ' <a href="' + contactHref + '">' + contactLabel + '</a>';
    panel.querySelector('.sc-input-area').before(esc);
  }

  function openChat() {
    isOpen = true;
    panel.classList.add('open');
    bubble.style.display = 'none';

    if (isMobile()) {
      // Save scroll position, then lock BOTH html and body
      savedScrollY = window.scrollY;
      document.documentElement.classList.add('sc-noscroll');
      document.body.classList.add('sc-noscroll');
      document.body.style.top = '-' + savedScrollY + 'px';
      // Block touch scrolling on the page behind
      document.addEventListener('touchmove', onTouchMove, { passive: false });
      // Sync to visual viewport for keyboard handling
      if (window.visualViewport) {
        window.visualViewport.addEventListener('resize', syncPanelToViewport);
        window.visualViewport.addEventListener('scroll', syncPanelToViewport);
      }
    }

    render();
    // Don't auto-focus on mobile to avoid keyboard popup
    if (!isMobile()) inputEl.focus();
  }

  function closeChat() {
    isOpen = false;
    panel.classList.remove('open');
    bubble.style.display = 'flex';
    // Reset viewport overrides
    panel.style.height = '';
    panel.style.top = '';
    panel.style.bottom = '';

    // Unlock scroll
    document.documentElement.classList.remove('sc-noscroll');
    document.body.classList.remove('sc-noscroll');
    document.body.style.top = '';
    window.scrollTo(0, savedScrollY);
    document.removeEventListener('touchmove', onTouchMove);
    if (window.visualViewport) {
      window.visualViewport.removeEventListener('resize', syncPanelToViewport);
      window.visualViewport.removeEventListener('scroll', syncPanelToViewport);
    }
  }

  function newChat() {
    state = { messages: [], id: generateId() };
    saveState();
    var esc = panel.querySelector('.sc-escalation');
    if (esc) esc.remove();
    render();
    inputEl.disabled = false;
    sendBtn.disabled = false;
    if (!isMobile()) inputEl.focus();
  }

  async function sendMessage() {
    var text = inputEl.value.trim();
    if (!text || isStreaming) return;
    if (text.length > 1000) text = text.slice(0, 1000);

    if (userTurnCount() >= MAX_TURNS) { showEscalation(); return; }

    state.messages.push({ role: 'user', content: text });
    saveState();
    appendMessageEl('user', text);
    inputEl.value = '';
    inputEl.style.height = 'auto';
    scrollBottom();

    isStreaming = true;
    sendBtn.disabled = true;
    typingEl.style.display = 'block';
    messagesEl.appendChild(typingEl);
    scrollBottom();

    var botDiv = document.createElement('div');
    botDiv.className = 'sc-msg sc-msg-bot';
    botDiv.textContent = '';
    var fullText = '';

    try {
      var response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: state.messages, language: IS_SPANISH ? 'es' : 'en' }),
      });

      typingEl.style.display = 'none';
      if (typingEl.parentNode) typingEl.parentNode.removeChild(typingEl);

      if (!response.ok) {
        var errData;
        try { errData = await response.json(); } catch (e) { errData = {}; }
        if (response.status === 429) {
          fullText = IS_SPANISH
            ? "Est\u00e1s enviando mensajes muy r\u00e1pido. Espera unos minutos e intenta de nuevo."
            : "You're sending messages too fast. Wait a few minutes and try again.";
        } else {
          fullText = errData.error || (IS_SPANISH
            ? "Algo sali\u00f3 mal. Intenta de nuevo, o escr\u00edbenos al +1 (831) 226-7831."
            : "Something went wrong. Try again, or text us at +1 (831) 230-8743.");
        }
        botDiv.innerHTML = formatMarkdown(fullText);
        messagesEl.appendChild(botDiv);
        state.messages.push({ role: 'assistant', content: fullText });
        saveState();
        scrollBottom();
        isStreaming = false;
        sendBtn.disabled = false;
        return;
      }

      messagesEl.appendChild(botDiv);
      scrollBottom();

      var reader = response.body.getReader();
      var decoder = new TextDecoder();
      var buffer = '';

      while (true) {
        var result = await reader.read();
        if (result.done) break;
        buffer += decoder.decode(result.value, { stream: true });
        var lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (var i = 0; i < lines.length; i++) {
          var line = lines[i].trim();
          if (!line.startsWith('data: ')) continue;
          var data = line.slice(6);
          if (data === '[DONE]') continue;
          try {
            var parsed = JSON.parse(data);
            if (parsed.content) {
              fullText += parsed.content;
              botDiv.innerHTML = formatMarkdown(fullText);
              scrollBottom();
            }
          } catch (e) {}
        }
      }

      if (fullText) {
        state.messages.push({ role: 'assistant', content: fullText });
        saveState();
      }
      if (userTurnCount() >= MAX_TURNS) showEscalation();

    } catch (err) {
      typingEl.style.display = 'none';
      if (typingEl.parentNode) typingEl.parentNode.removeChild(typingEl);
      fullText = IS_SPANISH
        ? "No se pudo conectar. Revisa tu internet e intenta de nuevo, o escr\u00edbenos al +1 (831) 226-7831."
        : "Couldn't connect. Check your internet and try again, or text us at +1 (831) 230-8743.";
      botDiv.innerHTML = formatMarkdown(fullText);
      messagesEl.appendChild(botDiv);
      state.messages.push({ role: 'assistant', content: fullText });
      saveState();
      scrollBottom();
    }

    isStreaming = false;
    sendBtn.disabled = false;
  }

  // Events
  bubble.addEventListener('click', openChat);
  document.getElementById('sc-close').addEventListener('click', closeChat);
  document.getElementById('sc-close-mobile').addEventListener('click', closeChat);
  document.getElementById('sc-new').addEventListener('click', newChat);
  sendBtn.addEventListener('click', sendMessage);

  inputEl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  });

  inputEl.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 80) + 'px';
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen) closeChat();
  });

})();
