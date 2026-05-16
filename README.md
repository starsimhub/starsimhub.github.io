# Starsim website

Source for [starsim.org](https://starsim.org/). Built with [Eleventy](https://www.11ty.dev/) from [index.md](index.md) using the [base.njk](base.njk) layout. Site assets live in [assets/](assets/).

## Prerequisites

- Node.js (any recent LTS)

## Usage

```bash
./build.sh   # install deps and build the site into _site/
./serve.sh   # build and serve at http://localhost:8080 with live reload
./clean.sh   # remove _site/ and node_modules/
```

`npm install` is run automatically by `build.sh` and `serve.sh`. No `package-lock.json` is generated (see [.npmrc](.npmrc)).

## Publishing

Done automatically via GitHub Actions.

## Layout

- [index.md](index.md) — page content and frontmatter (title, nav, hero, footer)
- [base.njk](base.njk) — single HTML layout (navbar, hero, content, footer)
- [eleventy.config.js](eleventy.config.js) — Eleventy config and custom shortcodes (`section`, `cards`, `card`, `event`, `cite`, `topbtn`, `examples`, ...)
- [assets/](assets/) — CSS, JS, images, fonts (copied verbatim to the output)
