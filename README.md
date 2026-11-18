# Burn

**Ruthless experience of a delusional agentic engineer.**
Field notes on agents, harnesses and skills, by Tuomas Taini.

**Site:** https://taituo.github.io/burn/

Set in [Gloam](https://taituo.github.io/gloam/), also by Tuomas Taini.

## Articles

| Vol | Title |
|---|---|
| 01 | [How can we sleep when the tokens are burning](https://taituo.github.io/burn/posts/how-can-we-sleep-when-the-tokens-are-burning.html) |

## Writing a new article

1. Add `posts/NNN-slug.md` with front matter:

   ```markdown
   ---
   title: Post title
   vol: 2
   date: 2026-12-01
   author: Tuomas Taini
   summary: One or two sentences for the index card.
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
  assets/         burn.css, burn.js
  fonts/          Gloam woff2 files
```

The **Mono** button switches body text between uppercase Gloam Bone Mono (the default) and Gloam. The swatches switch the accent palette. Both are remembered per browser.
