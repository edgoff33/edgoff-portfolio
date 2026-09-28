#!/usr/bin/env python3
"""
Ed Goff portfolio - site generator.

One source of truth, two outputs:

  DEPLOY   /mnt/user-data/outputs/edgoff-portfolio/   pages link ../assets/site.css
  PREVIEW  /mnt/user-data/outputs/previews/           CSS inlined, renders in chat

The deploy folder is the only thing that ever gets uploaded to GitHub.
The preview folder is for looking at before publishing. Never upload it.

Because both outputs come from the same body files and the same stylesheet,
they cannot drift apart.

To add a page: create src/pages/<name>.body.html, then add an entry to PAGES.
"""

import datetime
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
DEPLOY = pathlib.Path("/mnt/user-data/outputs/edgoff-portfolio")
PREVIEW = pathlib.Path("/mnt/user-data/outputs/previews")

# The live domain. Canonical tags, og:url, sitemap and robots.txt all derive
# from this. Set to None and they are omitted rather than emitted wrong.
DOMAIN = "https://edgoff.net"

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Carlito:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">'
)

ICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
    "<rect width='100' height='100' fill='%232E4057'/>"
    "<text x='50' y='68' font-size='52' font-family='Calibri,sans-serif' "
    "fill='white' text-anchor='middle'>EG</text></svg>\">"
)

# out_path, body file, <title>, meta description
PAGES = [
    ("index.html", "index.body.html",
     "Ed Goff, CISSP - Enterprise Cybersecurity Executive",
     "Ed Goff, CISSP - enterprise cybersecurity executive. Security architecture, "
     "identity and access management, AI governance. Contributor to the NIST "
     "Cybersecurity Framework and DOE energy sector standards."),

    ("writing/index.html", "writing.body.html",
     "Writing - Ed Goff",
     "Short pieces on identity and access management, AI governance, security "
     "architecture, and regulatory engagement, by Ed Goff, CISSP."),

    ("case-studies/index.html", "case-studies.body.html",
     "Case Studies - Ed Goff",
     "Accounts of specific security and identity transformations: the problem, "
     "what was built, and what it means for a reader facing the same problem."),

    ("how-i-work/index.html", "how-i-work.body.html",
     "How I Work - Ed Goff",
     "Reusable frameworks and operating artifacts for assessing and building "
     "enterprise security and identity programs."),

    ("how-i-work/30-60-90-day-plan/index.html",
     "how-i-work-30-60-90-day-plan.body.html",
     "How I Plan the First Ninety Days - Ed Goff",
     "The three-phase method Ed Goff, CISSP uses for the first ninety days in a "
     "security leadership role, with the detailed one-page plan as a PDF."),

    ("how-i-work/blended-cyber-governance-model/index.html",
     "how-i-work-blended-cyber-governance-model.body.html",
     "The Blended Cyber Governance Model - Ed Goff",
     "A governance model blending NIST CSF 2.0, the IIA Three Lines Model and "
     "people, process and technology around data, with eight governance "
     "dimensions mapped to the CSF Govern function."),

    ("how-i-work/shared-purpose-in-a-technical-team/index.html",
     "how-i-work-shared-purpose-in-a-technical-team.body.html",
     "How I Build Shared Purpose in a Technical Team - Ed Goff",
     "How Ed Goff, CISSP used a facilitated Find Your Why session to give a "
     "thirty-six person security architecture team a shared purpose, what the "
     "leader has to do that a facilitator cannot, and what changed afterward."),

    ("published-work/index.html", "published-work.body.html",
     "Published Work - Ed Goff",
     "Federal and industry publications by Ed Goff, CISSP, including a peer-reviewed "
     "ACM paper and Department of Energy procurement language for control systems."),

    ("standards/index.html", "standards.body.html",
     "Standards and National Initiatives - Ed Goff",
     "Ed Goff's contributions to the original NIST Cybersecurity Framework, ES-C2M2, "
     "NERC CIP, and Department of Energy critical infrastructure standards."),

    ("career/index.html", "career.body.html",
     "Career - Ed Goff",
     "Enterprise security and identity leadership across critical energy "
     "infrastructure and the nation's largest financial institutions."),

    ("capabilities/index.html", "capabilities.body.html",
     "Capabilities - Ed Goff",
     "Security architecture, identity and access management, AI governance, "
     "operational technology, and enterprise cybersecurity leadership."),

    ("credentials/index.html", "credentials.body.html",
     "Credentials - Ed Goff",
     "Certifications, education, and professional development, each with an "
     "issuer-hosted verification link."),

    ("404.html", "404.body.html",
     "Page not found - Ed Goff",
     "That page could not be found."),
]


def head(title, desc, css_href, canonical=None):
    tags = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{title}</title>",
        f'<meta name="description" content="{desc}">',
        '<meta name="author" content="Ed Goff">',
    ]
    if canonical:
        tags += [
            f'<link rel="canonical" href="{canonical}">',
            '<meta property="og:type" content="profile">',
            f'<meta property="og:title" content="{title}">',
            f'<meta property="og:description" content="{desc}">',
            f'<meta property="og:url" content="{canonical}">',
            '<meta name="twitter:card" content="summary">',
        ]
    tags += [ICON, FONTS, css_href]
    return "\n".join(tags)


def wrap(title, desc, css_href, body, canonical=None):
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        + head(title, desc, css_href, canonical)
        + "\n</head>\n<body>\n"
        + body.rstrip("\n")
        + "\n</body>\n</html>\n"
    )


def build():
    css = (SRC / "site.css").read_text()

    for out in (DEPLOY, PREVIEW):
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)

    (DEPLOY / "assets").mkdir()
    (DEPLOY / "assets" / "site.css").write_text(css)

    # src/static mirrors into the deploy folder at the same paths, so a page at
    # how-i-work/<slug>/ references its own images and PDFs by bare filename.
    # The preview is flat, so the same files are ALSO dropped at the preview root
    # by basename, which is where a flattened page looks for them.
    static = SRC / "static"
    if static.is_dir():
        for f in sorted(static.rglob("*")):
            if f.is_file():
                dest = DEPLOY / f.relative_to(static)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                shutil.copy2(f, PREVIEW / f.name)

    # GitHub Pages runs Jekyll unless told otherwise. For plain static HTML,
    # turning it off makes file serving predictable.
    (DEPLOY / ".nojekyll").write_text("")

    built = []
    for out_path, body_file, title, desc in PAGES:
        body = (SRC / "pages" / body_file).read_text()
        depth = out_path.count("/")

        # 404.html is served in response to ANY bad URL, at any depth, so no
        # relative path is correct and an absolute one only works at a domain
        # root. Inline its CSS so it renders wherever it is served from.
        rel = ("../" * depth) + "assets/site.css?v=" + source_version()
        inline_css = out_path == "404.html"

        canonical = None
        if DOMAIN and out_path != "404.html":
            slug = "" if out_path == "index.html" else out_path[: -len("index.html")]
            canonical = f"{DOMAIN.rstrip('/')}/{slug}"

        # deploy: linked stylesheet, except the 404 which carries its own
        dep = DEPLOY / out_path
        dep.parent.mkdir(parents=True, exist_ok=True)
        css_tag = (
            f"<style>\n{css}\n</style>"
            if inline_css
            else f'<link rel="stylesheet" href="{rel}">'
        )
        dep.write_text(wrap(title, desc, css_tag, body, canonical))

        # preview: inlined stylesheet, flattened filename so nothing nests
        flat = out_path.replace("/", "-").replace("-index.html", ".html")
        if flat == "index.html":
            flat = "hub.html"
        prev_body = body
        # Static files are dropped at the preview root by basename, so strip any
        # directory prefix from asset references for the preview copy only.
        prev_body = re.sub(r'(src|srcset)="([^"]*)"',
                           lambda m: '%s="%s"' % (
                               m.group(1),
                               re.sub(r'(?<![\w:/])[\w./-]*/(?=[\w-]+\.(?:jpg|jpeg|png|gif|svg|webp|pdf))',
                                      '', m.group(2))
                           ) if not m.group(2).startswith(('http', 'data:', '/')) else m.group(0),
                           prev_body)
        if out_path != "index.html":
            # The preview is flat, so every ../ would escape the folder. Rewrite
            # each depth to the flattened file that actually holds that page:
            # deepest first, so ../../ is not eaten by the ../ rule.
            for d in range(depth, 0, -1):
                up = "../" * d
                if d == depth:
                    target = "hub.html"            # d levels up is always the hub
                else:
                    anc = out_path.split("/")[: depth - d] + ["index.html"]
                    target = "/".join(anc).replace("/", "-").replace("-index.html", ".html")
                prev_body = prev_body.replace(f'href="{up}"', f'href="{target}"')
                prev_body = re.sub(rf'href="{re.escape(up)}(?=#)', f'href="{target}', prev_body)
        (PREVIEW / flat).write_text(
            wrap(title, desc, f"<style>\n{css}\n</style>", prev_body)
        )
        built.append((out_path, flat))

    if DOMAIN:
        base = DOMAIN.rstrip("/")
        today = datetime.date.today().isoformat()

        # sitemap: real pages only, never the 404
        locs = []
        for out_path, _, _, _ in PAGES:
            if out_path == "404.html":
                continue
            slug = "" if out_path == "index.html" else out_path[: -len("index.html")]
            pri = "1.0" if out_path == "index.html" else "0.8"
            locs.append(
                f"  <url>\n    <loc>{base}/{slug}</loc>\n"
                f"    <lastmod>{today}</lastmod>\n"
                f"    <priority>{pri}</priority>\n  </url>"
            )
        (DEPLOY / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(locs)
            + "\n</urlset>\n"
        )

        (DEPLOY / "robots.txt").write_text(
            "User-agent: *\nAllow: /\n\n" f"Sitemap: {base}/sitemap.xml\n"
        )

    return built


def source_version():
    """Print the version stamp so a build always says which source made it."""
    f = ROOT / "SOURCE-VERSION.txt"
    if f.exists():
        for line in f.read_text().splitlines():
            if line.startswith("VERSION:"):
                return line.split(":", 1)[1].strip()
    return "unstamped"


if __name__ == "__main__":
    print(f"source version: {source_version()}\n")
    for dep, prev in build():
        print(f"  {dep:34} -> preview: {prev}")
    print(f"\ndeploy:  {DEPLOY}")
    print(f"preview: {PREVIEW}   (never upload this)")
