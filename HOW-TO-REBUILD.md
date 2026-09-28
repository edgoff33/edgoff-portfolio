# How to rebuild the site

This folder is the **source** for edgoff.net. The published site is generated
from it. Keep it — without it, changing the design means editing every page
by hand instead of one stylesheet.

## What is here

```
build.py                  the generator
verify.js                 automated checks
src/
├── site.css              the design system - one file governs every page
└── pages/
    ├── index.body.html         the hub
    ├── writing.body.html       section index
    ├── case-studies.body.html  section index
    ├── how-i-work.body.html    section index
    └── 404.body.html
```

Page files contain only what goes inside `<body>`. The generator adds the
doctype, head, title, description, canonical tags and stylesheet link.

## To rebuild

```
python3 build.py
```

Produces two folders:

- **edgoff-portfolio/** - upload this to GitHub. Pages link `assets/site.css`.
- **previews/** - for looking at before publishing. CSS inlined, names flattened.
  **Never upload this one.**

## To check it

```
node verify.js
```

Renders every page at phone and desktop width and confirms: the stylesheet
applied, no horizontal overflow, no failed asset requests, valid tag nesting.

## To add a page

1. Create `src/pages/<name>.body.html`
2. Add an entry to the `PAGES` list in `build.py`: output path, body file,
   `<title>`, meta description
3. Rebuild

## Settings that matter

`DOMAIN` near the top of `build.py` is set to `https://edgoff.net`. It drives
the canonical tags, og:url, sitemap.xml and robots.txt. Set it to `None` and
those are omitted rather than emitted wrong.

## If you lose this folder

Not fatal. The published HTML on GitHub contains everything - the source can be
reconstructed from it. You would lose the convenience, not the content.
