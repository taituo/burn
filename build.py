#!/usr/bin/env python3
"""Build the burn site: posts/*.md -> docs/posts/*.html + docs/index.html.

Usage:  pip install markdown && python3 build.py

Each post is a markdown file in posts/ named NNN-slug.md with front matter:

    ---
    title: Post title
    vol: 2
    date: 2026-12-01
    author: Tuomas Taini
    summary: One or two sentences for the index card.
    play: play/some-game.html   (optional: a game version of the post)
    ---
"""
import html
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).parent
POSTS = ROOT / "posts"
OUT = ROOT / "docs"

SITE = "Ruthless experience of a delusional agentic engineer"
AUTHOR = "Tuomas Taini"
REPO = "https://github.com/taituo/burn"
GLOAM = "https://taituo.github.io/gloam/"
PALETTES = [("ember", "#f2c23a"), ("moss", "#9fd14f"), ("frost", "#6fbef0"),
            ("ghost", "#c6b6f2"), ("blood", "#e2453c"), ("bone", "#e9dfc4")]


def parse(path):
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = text[m.end():]
    slug = re.sub(r"^\d+-", "", path.stem)
    meta.setdefault("title", slug.replace("-", " "))
    meta.setdefault("author", AUTHOR)
    return slug, meta, body


def page(title, body, prefix, description=""):
    pals = "".join(
        f'<button data-p="{p}" style="background:{c}" aria-label="{p} palette" aria-pressed="false"></button>'
        for p, c in PALETTES)
    return f"""<!doctype html>
<html lang="en" data-pal="ember" data-type="mono">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="author" content="{AUTHOR}">
<link rel="preload" href="{prefix}fonts/Gloam-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{prefix}fonts/GloamBoneMono-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefix}assets/burn.css">
</head>
<body>
<header class="bar"><div class="wrap in">
  <a class="mark lan" href="{prefix}index.html">Burn</a>
  <nav class="mono"><a href="{prefix}index.html#articles">Articles</a><a href="{REPO}">Source</a></nav>
  <div class="tools">
    <button id="type" class="chip mono" aria-pressed="false" title="Toggle uppercase Bone Mono for body text">Mono</button>
    <div class="pals">{pals}</div>
  </div>
</div></header>
{body}
<footer><div class="wrap in mono">
  <span>&copy; 2026 {AUTHOR}</span>
  <span>Set in <a href="{GLOAM}">Gloam</a> &middot; <a href="{REPO}">Source</a></span>
</div></footer>
<script src="{prefix}assets/burn.js"></script>
<script src="{prefix}play/assets/dither.js"></script>
<script src="{prefix}assets/fire.js"></script>
</body>
</html>
"""


def vol(meta):
    v = meta.get("vol", "")
    return f"Vol. {int(v):02d}" if v.isdigit() else ""


def main():
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    posts = []
    (OUT / "posts").mkdir(parents=True, exist_ok=True)
    for path in sorted(POSTS.glob("*.md")):
        slug, meta, body = parse(path)
        md.reset()
        content = md.convert(body)
        bits = [b for b in (meta.get("date", ""), meta["author"]) if b]
        metaline = "".join(f"<span>{html.escape(b)}</span>" for b in bits)
        summary = meta.get("summary", "")
        article = f"""<main class="col">
<div class="post-head">
  <div class="kicker mono">{html.escape(vol(meta) or "Article")}</div>
  <h1 class="mono">{html.escape(meta["title"])}</h1>
  <div class="meta mono">{metaline}</div>
  {f'<p class="sum">{html.escape(summary)}</p>' if summary else ''}
  {f'<a class="btn mono" href="../{meta["play"]}">&#x25B6; Play this article</a>' if meta.get('play') else ''}
</div>
<article class="prose">
{content}
<a class="back mono" href="../index.html">&larr; All articles</a>
</article>
</main>"""
        (OUT / "posts" / f"{slug}.html").write_text(
            page(f'{meta["title"]} · {SITE}', article, "../", summary), encoding="utf-8")
        posts.append((slug, meta))
        print("built", slug)

    cards = []
    for slug, meta in sorted(posts, key=lambda p: p[1].get("date", ""), reverse=True):
        bits = [b for b in (vol(meta), meta.get("date", "")) if b]
        play = f'<a class="btn mono" href="{meta["play"]}">&#x25B6; Play</a>' if meta.get("play") else ""
        cards.append(f"""<div class="px card">
  <div class="meta mono">{' &middot; '.join(html.escape(b) for b in bits)}</div>
  <h3 class="mono"><a href="posts/{slug}.html">{html.escape(meta["title"])}</a></h3>
  <p>{html.escape(meta.get("summary", ""))}</p>
  <div class="acts">{play}<a class="btn ghost mono" href="posts/{slug}.html">Read &rarr;</a></div>
</div>""")

    index = f"""<main>
<section class="wrap hero">
  <div class="kicker mono">By {AUTHOR}</div>
  <h1 class="mono">Ruthless experience of a <b>delusional</b> agentic engineer</h1>
  <p class="sub">Field notes from the token furnace: agents, harnesses, skills, and the ideas that show up at 23:00.</p>
</section>
<canvas id="fire" class="fire" aria-hidden="true"></canvas>
<section class="wrap" id="articles">
  <div class="list">
    <div class="sect mono">Articles &middot; {len(posts)}</div>
    {''.join(cards)}
  </div>
</section>
</main>"""
    (OUT / "index.html").write_text(
        page(SITE, index, "", "Field notes on agents, harnesses and skills by Tuomas Taini."),
        encoding="utf-8")
    print("built index")


if __name__ == "__main__":
    main()
