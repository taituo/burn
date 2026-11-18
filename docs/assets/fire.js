// dithered fire band for the index page (uses play/assets/dither.js)
(function () {
  var cv = document.getElementById('fire');
  if (!cv || !window.Dither) return;
  var D = window.Dither, W = 320, H = 24, buf = new D.Buffer(W, H), ctx = cv.getContext('2d');
  cv.width = W; cv.height = H;
  function h32(x, y) { var h = x * 374761393 + y * 668265263; h = Math.imul(h ^ (h >> 13), 1274126177); return ((h ^ (h >> 16)) >>> 0) / 4294967295; }
  function vn(x, y) { var xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, s = function (t) { return t * t * (3 - 2 * t); }; var a = h32(xi, yi), b = h32(xi + 1, yi), c = h32(xi, yi + 1), d = h32(xi + 1, yi + 1); return a + (b - a) * s(xf) + (c - a) * s(yf) + (a - b - c + d) * s(xf) * s(yf); }
  var last = 0;
  function frame(now) {
    requestAnimationFrame(frame);
    if (now - last < 60) return; last = now;
    var pal = document.documentElement.getAttribute('data-pal') || 'ember';
    var P = (D.PALETTES[pal] || D.PALETTES.ember).map(D.u32), t = now / 1000, px = buf.px;
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
      var base = y / H, n = vn(x / 6, y / 4 + t * 2.4) * .7 + vn(x / 2.5, y / 2 + t * 4.5) * .3;
      var v = Math.max(0, base * base * 1.5 * (.4 + n * .95) - .06);
      px[y * W + x] = v < .03 ? 0 : P[D.q(v, 8, x, y)];
    }
    for (var i = 0; i < 30; i++) {
      var sp = .35 + h32(i, 2) * .65, yy = Math.round(H - ((t * 9 * sp + h32(i, 3) * H) % H)), xx = Math.round(h32(i, 1) * W + Math.sin(t * 2 + i) * 2);
      if (yy < 14 && xx >= 0 && xx < W) px[yy * W + xx] = P[7];
    }
    buf.blit(ctx, W, H);
  }
  requestAnimationFrame(frame);
})();
