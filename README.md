# Burn

**Ruthless experience of a delusional agentic engineer.**
Field notes on agents, harnesses and skills, by Tuomas Taini.

**Site:** https://taituo.github.io/burn/

Set in [Gloam](https://taituo.github.io/gloam/), also by Tuomas Taini.

## Articles

| Vol | Title | Game |
|---|---|---|
| 01 | [How can we sleep when the tokens are burning](https://taituo.github.io/burn/posts/how-can-we-sleep-when-the-tokens-are-burning.html) | [▶ Tokens Burning](https://taituo.github.io/burn/play/tokens-burning.html) |

## Writing a new article

1. Add `posts/NNN-slug.md` with front matter:

   ```markdown
   ---
   title: Post title
   vol: 2
   date: 2026-12-01
   author: Tuomas Taini
   summary: One or two sentences for the index card.
   play: play/some-game.html   # optional
   ---
   ```

2. Build:

   ```sh
   pip install markdown
   python3 build.py
   ```

3. Commit `posts/` and `docs/`. GitHub Pages serves `docs/` from `main`.

## Layout

```text
posts/            markdown sources
build.py          posts/*.md -> docs/posts/*.html + docs/index.html
docs/             the published site
  assets/         burn.css, burn.js, fire.js (dithered fire band)
  play/           game versions of articles (Gloam dither kit in play/assets/)
  fonts/          Gloam woff2 files
```

The **Mono** button switches body text between uppercase Gloam Bone Mono (the default) and Gloam. The swatches switch the accent palette. Both are remembered per browser.

## Games

Each article can have a game version in `docs/play/`: a 640 × 360 pixel stage, Bayer-dithered scenes, a HUD and dither transitions between stages, built on the Gloam dither kit. Controls: ◀ ▶ (or tap or swipe), P cycles the palette, M toggles sound, F goes fullscreen.
