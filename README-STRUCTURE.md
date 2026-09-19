# Site structure

Reference for how this site is laid out and how to add to it.
This file is documentation and is not part of the published site.

---

## What uploads where

Upload the **whole `edgoff-portfolio` folder** to the repository root. In GitHub,
**Add file → Upload files** accepts a dragged folder and preserves the structure.

```
edgoff-portfolio/
├── index.html                → the hub, served at yourdomain.com/
├── 404.html                  → shown for any bad URL
├── .nojekyll                 → stops GitHub running the site through Jekyll
├── assets/
│   └── site.css              → the design system, shared by every page
├── writing/
│   └── index.html            → yourdomain.com/writing/
├── case-studies/
│   └── index.html            → yourdomain.com/case-studies/
└── how-i-work/
    └── index.html            → yourdomain.com/how-i-work/
```

There is a second folder called **`previews`**. That one is for looking at pages
before publishing them. **Never upload it.** Its files have the stylesheet baked in
and flattened filenames, both of which are wrong for the live site.

The rule: upload `edgoff-portfolio`, ignore `previews`.

---

## URLs

GitHub Pages serves `index.html` from any folder, so folders give clean addresses with
no `.html` showing:

| File | Address |
|---|---|
| `index.html` | `yourdomain.com/` |
| `writing/index.html` | `yourdomain.com/writing/` |
| `writing/agent-identity/index.html` | `yourdomain.com/writing/agent-identity/` |

### Slug rules

Lowercase, hyphens between words, descriptive, and **no dates in the path**.

A URL reading `/writing/2026-agentic-ai/` looks stale in eighteen months even if the
argument still holds. The date goes on the page, not in the address.

Public URLs are effectively permanent. Once a recruiter has forwarded a link, changing
the path breaks it silently. Pick the slug carefully the first time.

---

## Adding a piece

Every piece is a folder containing an `index.html`:

```
writing/
├── index.html                          ← the section listing
└── governing-agent-identity/
    └── index.html                      ← the piece
```

Two things happen for each new piece:

1. The piece itself is written into its own folder.
2. An entry is added to the section's `index.html`, in the `<ul class="listing">`
   block. That file contains a commented-out pattern showing the exact markup.

Pieces in `writing/` are listed newest first. Case studies are listed **strongest
first** rather than newest — a reader rarely gets past the second one.

---

## The two-output build

Both copies are generated from one set of source files, so they cannot drift apart.

- **Deploy copy** — pages link `assets/site.css`. One stylesheet governs everything;
  a design change is a single file.
- **Preview copy** — the same pages with the stylesheet inlined, so they render
  properly when sent into a chat for review before publishing.

The one exception is `404.html`, which carries its own inlined stylesheet in **both**
copies. A 404 is served in response to any bad URL at any depth, so no relative path
to the stylesheet is correct and an absolute one only works at a domain root. Inlining
it means the 404 renders wherever it is served from.

---

## Section pages are live but unlinked

`writing/`, `case-studies/` and `how-i-work/` are uploaded and working, but the hub's
navigation does not link to them yet. That is deliberate: a recruiter clicking
"Case Studies" and finding an empty page is worse than no link at all.

Each section page says honestly that content is in preparation and points back to the
relevant part of the hub. As soon as a section has its first real piece, its link is
added to the hub navigation.

---

## Before the custom domain is attached

Two things are waiting on the domain:

1. **`DOMAIN` in the build script.** While it is unset, the generator omits the
   `canonical` and `og:url` tags rather than emitting wrong ones. Set it to the real
   domain and rebuild, and every page gets correct tags.
2. **The 404's links.** They point at `/`, which is correct at a domain root. On a
   `username.github.io/repo/` address they would go to the GitHub user root instead.
   Harmless in the interim and correct the moment the domain is live.

A `sitemap.xml` is also worth adding once the domain exists. It needs absolute URLs,
so there is nothing useful to write before then.

---

## Design system

Defined once in `assets/site.css` and reused by every page. Do not redefine colors or
type in a page.

- **Type:** `Calibri, Carlito, "Segoe UI", -apple-system, BlinkMacSystemFont, system-ui, sans-serif`.
  Carlito is loaded from Google Fonts as the metric-compatible Calibri equivalent for
  readers not on Windows. Body 18px / 1.62, dropping to 17px below 640px.
- **Accent:** navy `#2E4057`; deep navy `#223047` for names and headings.
- **Dark mode** via `prefers-color-scheme`, with navy lightened to `#9db4d0` for
  contrast.
- **Hyphens only.** No pipe characters and no en or em dashes anywhere in visible text.
  This is checked on every build.
- **Print stylesheet** included. Recruiters print.

### Classes available to a new piece

| Class | Use |
|---|---|
| `.article` | Wraps the prose. Narrower measure than the hub |
| `.standfirst` | The opening paragraph, set larger and lighter |
| `.piece-meta` | Date and context line under the title |
| `.pullquote` | A sentence worth stopping on |
| `.aside` | A boxed note beside the main argument. Takes an `h4` |
| `.endnote` | Closing note, separated by a rule |
| `.listing` | The section index list of pieces |
| `.backlink` | "Back to the main page" at the foot of a piece |

---

## Checks that run on every build

- Every page renders with the stylesheet applied, at phone and desktop width
- No horizontal overflow at 390px
- No failed asset requests
- No pipe characters or en/em dashes in visible text
- No British spellings
- No certification number or full legal name anywhere in the output
