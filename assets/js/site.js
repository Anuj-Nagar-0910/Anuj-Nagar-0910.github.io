/* Anuj Nagar portfolio: tiny, dependency-free enhancements. The site is fully readable without this file. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function store(get, k, v) { try { return get ? localStorage.getItem(k) : localStorage.setItem(k, v); } catch (e) { return null; } }
  function sess(get, k, v) { try { return get ? sessionStorage.getItem(k) : (v === null ? sessionStorage.removeItem(k) : sessionStorage.setItem(k, v)); } catch (e) { return null; } }
  function $(s, c) { return (c || doc).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); }

  /* ---------- theme ---------- */
  var themeBtn = $('#theme-btn');
  function applyTheme(t) { if (t) root.setAttribute('data-theme', t); }
  applyTheme(store(true, 'theme'));
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme') ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark';
    applyTheme(next); store(false, 'theme', next);
  });

  /* ---------- mobile menu ---------- */
  var menu = $('#menu'), menuBtn = $('#menu-btn');
  function setMenu(open) {
    if (!menu) return;
    menu.classList.toggle('is-open', open);
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    doc.body.style.overflow = open ? 'hidden' : '';
    if (open) { var f = $('a', menu); if (f) f.focus(); } else menuBtn.focus();
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () { setMenu(true); });
    $('.close', menu).addEventListener('click', function () { setMenu(false); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('is-open')) setMenu(false); });
    menu.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('a')) setMenu(false); });
  }

  /* ---------- fixed header after the hero ---------- */
  var head = $('.site-head');
  if (head && head.dataset.solidAfter) {
    var onScroll = function () {
      var y = window.scrollY, past = y > 140;
      head.classList.toggle('is-fixed', past);
      head.classList.toggle('head-solid', past);
    };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }

  /* ---------- page transitions (curtain) ---------- */
  var curtainLabel = $('.curtain span');
  function reveal() {
    if (!root.classList.contains('is-entering')) return;
    root.classList.remove('is-entering'); root.classList.add('is-revealing');
    sess(false, 'xnav', null);
    setTimeout(function () { root.classList.remove('is-revealing'); }, 900);
  }
  if (root.classList.contains('is-entering')) {
    if (doc.readyState === 'complete') setTimeout(reveal, 80); else window.addEventListener('load', function () { setTimeout(reveal, 80); });
    setTimeout(reveal, 2500); // never trap the visitor behind the curtain
  }
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { root.classList.remove('is-leaving', 'is-entering', 'is-revealing'); }
  });
  doc.addEventListener('click', function (e) {
    if (reduce || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.target === '_blank' || a.hasAttribute('download') || a.getAttribute('rel') === 'external') return;
    var url;
    try { url = new URL(a.href, location.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;
    if (url.pathname === location.pathname && url.search === location.search) return; // same page or hash jump
    if (!/\/$|\.html$/.test(url.pathname)) return;
    e.preventDefault();
    if (menu && menu.classList.contains('is-open')) setMenu(false);
    var label = a.getAttribute('data-label') || (a.textContent || '').trim().replace(/[\s→↗↓]+$/, '').slice(0, 28);
    if (curtainLabel) curtainLabel.textContent = label;
    sess(false, 'xnav', JSON.stringify({ l: label }));
    root.classList.add('is-leaving');
    setTimeout(function () { location.href = url.href; }, 480);
  });

  /* ---------- scroll reveal ---------- */
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    $$('[data-reveal]').forEach(function (el, i) { el.style.setProperty('--d', ((i % 4) * 0.06) + 's'); io.observe(el); });
  } else { $$('[data-reveal]').forEach(function (el) { el.classList.add('in'); }); }

  /* ---------- word-by-word highlight ---------- */
  var intro = $$('.intro [data-words]');
  if (intro.length && !reduce) {
    var groups = intro.map(function (p) {
      var out = [];
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            var frag = doc.createDocumentFragment();
            n.textContent.split(/(\s+)/).forEach(function (t) {
              if (!t) return;
              if (/^\s+$/.test(t)) { frag.appendChild(doc.createTextNode(t)); return; }
              var s = doc.createElement('span'); s.className = 'w'; s.textContent = t; frag.appendChild(s); out.push(s);
            });
            node.replaceChild(frag, n);
          } else if (n.nodeType === 1) walk(n);
        });
      })(p);
      return { el: p, words: out };
    });
    var tick = false;
    var paint = function () {
      tick = false;
      var vh = window.innerHeight;
      groups.forEach(function (g) {
        var r = g.el.getBoundingClientRect();
        var p = (vh * .82 - r.top) / (r.height + vh * .32);
        p = Math.max(0, Math.min(1, p));
        var n = Math.round(p * g.words.length);
        g.words.forEach(function (w, i) { w.classList.toggle('lit', i < n); });
      });
    };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(paint); } }, { passive: true });
    window.addEventListener('resize', paint); paint();
  }

  /* ---------- copy email ---------- */
  $$('[data-email]').forEach(function (b) {
    var addr = b.getAttribute('data-u') + '@' + b.getAttribute('data-d');
    var toast = $('.toast', b.parentNode);
    b.addEventListener('click', function (e) {
      e.preventDefault();
      var done = function () { if (toast) { toast.textContent = 'Copied. Write soon.'; toast.classList.add('show'); setTimeout(function () { toast.classList.remove('show'); }, 2400); } };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(addr).then(done, function () { location.href = 'mailto:' + addr; });
      else location.href = 'mailto:' + addr;
    });
  });

  /* ---------- Signal Lab (hero widget) ---------- */
  var lab = $('#lab');
  if (lab) {
    var RAW = 2.0, EST = 3.2, T0 = -3, T1 = 5, X0 = 14, X1 = 306;
    var slider = $('#off', lab), outv = $('#off-v', lab), trB = $('#trb', lab), dB = $('#dB', lab), lblB = $('#lblB', lab);
    var r1 = $('#r1', lab), r2 = $('#r2', lab), vd = $('#vd', lab), msg = $('#lab-msg', lab);
    var xOf = function (t) { return X0 + (t - T0) / (T1 - T0) * (X1 - X0); };
    var fmt = function (v) { return (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(1) + ' ms'; };
    var render = function (off) {
      off = parseFloat(off);
      var diff = RAW - off, xb = xOf(diff);
      trB.setAttribute('d', 'M' + X0 + ',108 H' + xb.toFixed(1) + ' V84 H' + X1);
      dB.setAttribute('x1', xb.toFixed(1)); dB.setAttribute('x2', xb.toFixed(1));
      lblB.setAttribute('x', Math.min(Math.max(xb + 4, 20), 250).toFixed(1));
      outv.textContent = off.toFixed(1) + ' ms';
      slider.setAttribute('aria-valuetext', off.toFixed(1) + ' milliseconds removed');
      r1.textContent = 'Raw timestamps: B vs A ' + fmt(RAW);
      var bad = diff < -0.05;
      r2.textContent = off === 0 ? 'No offset removed yet' : 'After removing offset: B vs A ' + fmt(diff);
      vd.textContent = bad ? 'NOK' : 'OK'; vd.className = 'verdict ' + (bad ? 'nok' : 'ok');
      msg.textContent = bad ? 'B actually started first. The raw view hid it.' : (off === 0 ? 'Looks fine: A seems to start first.' : 'Still A first once the offset is partly removed.');
    };
    slider.addEventListener('input', function () { render(slider.value); });
    $('#est', lab).addEventListener('click', function () { animateTo(EST); });
    $('#rst', lab).addEventListener('click', function () { animateTo(0); });
    var animateTo = function (target) {
      var start = parseFloat(slider.value), t0 = null;
      if (reduce) { slider.value = target; render(target); return; }
      var step = function (t) {
        if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 700), e = 1 - Math.pow(1 - k, 3);
        var v = start + (target - start) * e; slider.value = v.toFixed(2); render(v);
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    render(0);
    // gentle autoplay once, so the point lands even if nobody touches the slider
    if (!reduce && 'IntersectionObserver' in window) {
      var played = false;
      new IntersectionObserver(function (es, o) {
        if (es[0].isIntersecting && !played) { played = true; setTimeout(function () { if (parseFloat(slider.value) === 0) animateTo(EST); }, 1400); o.disconnect(); }
      }, { threshold: .6 }).observe(lab);
    }
  }

  /* ---------- pipeline highlight ---------- */
  var pipe = $('.pipe ol');
  if (pipe && !reduce) {
    var lis = $$('li', pipe), idx = 0;
    setInterval(function () { lis.forEach(function (l, i) { l.classList.toggle('on', i === idx); }); idx = (idx + 1) % lis.length; }, 1400);
  }

  /* ---------- Sig, the guide ---------- */
  var gEl = $('#guide'), cv = $('#sig'), bub = $('#bubble'), gtog = $('#guide-toggle');
  if (gEl && cv) {
    var hidden = store(true, 'guide') === 'off';
    var setHidden = function (h) { gEl.classList.toggle('is-hidden', h); gtog.setAttribute('aria-pressed', h ? 'true' : 'false'); gtog.title = h ? 'Show the guide' : 'Hide the guide'; store(false, 'guide', h ? 'off' : 'on'); };
    setHidden(hidden);
    gtog.addEventListener('click', function () { setHidden(!gEl.classList.contains('is-hidden')); });

    var N = 48, ctx = cv.getContext('2d'); cv.width = N; cv.height = N;
    var B = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]];
    var INK = '#12151B', LIGHT = '#F4EFE4', ACC = '#FF5A1F';
    var look = { x: 0, y: 0 }, t = 0, blink = 0, wave = 0;
    var draw = function () {
      ctx.clearRect(0, 0, N, N);
      var cx = 24, cy = 24, R = 15.5, i, j;
      // body (shoulders) dithered
      for (j = 36; j < N; j++) for (i = 4; i < 44; i++) {
        var dx = (i - 24) / 20, dy = (j - 50) / 13;
        if (dx * dx + dy * dy <= 1) {
          var br = .72 - (i - 4) / 40 * .5; ctx.fillStyle = br > (B[j & 3][i & 3] + .5) / 16 ? LIGHT : INK; ctx.fillRect(i, j, 1, 1);
        }
      }
      // head sphere with dithered shading
      for (j = 0; j < N; j++) for (i = 0; i < N; i++) {
        var x = (i - cx) / R, y = (j - cy) / R, d = x * x + y * y;
        if (d <= 1) {
          var z = Math.sqrt(1 - d), l = Math.max(0, (-.5 * x - .6 * y + .62 * z));
          var br2 = .22 + l * .9;
          ctx.fillStyle = br2 > (B[j & 3][i & 3] + .5) / 16 ? LIGHT : INK; ctx.fillRect(i, j, 1, 1);
        } else if (d <= 1.12) { ctx.fillStyle = INK; ctx.fillRect(i, j, 1, 1); }
      }
      // face panel
      ctx.fillStyle = LIGHT; ctx.fillRect(14, 19, 20, 12);
      ctx.fillStyle = INK; ctx.fillRect(13, 18, 22, 1); ctx.fillRect(13, 31, 22, 1); ctx.fillRect(13, 19, 1, 12); ctx.fillRect(34, 19, 1, 12);
      // eyes follow the pointer
      var ex = Math.round(look.x * 1.6), ey = Math.round(look.y * 1.2), eh = blink > 0 ? 1 : 4;
      ctx.fillStyle = INK; ctx.fillRect(17 + ex, 21 + ey + (blink > 0 ? 1 : 0), 3, eh); ctx.fillRect(28 + ex, 21 + ey + (blink > 0 ? 1 : 0), 3, eh);
      // mouth is a little signal wave
      for (i = 17; i <= 30; i++) { var my = 27 + Math.round(Math.sin((i - 17) / 13 * Math.PI * 2 + t * (wave > 0 ? 8 : 0)) * 1.2); ctx.fillRect(i, my, 1, 1); }
      // antennas
      var sw = Math.round(Math.sin(t * (wave > 0 ? 9 : 1.6)) * (wave > 0 ? 3 : 1));
      ctx.fillStyle = INK; for (i = 0; i < 7; i++) { ctx.fillRect(18 - i + (i > 3 ? sw : 0), 9 - i, 1, 1); ctx.fillRect(30 + i - (i > 3 ? sw : 0), 9 - i, 1, 1); }
      ctx.fillStyle = ACC; ctx.fillRect(10 + sw - 1, 1, 3, 3); ctx.fillRect(37 - sw - 1, 1, 3, 3);
    };
    var loop = function (ts) {
      t = ts / 1000; if (blink > 0) blink--; else if (Math.random() < .006) blink = 6; if (wave > 0) wave--;
      draw(); if (!reduce) requestAnimationFrame(loop);
    };
    draw(); if (!reduce) requestAnimationFrame(loop);
    window.addEventListener('pointermove', function (e) {
      var r = cv.getBoundingClientRect(), cx2 = r.left + r.width / 2, cy2 = r.top + r.height * .45;
      look.x = Math.max(-1, Math.min(1, (e.clientX - cx2) / 400)); look.y = Math.max(-1, Math.min(1, (e.clientY - cy2) / 400));
    }, { passive: true });

    var say = function (html) {
      if (!bub || bub.dataset.cur === html) return;
      bub.dataset.cur = html; bub.innerHTML = html; bub.classList.remove('pop', 'fade'); void bub.offsetWidth; if (!reduce) bub.classList.add('pop');
      clearTimeout(fadeT); fadeT = setTimeout(function () { bub.classList.add('fade'); }, window.innerWidth < 700 ? 4200 : 7000);
    };
    var fadeT = 0;
    var greet = gEl.getAttribute('data-greet'); if (greet) say(greet);
    var quips = ['Careful, I’m ticking at 1 kHz.', 'Beep. That’s my way of saying hi.', 'Fun fact: two clocks are never quite the same clock.', 'Ask me about clock offsets. I dare you.', 'Okay okay, I’ll stop wobbling.'];
    var clicks = 0;
    cv.addEventListener('click', function () {
      cv.classList.remove('hop'); void cv.offsetWidth; if (!reduce) cv.classList.add('hop');
      wave = 50; say(quips[clicks % quips.length]); clicks++;
    });
    if ('IntersectionObserver' in window) {
      var cur = null;
      var so = new IntersectionObserver(function (es) {
        es.forEach(function (en) { if (en.isIntersecting && en.target.getAttribute('data-says')) { cur = en.target; say(cur.getAttribute('data-says')); } });
      }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
      $$('[data-says]').forEach(function (s) { so.observe(s); });
    }
  }
})();
