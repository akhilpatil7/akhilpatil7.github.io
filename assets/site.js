/* ═══════════════════════════════════════════════════════════════
   Akhil Patil — Field Notes
   Progressive enhancement only. Every byte of content is already in
   the HTML; this file adds navigation, progress, and filtering.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  var nav = document.getElementById('nav');

  /* ── Nav: shadow on scroll ─────────────────────────────────── */
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('scrolled', window.scrollY > 36);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    /* ── Nav: mobile menu ────────────────────────────────────── */
    var toggle = nav.querySelector('.nav-toggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        var open = nav.classList.toggle('menu-open');
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      nav.querySelectorAll('.nav-links a').forEach(function (a) {
        a.addEventListener('click', function () {
          nav.classList.remove('menu-open');
          toggle.setAttribute('aria-expanded', 'false');
        });
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && nav.classList.contains('menu-open')) {
          nav.classList.remove('menu-open');
          toggle.setAttribute('aria-expanded', 'false');
          toggle.focus();
        }
      });
    }
  }

  /* ── Reading progress ──────────────────────────────────────── */
  var bar = document.getElementById('progress');
  var article = document.querySelector('.post-body');
  if (bar && article) {
    var tick = function () {
      var rect = article.getBoundingClientRect();
      var total = rect.height - window.innerHeight;
      var done = total > 0 ? (-rect.top) / total : (rect.top <= 0 ? 1 : 0);
      bar.style.width = Math.min(100, Math.max(0, done * 100)) + '%';
    };
    tick();
    window.addEventListener('scroll', tick, { passive: true });
    window.addEventListener('resize', tick, { passive: true });
  }

  /* ── TOC scrollspy ─────────────────────────────────────────── */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (tocLinks.length) {
    var headings = tocLinks
      .map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); })
      .filter(Boolean);

    var spy = function () {
      var idx = 0;
      for (var i = 0; i < headings.length; i++) {
        if (headings[i].getBoundingClientRect().top <= 120) idx = i;
      }
      tocLinks.forEach(function (a, i) { a.classList.toggle('active', i === idx); });
    };
    spy();
    window.addEventListener('scroll', spy, { passive: true });
  }

  /* ── Category filter (blog index) ──────────────────────────── */
  var filterBtns = Array.prototype.slice.call(document.querySelectorAll('.filter-btn'));
  var rows = Array.prototype.slice.call(document.querySelectorAll('.post-row'));
  if (filterBtns.length && rows.length) {
    var apply = function (cat, push) {
      filterBtns.forEach(function (b) { b.classList.toggle('active', b.dataset.filter === cat); });
      rows.forEach(function (r) {
        r.classList.toggle('hidden', cat !== 'all' && r.dataset.cat !== cat);
      });
      var count = document.getElementById('post-count');
      if (count) {
        var n = rows.filter(function (r) { return !r.classList.contains('hidden'); }).length;
        count.textContent = n;
      }
      if (push) {
        var url = cat === 'all' ? location.pathname : location.pathname + '?topic=' + cat;
        history.replaceState(null, '', url);
      }
    };

    filterBtns.forEach(function (b) {
      b.addEventListener('click', function () { apply(b.dataset.filter, true); });
    });

    var initial = new URLSearchParams(location.search).get('topic');
    if (initial && filterBtns.some(function (b) { return b.dataset.filter === initial; })) {
      apply(initial, false);
    }
  }

  /* ── Copy link ─────────────────────────────────────────────── */
  document.querySelectorAll('[data-copy-link]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.dataset.copyLink || location.href;
      var done = function () {
        var prev = btn.getAttribute('aria-label');
        btn.setAttribute('aria-label', 'Link copied');
        btn.classList.add('copied');
        setTimeout(function () {
          btn.setAttribute('aria-label', prev);
          btn.classList.remove('copied');
        }, 1600);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () {});
      else done();
    });
  });

  /* ── Scroll reveal ─────────────────────────────────────────── */
  var targets = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('visible'); });
  } else {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -28px 0px' });
    targets.forEach(function (el) { obs.observe(el); });
  }
})();
