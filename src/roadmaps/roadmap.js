/* Shared roadmap engine — reads window.ROADMAP, renders into #rmApp,
   persists per-node status in localStorage under "rm-<id>". */
(function () {
  var R = window.ROADMAP;
  if (!R) return;
  var KEY = 'rm-' + R.id;
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { state = {}; }

  var allNodes = [];
  R.groups.forEach(function (g) { g.nodes.forEach(function (n) { allNodes.push(n); }); });
  var byId = {};
  allNodes.forEach(function (n) { byId[n.id] = n; });

  var app = document.getElementById('rmApp');

  /* ---- progress header ---- */
  var header = document.createElement('div');
  header.className = 'rm-progressbar';
  header.innerHTML =
    '<div class="rm-progress-row"><span><strong id="rmDoneCount">0</strong> of <strong>' + allNodes.length + '</strong> topics completed</span>' +
    '<span style="display:flex;align-items:center;gap:10px"><strong id="rmPct">0%</strong>' +
    '<button class="rm-reset" id="rmReset"><i class="fa-solid fa-rotate-left"></i> Reset</button></span></div>' +
    '<div class="rm-track"><div class="rm-fill" id="rmFill"></div></div>' +
    '<div class="rm-legend">' +
    '<span><span class="dot dot-pending"></span> Pending</span>' +
    '<span><span class="dot dot-learning"></span> In progress</span>' +
    '<span><span class="dot dot-done"></span> Done</span>' +
    '<span><span class="dot dot-skip"></span> Skipped</span>' +
    '<span style="opacity:.8"><i class="fa-regular fa-hand-pointer"></i> Click any topic to see resources &amp; track it</span>' +
    '</div>';
  app.appendChild(header);

  /* ---- spine ---- */
  var wrap = document.createElement('div');
  wrap.className = 'rm-wrap';
  var spine = document.createElement('div');
  spine.className = 'rm-spine';
  R.groups.forEach(function (g) {
    var gEl = document.createElement('div');
    gEl.className = 'rm-group';
    var head = document.createElement('div');
    head.className = 'rm-group-node';
    head.textContent = g.title;
    gEl.appendChild(head);
    var kids = document.createElement('div');
    kids.className = 'rm-children';
    g.nodes.forEach(function (n, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'rm-node ' + (i % 2 === 0 ? 'left' : 'right');
      b.id = 'rm-node-' + n.id;
      b.innerHTML = '<span class="rm-check"><i class="fa-solid fa-check"></i></span><span class="rm-label">' + n.title + '</span>';
      b.addEventListener('click', function () { openDrawer(n.id); });
      kids.appendChild(b);
    });
    gEl.appendChild(kids);
    spine.appendChild(gEl);
  });
  wrap.appendChild(spine);
  app.appendChild(wrap);

  /* ---- drawer ---- */
  var overlay = document.createElement('div');
  overlay.className = 'rm-overlay';
  var drawer = document.createElement('div');
  drawer.className = 'rm-drawer';
  drawer.innerHTML =
    '<div class="rm-drawer-head"><h3 id="rmDrawerTitle"></h3>' +
    '<button class="rm-close" id="rmClose" aria-label="Close"><i class="fa-solid fa-xmark"></i></button></div>' +
    '<div class="rm-drawer-body">' +
    '<p class="rm-desc" id="rmDrawerDesc"></p>' +
    '<div class="rm-status-row">' +
    '<button class="rm-status-btn" data-s="learning"><i class="fa-solid fa-spinner"></i> In progress</button>' +
    '<button class="rm-status-btn" data-s="done"><i class="fa-solid fa-check"></i> Done</button>' +
    '<button class="rm-status-btn" data-s="skip"><i class="fa-solid fa-forward"></i> Skip</button>' +
    '</div>' +
    '<div class="rm-res-title">Resources</div>' +
    '<div id="rmDrawerRes"></div>' +
    '</div>';
  document.body.appendChild(overlay);
  document.body.appendChild(drawer);

  var current = null;

  function openDrawer(id) {
    current = id;
    var n = byId[id];
    document.getElementById('rmDrawerTitle').textContent = n.title;
    document.getElementById('rmDrawerDesc').innerHTML = n.desc || '';
    var res = document.getElementById('rmDrawerRes');
    res.innerHTML = '';
    (n.resources || []).forEach(function (r) {
      var a = document.createElement('a');
      a.className = 'rm-res';
      a.href = r.href;
      var ext = r.t === 'ext';
      if (ext) { a.target = '_blank'; a.rel = 'noopener'; }
      a.innerHTML = '<i class="fa-solid ' + (ext ? 'fa-arrow-up-right-from-square' : 'fa-graduation-cap') + '"></i>' +
        '<span>' + r.label + '</span>' +
        '<span class="rm-res-tag' + (ext ? ' ext' : '') + '">' + (ext ? 'External' : 'On this site') + '</span>';
      res.appendChild(a);
    });
    if (!(n.resources || []).length) res.innerHTML = '<p class="rm-desc">No resources linked yet — coming soon.</p>';
    syncStatusButtons();
    overlay.classList.add('open');
    drawer.classList.add('open');
  }
  function closeDrawer() {
    overlay.classList.remove('open');
    drawer.classList.remove('open');
    current = null;
  }
  overlay.addEventListener('click', closeDrawer);
  document.getElementById('rmClose').addEventListener('click', closeDrawer);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDrawer(); });

  drawer.querySelectorAll('.rm-status-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (!current) return;
      var s = btn.getAttribute('data-s');
      if (state[current] === s) delete state[current]; else state[current] = s;
      localStorage.setItem(KEY, JSON.stringify(state));
      syncStatusButtons();
      refresh();
    });
  });

  function syncStatusButtons() {
    var s = state[current];
    drawer.querySelectorAll('.rm-status-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-s') === s);
    });
  }

  document.getElementById('rmReset').addEventListener('click', function () {
    if (!confirm('Reset all progress on this roadmap?')) return;
    state = {};
    localStorage.removeItem(KEY);
    refresh();
  });

  function refresh() {
    var done = 0, skip = 0;
    allNodes.forEach(function (n) {
      var s = state[n.id] || '';
      var el = document.getElementById('rm-node-' + n.id);
      if (s) el.setAttribute('data-status', s); else el.removeAttribute('data-status');
      if (s === 'done') done++;
      if (s === 'skip') skip++;
    });
    var denom = Math.max(1, allNodes.length - skip);
    var pct = Math.round((done / denom) * 100);
    document.getElementById('rmDoneCount').textContent = done;
    document.getElementById('rmPct').textContent = pct + '%';
    document.getElementById('rmFill').style.width = pct + '%';
  }
  refresh();
})();
