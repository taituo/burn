// palette + type toggles; remembered per browser when storage is available
(function () {
  var root = document.documentElement;
  function get(k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return d; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  function pal(p) {
    root.setAttribute('data-pal', p); set('burn-pal', p);
    document.querySelectorAll('.pals button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.p === p ? 'true' : 'false');
    });
  }
  function type(t) {
    root.setAttribute('data-type', t); set('burn-type', t);
    var b = document.getElementById('type');
    if (b) b.setAttribute('aria-pressed', t === 'mono' ? 'true' : 'false');
  }

  pal(get('burn-pal', 'ember'));
  type(get('burn-type', 'mono'));

  document.querySelectorAll('.pals button').forEach(function (b) {
    b.addEventListener('click', function () { pal(b.dataset.p); });
  });
  var t = document.getElementById('type');
  if (t) t.addEventListener('click', function () {
    type(root.getAttribute('data-type') === 'mono' ? 'gloam' : 'mono');
  });
})();
