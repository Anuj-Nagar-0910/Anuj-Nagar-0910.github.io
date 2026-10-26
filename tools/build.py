#!/usr/bin/env python3
"""Static site generator for the portfolio. Usage (from the repo root):  python3 tools/build.py

Edit text in tools/content.py (posts, projects, log, plans). Edit case-study prose in tools/cases.py.
Output: index.html, work/, writing/, lab-log/, 404.html, sitemap.xml, robots.txt, favicon.svg
"""
import html, json, os, sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from content import *          # noqa
from cases import CASES        # noqa
from charts import *           # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAS_OG = os.path.exists(os.path.join(ROOT, "assets", "og.png"))
esc = html.escape


def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def fmt_date(iso, month_only=False):
    d = date.fromisoformat(iso)
    return d.strftime("%b %Y") if month_only else d.strftime("%d %b %Y").lstrip("0")


ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>'
OUT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'


# ------------------------------------------------------------------ shared chrome
BOOT = "<script>(function(d){d.classList.add('js');try{var m=matchMedia('(prefers-reduced-motion: reduce)').matches,x=sessionStorage.getItem('xnav');if(x&&!m){d.classList.add('is-entering');d.setAttribute('data-l',JSON.parse(x).l||'')}var t=localStorage.getItem('theme');if(t)d.setAttribute('data-theme',t)}catch(e){}})(document.documentElement)</script>"


def head(title, desc, path, kind="website", ld=None, noindex=False):
    assert len(title) <= 66, (len(title), title)
    assert 60 <= len(desc) <= 165, (len(desc), desc)
    url = SITE + path
    og = f'''<meta property="og:image" content="{SITE}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Anuj Nagar: data analysis and science writing">''' if HAS_OG else ""
    card = "summary_large_image" if HAS_OG else "summary"
    ldj = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>' if ld else ""
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#FF5A1F">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="en_IN">
{og}
<meta name="twitter:card" content="{card}"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}">
<link rel="me" href="{GITHUB}"><link rel="me" href="{LINKEDIN}"><link rel="me" href="{SUBSTACK}">
<link rel="alternate" type="application/rss+xml" title="UnFogIt" href="{SUBSTACK}feed">
{BOOT}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=JetBrains+Mono:wght@500&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
{ldj}
</head>
'''


def nav(active="", tone="ink", home=False):
    h = "" if home else "/"
    def a(href, label, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<a class="pill hide-mobile" href="{href}"{cur}>{label}</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-head" data-tone="{tone}" data-solid-after>
<div class="wrap">
<a class="brand" href="/">{NAME}<small>Data analysis &amp; science writing</small></a>
<nav class="nav" aria-label="Main">
{a("/work/", "Experiments", "work")}{a("/writing/", "Field notes", "writing")}{a("/lab-log/", "Lab log", "log")}
<a class="pill hide-mobile" href="{h}#contact" data-label="Contact">Get in touch {DOWN}</a>
<button class="pill theme-btn" id="theme-btn" type="button" aria-label="Switch between light and dark mode"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/></svg></button>
<button class="pill only-mobile" id="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
</nav>
</div>
</header>
<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menu">
<button class="pill pill--ghost close" type="button">Close</button>
<a href="/">Home</a><a href="/work/">Experiments</a><a href="/writing/">Field notes</a><a href="/lab-log/">Lab log</a><a href="{h}#contact">Contact</a>
</div>
'''


CURT = "<script>(function(){var s=document.querySelector('.curtain span'),l=document.documentElement.getAttribute('data-l');if(s&&l)s.textContent=l})()</script>"


def chrome_end(greet):
    return f'''<div class="guide" id="guide" data-greet="{esc(greet)}">
<canvas id="sig" width="48" height="48" aria-hidden="true"></canvas>
<div class="bubble" id="bubble" aria-hidden="true"></div>
</div>
<button class="guide-toggle" id="guide-toggle" type="button" aria-pressed="false" title="Hide the guide" aria-label="Show or hide the guide character">Sig</button>
<div class="curtain" aria-hidden="true"><i class="a"></i><i class="b"></i><span></span></div>
{CURT}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''


def footer():
    return f'''<footer class="foot">
<div class="wrap">
<p style="margin:0">&copy; 2026 {NAME}. Built by hand with HTML, CSS and a little JavaScript. No trackers, no cookies.</p>
<ul>
<li><a href="{GITHUB}" rel="me external">GitHub</a></li>
<li><a href="{LINKEDIN}" rel="me external">LinkedIn</a></li>
<li><a href="{SUBSTACK}" rel="me external">UnFogIt</a></li>
<li><a href="/lab-log/">Lab log</a></li>
</ul>
</div>
</footer>
'''


def contact(home=False):
    return f'''<section class="sec sec--accent contact" id="contact" data-says="Say hi. Copying the email is one click." aria-labelledby="contact-h">
<div class="wrap">
<p class="eyebrow mono">Contact</p>
<h2 id="contact-h">Got a messy dataset or a science question?</h2>
<p class="lede">I read everything and answer when I can. The quickest way is email, and LinkedIn works too.</p>
<div class="pills" style="margin-top:28px">
<span style="display:inline-flex;align-items:center;flex-wrap:wrap;gap:6px">
<a class="pill pill--lg" href="mailto:{EMAIL_U}@{EMAIL_D}" data-email data-u="{EMAIL_U}" data-d="{EMAIL_D}">Copy my email</a><span class="toast" role="status" aria-live="polite"></span>
</span>
<a class="pill pill--lg pill--ghost" href="{LINKEDIN}" rel="me external" target="_blank">LinkedIn {OUT}</a>
<a class="pill pill--lg pill--ghost" href="{GITHUB}" rel="me external" target="_blank">GitHub {OUT}</a>
<a class="pill pill--lg pill--ghost" href="{SUBSTACK}" rel="me external" target="_blank">UnFogIt {OUT}</a>
</div>
<noscript><p>Email: {EMAIL_U} [at] {EMAIL_D}</p></noscript>
</div>
</section>
'''


# ------------------------------------------------------------------ JSON-LD
PERSON = {"@type": "Person", "@id": SITE + "/#anuj", "name": NAME, "url": SITE + "/",
          "sameAs": [GITHUB, LINKEDIN, SUBSTACK],
          "description": "Data analyst who turns messy machine data into clear answers with Python, SQL and Power BI, and writes plain-language science explainers.",
          "knowsAbout": ["Data analysis", "Python", "pandas", "Time-series analysis", "Power BI", "Excel", "Sentiment analysis", "Test automation", "Science communication"]}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": NAME, "inLanguage": "en", "author": {"@id": SITE + "/#anuj"}}


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}


# ------------------------------------------------------------------ pieces reused on several pages
def chips_html():
    out = []
    for label, kind, url in CHIPS:
        if kind == "repo":
            out.append(f'<a class="chip" href="{url}" rel="external" target="_blank">{esc(label)} <small>repo</small></a>')
        else:
            out.append(f'<a class="chip" href="{url}">{esc(label)} <small>course</small></a>')
    return "".join(out)


def rows_html(skip_first=True):
    rows = []
    for p in PROJECTS[1:] if skip_first else PROJECTS:
        rows.append(f'''<a class="row" href="/work/{p["slug"]}/" data-label="{esc(p["title"])}">
<span class="n">{p["n"]}</span>
<span><h3>{esc(p["title"])}</h3><span class="b">{esc(p["short"])}</span></span>
<span class="t">{esc(" · ".join(p["tools"]))}<br>{esc(p["period"])}</span>
<span class="go" aria-hidden="true">&rarr;</span>
</a>''')
    return "\n".join(rows)


def split_title(t):
    if ": " in t:
        a, b = t.split(": ", 1)
        return a, b
    return t, ""


def notes_html(n=4):
    out = []
    for d, tag, t, slug in POSTS[:n]:
        a, b = split_title(t)
        out.append(f'''<a class="note" href="{SUBSTACK}p/{slug}" rel="external" target="_blank" data-reveal>
<span><span class="d" style="margin:0 0 14px"><span>{esc(tag)}</span><time datetime="{d}">{fmt_date(d)}</time></span><h3>{esc(a)}</h3><p>{esc(b)}</p></span>
<span class="d"><span>Read on UnFogIt</span><span aria-hidden="true">&nearr;</span></span>
</a>''')
    return "\n".join(out)


def log_html(entries, link_prefix=""):
    out = []
    for d, k, t, body, link in entries:
        when = fmt_date(d, d in MONTH_ONLY)
        more = f' <a href="{link}">See more &rarr;</a>' if link else ""
        out.append(f'''<li data-k="{k}" data-reveal><div class="when mono"><time datetime="{d}">{when}</time><span class="kind">{k}</span></div><h3>{esc(t)}</h3><p>{esc(body)}{more}</p></li>''')
    return "\n".join(out)


def bench_html():
    return "\n".join(f'<article class="card{" dashed" if s != "In progress" else ""}" data-reveal><span class="mono muted">{s}</span><h3 style="margin-top:.5em">{esc(t)}</h3><p>{esc(b)}</p></article>' for s, t, b in BENCH)


def sketches_html():
    cards = []
    for name, when, text, url in SKETCHES:
        cards.append(f'<article class="card dashed" data-reveal><span class="mono muted">{when}</span><h3 style="margin-top:.5em;font-size:1.35rem">{esc(name)}</h3><p>{esc(text)}</p><a href="{url}" rel="external" target="_blank">Open repo &nearr;</a></article>')
    for name, url in SKETCH_PAGES:
        cards.append(f'<article class="card dashed" data-reveal><span class="mono muted">Jul 2025 &middot; page</span><h3 style="margin-top:.5em;font-size:1.35rem">{esc(name)}</h3><p>An older standalone page from the first version of this site. Still online, still readable.</p><a href="{url}" rel="external">Open the page &rarr;</a></article>')
    return "\n".join(cards)


# ------------------------------------------------------------------ HOME
def home():
    p0 = PROJECTS[0]
    steps = [("Load", "Open multi-GB MF4 files lazily"), ("Segment", "Split into power-ups"), ("Measure", "Resets, gaps, first app update"),
             ("Correct", "Remove clock offset between paths"), ("Cross-check", "A second, offset-free method"), ("Judge", "OK, NOK, CHECK or INFO"), ("Report", "CSV plus browser dashboard")]
    pipe = "".join(f'<li><span class="mono">{i + 1:02d}</span><b>{a}</b><span>{b}</span></li>' for i, (a, b) in enumerate(steps))
    ld = {"@context": "https://schema.org", "@graph": [PERSON, WEBSITE, crumbs_ld([("Home", "/")])]}
    t = "Anuj Nagar | Data Analyst and Science Explainer"
    d = "Data analysis in Python, SQL and Power BI, plus plain-language science writing. Start with MF4 Log Analytics, which turns about 95 hours of log checking into 2.5."
    return head(t, d, "/", ld=ld) + f'''<body>
{nav("", "ink", home=True)}
<main id="main">

<section class="sec sec--accent hero" data-says="Hi, I’m <mark>Sig</mark>, the probe. Drag the slider, then scroll." aria-label="Introduction">
<div class="wrap">
<h1>I turn messy machine data into clear answers.</h1>
<p class="sub">Data analysis in Python, SQL and Power BI. And science explained in plain words, at UnFogIt.</p>
<div class="pills cta"><a class="pill pill--lg" href="#entry-01">See the flagship project {DOWN}</a><a class="pill pill--lg pill--ghost" href="/writing/">Read the field notes {ARROW}</a></div>
<div class="lab" id="lab" role="group" aria-labelledby="lab-h">
<header><p class="lab-title" id="lab-h">Signal lab</p><span class="tag mono">synthetic data</span></header>
<svg viewBox="0 0 320 130" role="img" aria-label="Two digital signals. Path A rises at zero milliseconds. Path B rises at a position you control with the slider.">
<g class="grid" stroke-width="1"><path d="M14 22v100M61 22v100M108 22v100M155 22v100M202 22v100M249 22v100M296 22v100"/></g>
<line x1="108" x2="108" y1="14" y2="122" stroke="#12151B" stroke-dasharray="3 3" opacity=".55"/>
<text x="112" y="22">A starts</text>
<path class="tr-a" d="M14,70 H108 V46 H306" fill="none" stroke-width="2.6"/>
<path class="tr-b" id="trb" d="M14,108 H155 V84 H306" fill="none" stroke-width="2.6"/>
<line id="dB" x1="155" x2="155" y1="60" y2="122" stroke="#FF5A1F" stroke-dasharray="3 3"/>
<text id="lblB" x="159" y="118">B starts</text>
<text x="16" y="62">PATH A</text><text x="16" y="100">PATH B</text>
</svg>
<label for="off">Remove clock offset <output id="off-v" for="off">0.0 ms</output></label>
<input id="off" type="range" min="0" max="3.2" step="0.1" value="0" aria-describedby="lab-msg">
<div class="readout"><span id="r1">Raw timestamps: B vs A +2.0 ms</span><span class="verdict ok" id="vd" role="status">OK</span><span id="r2">No offset removed yet</span></div>
<p class="lab-note" id="lab-msg" aria-live="polite">Looks fine: A seems to start first.</p>
<div class="row-btn"><button class="mini" id="est" type="button">Use the estimated 3.2 ms</button><button class="mini" id="rst" type="button">Reset</button></div>
<p class="lab-note">A replay of the demo recording in my MF4 project: the raw view hides a violation.</p>
</div>
</div>
</section>

<section class="sec sec--paper intro" data-says="That’s Anuj. Five years of chasing <mark>milliseconds</mark>." aria-label="About">
<div class="wrap">
<p class="eyebrow mono">About the notebook</p>
<p data-words>I’m Anuj. For five years I’ve checked whether automotive software behaves, chasing millisecond start-up bugs through gigabytes of measurement logs.</p>
<p data-words class="wide" style="margin-top:.8em">Now I’m turning that habit into data analysis, and I write UnFogIt, where research too dense for headlines gets explained in plain words.</p>
<div class="receipts" aria-label="Skills, each linked to the work that backs it">{chips_html()}</div>
<p class="muted" style="margin-top:14px;font-size:.95rem;max-width:60ch">Every skill links to the repo that shows it. If I can’t point at the work, it isn’t on this list.</p>
</div>
</section>

<section class="sec sec--navy" id="entry-01" data-says="The big one. <mark>95 hours</mark> of log-reading, estimated down to about 2.5." aria-labelledby="e1">
<div class="wrap entry">
<p class="num" aria-hidden="true">01</p>
<div class="head" data-reveal>
<p class="eyebrow mono">Experiment 01 &middot; flagship</p>
<h2 id="e1">{esc(p0["title"])}</h2>
<p class="lede">Two processors, two clocks, hundreds of power-ups. For every start-up in a multi-gigabyte recording, which one came first, by how many milliseconds, and why.</p>
</div>
<div class="stat" data-reveal>
<div class="big">95 h <span class="arrow" aria-hidden="true">&rarr;</span> 2.5 h</div>
<p><span class="sr">From about 95 hours to about 2.5 hours. </span>Estimated for a 10-recording campaign (about 585 start-ups). The tool time was measured once; the manual time is my estimate of 10 minutes per cycle.</p>
</div>
<div class="pipe" data-reveal><ol style="--n:7" aria-label="The seven steps of the pipeline">{pipe}</ol></div>
<div class="actions pills" data-reveal>
<a class="pill pill--lg" href="/work/mf4-log-analytics/" data-label="MF4 Log Analytics">Read the case study {ARROW}</a>
<a class="pill pill--lg pill--ghost" href="{p0["live"]}" rel="external" target="_blank">Open the live workflow {OUT}</a>
<a class="pill pill--lg pill--ghost" href="{p0["repo"]}" rel="external" target="_blank">Source on GitHub {OUT}</a>
</div>
</div>
</section>

<section class="sec sec--paper" data-says="Five more experiments. Each one says what went wrong, too." aria-labelledby="work-h">
<div class="wrap">
<div class="list-head"><div><p class="eyebrow mono">More experiments</p><h2 id="work-h">The rest of the bench</h2></div>
<a class="pill" href="/work/">All experiments {ARROW}</a></div>
<div class="rows" data-reveal>
{rows_html()}
</div>
</div>
</section>

<section class="sec sec--navy" data-says="He also explains <mark>science</mark> without a decoder ring." aria-labelledby="writing-h">
<div class="wrap">
<div class="list-head"><div><p class="eyebrow mono">Field notes &middot; UnFogIt</p><h2 id="writing-h">Wait, what?</h2>
<p class="lede" style="margin-top:1em">UnFogIt breaks down the AI, science and tech research too dense for headlines.</p></div>
<a class="pill" href="/writing/">All {len(POSTS)} notes {ARROW}</a></div>
<div class="notes">
{notes_html(4)}
</div>
</div>
</section>

<section class="sec sec--sheet sec--paper" data-says="A lab log keeps the dates honest." aria-labelledby="log-h">
<div class="wrap">
<div class="list-head"><div><p class="eyebrow mono">Lab log</p><h2 id="log-h">What I learned, and when</h2></div>
<a class="pill" href="/lab-log/">Full log {ARROW}</a></div>
<ol class="log">
{log_html(LOG[:6])}
</ol>
</div>
</section>

<section class="sec sec--paper" data-says="Plans, not promises. I like that." aria-labelledby="bench-h">
<div class="wrap">
<p class="eyebrow mono">On the bench</p>
<h2 id="bench-h" style="margin-bottom:.5em">What I’m building next</h2>
<div class="bench">
{bench_html()}
</div>
<p class="muted" style="margin-top:22px;font-size:.95rem">Plans, not promises. Dashed cards are ideas; the solid one is already under way.</p>
</div>
</section>

{contact(True)}
</main>
{footer()}
''' + chrome_end("Hi, I’m <mark>Sig</mark>, the probe. Drag the slider, then scroll.")


# ------------------------------------------------------------------ WORK index
def work_index():
    t = "Experiments: Data Analysis Projects by Anuj Nagar"
    d = "Six data analysis experiments in Python, Power BI, Excel and pytest, each with the question, the method, the result and the caveat. Plus a shelf of early sketches."
    items = [{"@type": "ListItem", "position": i + 1, "url": f'{SITE}/work/{p["slug"]}/', "name": p["title"]} for i, p in enumerate(PROJECTS)]
    ld = {"@context": "https://schema.org", "@graph": [PERSON, WEBSITE, crumbs_ld([("Home", "/"), ("Experiments", "/work/")]),
          {"@type": "CollectionPage", "name": t, "url": SITE + "/work/", "mainEntity": {"@type": "ItemList", "itemListElement": items}}]}
    return head(t, d, "/work/", ld=ld) + f'''<body>
{nav("work", "light")}
<main id="main">
<section class="sec sec--navy case-hero" data-says="Six entries. Every one has a <mark>caveat</mark> section." aria-labelledby="h1">
<div class="wrap">
<nav class="crumbs mono" aria-label="Breadcrumb"><a href="/">Home</a> / Experiments</nav>
<h1 id="h1">All experiments</h1>
<p class="lede">Each entry follows the same four beats: the question, the method, the result, and the caveat. The caveat is the part most portfolios leave out.</p>
</div>
</section>
<section class="sec sec--paper" aria-label="Experiments">
<div class="wrap"><h2 class="sr">The six experiments</h2><div class="rows">
{rows_html(skip_first=False)}
</div></div>
</section>
<section class="sec sec--sheet sec--paper" id="sketches" data-says="The sketches shelf. Honest about what’s finished." aria-labelledby="sk-h">
<div class="wrap">
<p class="eyebrow mono">Sketches shelf</p>
<h2 id="sk-h" style="margin-bottom:.4em">Where it started</h2>
<p class="lede" style="margin-bottom:1.6em">Early experiments from July 2025. Some are working demos, some are little more than a README. I keep them because they show where I began, and I label them for what they are.</p>
<div class="bench" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr))">
{sketches_html()}
</div>
</div>
</section>
{contact()}
</main>
{footer()}
''' + chrome_end("Six entries. Every one has a <mark>caveat</mark> section.")


# ------------------------------------------------------------------ CASE pages
def case_page(i):
    p = PROJECTS[i]
    c = CASES[p["slug"]]
    prev_p = PROJECTS[i - 1] if i > 0 else PROJECTS[-1]
    next_p = PROJECTS[i + 1] if i < len(PROJECTS) - 1 else PROJECTS[0]
    path = f'/work/{p["slug"]}/'
    is_code = p["slug"] in ("mf4-log-analytics", "python-test-automation", "dsa-learning")
    work = {"@type": "SoftwareSourceCode" if is_code else "CreativeWork", "@id": SITE + path + "#work", "name": p["title"], "url": SITE + path,
            "description": p["meta_desc"], "author": {"@id": SITE + "/#anuj"}, "dateModified": UPDATED, "inLanguage": "en",
            "sameAs": [p["repo"]]}
    if is_code:
        work["codeRepository"] = p["repo"]
        work["programmingLanguage"] = "Python"
    ld = {"@context": "https://schema.org", "@graph": [PERSON, WEBSITE, work, crumbs_ld([("Home", "/"), ("Experiments", "/work/"), (p["title"], path)])]}
    facts = "".join(f'<div><dt class="mono">{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in p["facts"])
    live = f'<a class="pill pill--lg" href="{p["live"]}" rel="external" target="_blank">{esc(c.get("live_label", "Open the live demo"))} {OUT}</a>' if p["live"] else ""
    beats = ""
    for letter, label, heading, body in c["beats"]:
        beats += f'''<section class="beat" aria-labelledby="b-{letter}" data-reveal><div class="k"><b aria-hidden="true">{letter}</b><span class="mono">{label}</span></div><div class="c"><h2 id="b-{letter}">{heading}</h2>{body}</div></section>\n'''
    return head(p["meta_title"] + " | " + NAME if len(p["meta_title"]) + len(NAME) + 3 <= 66 else p["meta_title"], p["meta_desc"], path, kind="article", ld=ld) + f'''<body>
{nav("work", "light")}
<main id="main">
<section class="sec sec--navy case-hero" data-says="{esc(c["says"])}" aria-labelledby="h1">
<div class="wrap">
<nav class="crumbs mono" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/work/">Experiments</a> / {p["n"]}</nav>
<p class="eyebrow mono">Experiment {p["n"]}{" &middot; flagship" if i == 0 else ""}</p>
<h1 id="h1">{esc(p["title"])}</h1>
<p class="lede">{c["lede"]}</p>
<div class="pills" style="margin-top:28px">{live}
<a class="pill pill--lg pill--ghost" href="{p["repo"]}" rel="external" target="_blank">Source on GitHub {OUT}</a></div>
<dl class="facts">{facts}</dl>
</div>
</section>
<section class="sec sec--paper" aria-label="Case study">
<div class="wrap">
<div class="beats">
{beats}
</div>
<nav class="next-prev" aria-label="More experiments">
<a href="/work/{prev_p["slug"]}/" data-label="{esc(prev_p["title"])}"><span class="mono muted">&larr; Previous</span><b>{esc(prev_p["title"])}</b></a>
<a href="/work/{next_p["slug"]}/" data-label="{esc(next_p["title"])}"><span class="mono muted">Next &rarr;</span><b>{esc(next_p["title"])}</b></a>
</nav>
</div>
</section>
{contact()}
</main>
{footer()}
''' + chrome_end(c["says"])


# ------------------------------------------------------------------ WRITING
def writing():
    t = "Field Notes: Science Explained Plainly (UnFogIt)"
    d = "Plain-language explainers on AI, space, biology, quantum computing and psychology research, written by Anuj Nagar for UnFogIt on Substack."
    posts_ld = [{"@type": "BlogPosting", "headline": split_title(tt)[0] + (": " + split_title(tt)[1] if split_title(tt)[1] else ""),
                 "url": f"{SUBSTACK}p/{slug}", "datePublished": dd, "author": {"@id": SITE + "/#anuj"}} for dd, tag, tt, slug in POSTS]
    ld = {"@context": "https://schema.org", "@graph": [PERSON, WEBSITE, crumbs_ld([("Home", "/"), ("Field notes", "/writing/")]),
          {"@type": "Blog", "name": "UnFogIt", "url": SUBSTACK, "description": "Breaking down the AI, science and tech research too dense for headlines.", "author": {"@id": SITE + "/#anuj"}, "blogPost": posts_ld}]}
    lis = []
    for dd, tag, tt, slug in POSTS:
        a, b = split_title(tt)
        lis.append(f'''<li><a href="{SUBSTACK}p/{slug}" rel="external" target="_blank"><span class="d mono muted"><time datetime="{dd}">{fmt_date(dd)}</time><br>{esc(tag)}</span><span><h3>{esc(a)}</h3><p>{esc(b)}</p></span><span aria-hidden="true">&nearr;</span></a></li>''')
    return head(t, d, "/writing/", ld=ld) + f'''<body>
{nav("writing", "ink")}
<main id="main">
<section class="sec sec--accent case-hero" data-says="Wait, what? That’s the whole <mark>idea</mark>." aria-labelledby="h1">
<div class="wrap">
<nav class="crumbs mono" aria-label="Breadcrumb"><a href="/">Home</a> / Field notes</nav>
<h1 id="h1">Wait, what?</h1>
<p class="lede">UnFogIt breaks down the AI, science and tech research too dense for headlines. Each note takes one paper and says what it found, in words you don’t need a degree for.</p>
<div class="pills" style="margin-top:28px"><a class="pill pill--lg" href="{SUBSTACK}" rel="external" target="_blank">Subscribe on Substack {OUT}</a></div>
</div>
</section>
<section class="sec sec--paper" aria-label="All field notes">
<div class="wrap">
<h2 class="sr">All field notes</h2>
<p class="eyebrow mono" aria-hidden="true">{len(POSTS)} most recent notes</p>
<ul class="post-list">
{chr(10).join(lis)}
</ul>
<p class="muted" style="margin-top:28px">The full archive lives on <a href="{SUBSTACK}archive" rel="external" target="_blank">Substack</a>.</p>
</div>
</section>
{contact()}
</main>
{footer()}
''' + chrome_end("Wait, what? That’s the whole <mark>idea</mark>.")


# ------------------------------------------------------------------ LAB LOG
def lab_log():
    t = "Lab Log: What Anuj Nagar Learned and Built, by Date"
    d = "A dated log of what I learned and built: Python, SQL, Excel, Power BI and Tableau courses, data analysis projects, and writing, newest first."
    ld = {"@context": "https://schema.org", "@graph": [PERSON, WEBSITE, crumbs_ld([("Home", "/"), ("Lab log", "/lab-log/")])]}
    return head(t, d, "/lab-log/", ld=ld) + f'''<body>
{nav("log", "light")}
<main id="main">
<section class="sec sec--navy case-hero" data-says="A lab log is a diary for <mark>experiments</mark>." aria-labelledby="h1">
<div class="wrap">
<nav class="crumbs mono" aria-label="Breadcrumb"><a href="/">Home</a> / Lab log</nav>
<h1 id="h1">The lab log</h1>
<p class="lede">Scientists keep a lab log: dated, short, honest entries about what they tried, what happened and what they learned. This is mine. It includes the courses I’ve finished, because learning is part of the work.</p>
</div>
</section>
<section class="sec sec--paper" aria-label="Log entries">
<div class="wrap">
<div class="legend mono" aria-hidden="true"><span><i style="background:var(--accent)"></i>built</span><span><i style="background:var(--sky)"></i>learned</span><span><i style="background:var(--phos)"></i>wrote</span><span><i style="border-style:dashed"></i>next</span></div>
<h2 class="sr">Log entries, newest first</h2>
<ol class="log">
<li data-k="next" data-reveal><div class="when mono"><time datetime="2026-10">Now</time><span class="kind">next</span></div><h3>Crio.Do DA-201 (data analytics) in progress</h3><p>The capstone comes after the coursework. It will become entry 07 on this site.</p></li>
{log_html(LOG)}
</ol>
<p class="muted" style="margin-top:34px;font-size:.95rem">Course dates are shown by month. Certificates are on <a href="{LINKEDIN}" rel="me external" target="_blank">LinkedIn</a>.</p>
</div>
</section>
<section class="sec sec--sheet sec--paper" data-says="Plans, not promises." aria-labelledby="bench-h">
<div class="wrap">
<p class="eyebrow mono">On the bench</p>
<h2 id="bench-h" style="margin-bottom:.5em">What’s next</h2>
<div class="bench">{bench_html()}</div>
</div>
</section>
{contact()}
</main>
{footer()}
''' + chrome_end("A lab log is a diary for <mark>experiments</mark>.")


# ------------------------------------------------------------------ 404
def not_found():
    return head("Signal lost | Anuj Nagar", "That page doesn’t exist, but the experiments, field notes and lab log are all one click away. Head back to the home page.", "/404.html", noindex=True) + f'''<body>
{nav("", "ink")}
<main id="main">
<section class="sec sec--accent lost" data-says="No signal here. Try the <mark>home</mark> page?">
<div class="wrap">
<p class="eyebrow mono">Error 404</p>
<h1>Signal lost.</h1>
<p class="lede" style="margin-top:1em">That page isn’t here. It may have moved, or the link had a typo.</p>
<div class="pills" style="margin-top:28px"><a class="pill pill--lg" href="/">Back to the start {ARROW}</a><a class="pill pill--lg pill--ghost" href="/work/">Experiments</a><a class="pill pill--lg pill--ghost" href="/writing/">Field notes</a></div>
</div>
</section>
</main>
{footer()}
''' + chrome_end("No signal here. Try the <mark>home</mark> page?")


# ------------------------------------------------------------------ run
def main():
    write("index.html", home())
    write("work/index.html", work_index())
    for i, p in enumerate(PROJECTS):
        write(f'work/{p["slug"]}/index.html', case_page(i))
    write("writing/index.html", writing())
    write("lab-log/index.html", lab_log())
    write("404.html", not_found())
    urls = ["/", "/work/"] + [f'/work/{p["slug"]}/' for p in PROJECTS] + ["/writing/", "/lab-log/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f'  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED}</lastmod></url>\n' for u in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write(".nojekyll", "")
    write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#FF5A1F"/><path d="M8 40h14V22h12v22h8V30h14" fill="none" stroke="#12151B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>\n')
    print("built", len(urls), "pages; og image:", HAS_OG)


if __name__ == "__main__":
    main()
