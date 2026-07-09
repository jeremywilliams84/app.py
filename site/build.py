# -*- coding: utf-8 -*-
"""Générateur du site Localto — design premium, contenus persona, SEO.

Usage :  python3 site/build.py   (écrit le site final dans ./dist)
"""
import json
import shutil
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "dist"
DATA = json.loads((ROOT / "data.json").read_text())
SITE = C.SITE
URL = SITE["url"]


def de_pluriel(m):
    p = C.METIERS[m]["pluriel"]
    return ("d'" + p) if p[0].lower() in "aeéiouh" else ("de " + p)


# ---------------------------------------------------------------------------
# Icônes SVG (style trait, 24x24)
# ---------------------------------------------------------------------------

_I = {
    "wrench": '<path d="M14.7 6.3a4.5 4.5 0 0 0-6 5.6L3 17.6a2 2 0 1 0 2.8 2.8l5.7-5.7a4.5 4.5 0 0 0 5.6-6l-3 3-2.8-.7-.7-2.8 3.1-2.9z"/>',
    "bolt": '<path d="M13 2 4.5 13.5H11L10 22l8.5-11.5H12L13 2z"/>',
    "scissors": '<circle cx="6" cy="6" r="2.6"/><circle cx="6" cy="18" r="2.6"/><path d="M8.2 7.6 20 19M8.2 16.4 20 5M14.7 14.7l-2.2-2.2"/>',
    "scale": '<path d="M12 3v18M8 21h8M12 5l-6 2m6-2 6 2M6 7l-3 6a3.5 3.5 0 0 0 6 0L6 7zm12 0-3 6a3.5 3.5 0 0 0 6 0l-3-6z"/>',
    "compass": '<circle cx="12" cy="5" r="1.8"/><path d="M11 6.6 5.5 20M13 6.6 18.5 20M7.3 15.5a8 8 0 0 0 9.4 0"/>',
    "calculator": '<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 7.5h7M8.5 12h.01M12 12h.01M15.5 12h.01M8.5 15.5h.01M12 15.5h.01M15.5 15.5v.01"/>',
    "hand": '<path d="M12 20.5s-7-4.4-7-9.3A3.9 3.9 0 0 1 12 8.6a3.9 3.9 0 0 1 7 2.6c0 4.9-7 9.3-7 9.3z"/><path d="M8.6 11.9h2l1-1.6 1.4 2.8 1-1.2h1.6"/>',
    "dumbbell": '<path d="M7.5 9v6M4.5 10v4M19.5 10v4M16.5 9v6M7.5 12h9M2.5 12h2M19.5 12h2"/>',
    "camera": '<path d="M4 8.5A2.5 2.5 0 0 1 6.5 6h1l1.4-2h6.2L16.5 6h1A2.5 2.5 0 0 1 20 8.5v8a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 4 16.5v-8z"/><circle cx="12" cy="12.5" r="3.4"/>',
    "layout": '<rect x="3.5" y="4" width="17" height="16" rx="2.5"/><path d="M3.5 9.5h17M9.5 9.5V20"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.4-4.4"/>',
    "shield": '<path d="M12 3 5 5.8v5.4c0 4.3 3 7.7 7 9.8 4-2.1 7-5.5 7-9.8V5.8L12 3z"/><path d="m9.2 11.8 2 2 3.6-3.9"/>',
    "calendar": '<rect x="4" y="5.5" width="16" height="15" rx="2.5"/><path d="M8 3.5v4M16 3.5v4M4 10.5h16M9 15l2 2 4-4.5"/>',
    "pin": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "x": '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
    "key": '<circle cx="8" cy="15.5" r="4"/><path d="m11 12.5 8.5-8.5M16 7.5l3 3M13.5 10l2 2"/>',
    "bulb": '<path d="M9.5 18a6.5 6.5 0 1 1 5 0v1.5a1.5 1.5 0 0 1-1.5 1.5h-2a1.5 1.5 0 0 1-1.5-1.5V18z"/><path d="M9.5 21.5h5"/>',
    "arrow": '<path d="M4.5 12h14M13 6.5l5.5 5.5L13 17.5"/>',
    "star": '<path d="m12 3.5 2.5 5.2 5.7.8-4.1 4 1 5.7L12 16.5l-5.1 2.7 1-5.7-4.1-4 5.7-.8L12 3.5z"/>',
    "chevron": '<path d="m7 10 5 5 5-5"/>',
    "quote": '<path d="M7.5 5.5C5 7 3.5 9.5 3.5 13v5.5H9V13H5.8c0-2.4 1.2-4.3 3.2-5.5L7.5 5.5zm10 0C15 7 13.5 9.5 13.5 13v5.5H19V13h-3.2c0-2.4 1.2-4.3 3.2-5.5l-1.5-2z"/>',
}


def icon(name, cls="ic"):
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{_I[name]}</svg>'
    )


# ---------------------------------------------------------------------------
# Illustration héro (scène recherche locale)
# ---------------------------------------------------------------------------

def hero_art():
    return """
<div class="hero-art" aria-hidden="true">
  <svg viewBox="0 0 560 470" fill="none" xmlns="http://www.w3.org/2000/svg" role="img">
    <defs>
      <linearGradient id="gBrand" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#1a8a5c"/><stop offset="1" stop-color="#0e5638"/>
      </linearGradient>
      <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
        <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#0c1f16" flood-opacity="0.13"/>
      </filter>
    </defs>
    <!-- carte / plan de ville -->
    <g class="float-slow" filter="url(#soft)">
      <rect x="200" y="30" width="330" height="270" rx="20" fill="#ffffff"/>
      <rect x="200" y="30" width="330" height="270" rx="20" fill="#eaf4ec"/>
      <path d="M200 120 H530 M200 210 H530 M290 30 V300 M400 30 V300 M470 30 V300" stroke="#ffffff" stroke-width="14"/>
      <path d="M200 120 H530 M200 210 H530 M290 30 V300 M400 30 V300 M470 30 V300" stroke="#d4e6d8" stroke-width="2"/>
      <circle cx="345" cy="165" r="34" fill="#e4572e" opacity="0.14"/>
      <circle cx="345" cy="165" r="18" fill="#e4572e" opacity="0.22"/>
      <g transform="translate(345 150)">
        <path d="M0 32C0 32 -16 17 -16 4a16 16 0 1 1 32 0C16 17 0 32 0 32z" fill="#e4572e"/>
        <circle cx="0" cy="4" r="6" fill="#fff"/>
      </g>
      <g fill="#15714b">
        <circle cx="255" cy="80" r="7"/><circle cx="465" cy="95" r="7"/><circle cx="430" cy="255" r="7"/>
      </g>
    </g>
    <!-- carte résultat de recherche -->
    <g class="float" filter="url(#soft)">
      <rect x="30" y="120" width="300" height="300" rx="20" fill="#fff"/>
      <rect x="52" y="146" width="256" height="44" rx="12" fill="#f2f7f1" stroke="#dfeade"/>
      <circle cx="76" cy="168" r="8" stroke="#54655c" stroke-width="2.4" fill="none"/>
      <path d="m82 174 6 6" stroke="#54655c" stroke-width="2.4" stroke-linecap="round"/>
      <rect x="98" y="161" width="150" height="14" rx="7" fill="#0c1f16" opacity="0.82"/>
      <rect x="52" y="214" width="256" height="56" rx="12" fill="url(#gBrand)"/>
      <rect x="68" y="230" width="120" height="11" rx="5.5" fill="#fff" opacity="0.95"/>
      <rect x="68" y="248" width="80" height="8" rx="4" fill="#fff" opacity="0.55"/>
      <g transform="translate(258 230)" fill="#f7c948">
        <path d="m8 0 2.2 4.6 5 .7-3.6 3.5.9 5L8 11.4 3.5 13.8l.9-5L.8 5.3l5-.7L8 0z"/>
      </g>
      <rect x="52" y="282" width="256" height="46" rx="12" fill="#f7faf6" stroke="#e2eae0"/>
      <rect x="68" y="295" width="132" height="10" rx="5" fill="#54655c" opacity="0.6"/>
      <rect x="68" y="311" width="90" height="7" rx="3.5" fill="#54655c" opacity="0.3"/>
      <rect x="52" y="340" width="256" height="46" rx="12" fill="#f7faf6" stroke="#e2eae0"/>
      <rect x="68" y="353" width="150" height="10" rx="5" fill="#54655c" opacity="0.6"/>
      <rect x="68" y="369" width="70" height="7" rx="3.5" fill="#54655c" opacity="0.3"/>
    </g>
    <!-- badge avis -->
    <g class="float-rev" filter="url(#soft)">
      <rect x="330" y="330" width="196" height="72" rx="18" fill="#fff"/>
      <circle cx="366" cy="366" r="18" fill="#e3f2e9"/>
      <path d="m358.5 366 5 5 10-11" stroke="#15714b" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <text x="394" y="361" font-family="system-ui,sans-serif" font-size="15" font-weight="800" fill="#0c1f16">4,9 / 5</text>
      <text x="394" y="381" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#54655c">127 avis clients</text>
    </g>
  </svg>
</div>"""


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """
/* Localto — design system */
:root{
  --bg:#f6f9f4; --surface:#ffffff; --ink:#0c1f16; --muted:#54655c;
  --line:#e2eae0; --brand:#15714b; --brand-deep:#0e5638; --brand-soft:#e3f2e9;
  --accent:#e4572e; --accent-soft:#fbe9e2; --gold:#e9a13b; --dark:#0a1b13;
  --r:18px; --r-sm:12px;
  --shadow-1:0 1px 2px rgba(12,31,22,.05),0 4px 14px rgba(12,31,22,.06);
  --shadow-2:0 2px 4px rgba(12,31,22,.06),0 18px 40px rgba(12,31,22,.12);
  --font-display:"Fraunces",Georgia,serif;
  --font-body:"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{
  margin:0;background:var(--bg);color:var(--ink);
  font-family:var(--font-body);font-size:1.04rem;line-height:1.75;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
}
img,svg{max-width:100%;height:auto}
a{color:inherit}
.container{max-width:1140px;margin-inline:auto;padding-inline:24px}
.narrow{max-width:820px}

h1,h2,h3,.display{font-family:var(--font-display);font-weight:600;line-height:1.14;letter-spacing:-.01em;margin:0}
h1{font-size:clamp(2.3rem,4.6vw,3.7rem)}
h2{font-size:clamp(1.7rem,3vw,2.4rem)}
h3{font-size:1.22rem;line-height:1.35}
p{margin:0}
.lead{font-size:clamp(1.05rem,1.6vw,1.22rem);line-height:1.75;color:var(--muted)}
strong{color:var(--ink)}
.link{color:var(--brand);font-weight:700;text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:3px}
.link:hover{color:var(--brand-deep)}

.eyebrow{
  display:inline-flex;align-items:center;gap:.5rem;
  font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);margin-bottom:14px;
}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--accent);border-radius:2px}

.ic{width:22px;height:22px;flex:none}

/* ---------- header ---------- */
.header{
  position:sticky;top:0;z-index:50;
  background:rgba(246,249,244,.82);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  border-bottom:1px solid transparent;transition:border-color .3s,box-shadow .3s;
}
.header.scrolled{border-color:var(--line);box-shadow:0 6px 24px rgba(12,31,22,.06)}
.header .container{display:flex;align-items:center;justify-content:space-between;gap:20px;padding-block:14px}
.logo{display:flex;align-items:center;gap:11px;font-weight:800;font-size:1.22rem;text-decoration:none;letter-spacing:-.02em}
.logo-mark{
  display:grid;place-items:center;width:38px;height:38px;border-radius:11px;color:#fff;
  background:linear-gradient(135deg,#1a8a5c,var(--brand-deep));
  box-shadow:0 4px 12px rgba(21,113,75,.35);font-family:var(--font-display);font-size:1.15rem;
}
.nav{display:flex;align-items:center;gap:26px}
.nav a{font-size:.92rem;font-weight:700;color:var(--muted);text-decoration:none;transition:color .2s}
.nav a:hover,.nav a[aria-current]{color:var(--brand)}
.nav a.btn,.nav a.btn:hover{color:#fff}
.nav .btn{padding:.62rem 1.1rem;font-size:.88rem}
@media (max-width:880px){.nav a:not(.btn){display:none}}

/* ---------- boutons ---------- */
.btn{
  display:inline-flex;align-items:center;gap:.55rem;
  padding:.85rem 1.5rem;border-radius:999px;border:0;cursor:pointer;
  font-family:var(--font-body);font-weight:800;font-size:.98rem;text-decoration:none;
  background:linear-gradient(135deg,#1a8a5c,var(--brand-deep));color:#fff;
  box-shadow:0 6px 18px rgba(21,113,75,.32);
  transition:transform .2s,box-shadow .2s,filter .2s;
}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(21,113,75,.4);filter:brightness(1.05)}
.btn .ic{width:18px;height:18px}
.btn-ghost{
  background:var(--surface);color:var(--brand);box-shadow:none;
  border:1.5px solid var(--brand);
}
.btn-ghost:hover{box-shadow:0 8px 20px rgba(21,113,75,.15);filter:none;background:var(--brand-soft)}
.btn-light{background:#fff;color:var(--brand-deep);box-shadow:0 6px 18px rgba(0,0,0,.25)}
.btn-light:hover{filter:none}

/* ---------- héros ---------- */
.hero{
  position:relative;overflow:hidden;
  background:
    radial-gradient(900px 480px at 85% -10%, rgba(21,113,75,.14), transparent 62%),
    radial-gradient(700px 420px at -8% 108%, rgba(228,87,46,.10), transparent 60%),
    linear-gradient(180deg,#f2f8f0,var(--bg));
  border-bottom:1px solid var(--line);
}
.hero::before{
  content:"";position:absolute;inset:0;pointer-events:none;opacity:.5;
  background-image:radial-gradient(rgba(21,113,75,.13) 1.3px, transparent 1.3px);
  background-size:26px 26px;
  mask-image:linear-gradient(180deg,#000 0%,transparent 68%);
  -webkit-mask-image:linear-gradient(180deg,#000 0%,transparent 68%);
}
.hero-grid{
  position:relative;display:grid;gap:48px;align-items:center;
  grid-template-columns:1.05fr .95fr;padding-block:84px 92px;
}
@media (max-width:960px){.hero-grid{grid-template-columns:1fr;padding-block:60px}}
.hero .badge{
  display:inline-flex;align-items:center;gap:.5rem;padding:.45rem 1rem;border-radius:999px;
  background:var(--surface);border:1px solid var(--line);box-shadow:var(--shadow-1);
  font-size:.82rem;font-weight:800;color:var(--brand);
}
.hero .badge .ic{width:15px;height:15px;color:var(--accent)}
.hero h1{margin-top:22px}
.hero h1 .accent{color:var(--brand);font-style:italic}
.hero .lead{margin-top:22px;max-width:34em}
.hero-cta{display:flex;flex-wrap:wrap;gap:14px;margin-top:32px}
.hero-points{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:34px;padding:0;list-style:none}
.hero-points li{display:flex;align-items:center;gap:.5rem;font-size:.9rem;font-weight:700;color:var(--muted)}
.hero-points .ic{width:17px;height:17px;color:var(--brand)}
.hero-art svg{display:block;width:100%}

/* héro pages internes */
.hero-page .hero-grid{grid-template-columns:1fr auto;padding-block:56px 64px}
@media (max-width:820px){.hero-page .hero-grid{grid-template-columns:1fr}}
.hero-emblem{
  position:relative;display:grid;place-items:center;width:190px;height:190px;margin-inline:auto;
}
.hero-emblem .ring{position:absolute;inset:0;border-radius:50%;border:2px dashed rgba(21,113,75,.35);animation:spin 40s linear infinite}
.hero-emblem .disc{
  display:grid;place-items:center;width:132px;height:132px;border-radius:38px;
  background:linear-gradient(135deg,#1a8a5c,var(--brand-deep));color:#fff;
  box-shadow:0 18px 40px rgba(21,113,75,.35);transform:rotate(-6deg);
}
.hero-emblem .disc .ic{width:58px;height:58px;stroke-width:1.5}
.hero-emblem .dot{position:absolute;width:14px;height:14px;border-radius:50%;background:var(--accent);top:12px;right:26px;box-shadow:0 4px 10px rgba(228,87,46,.45)}
@keyframes spin{to{transform:rotate(360deg)}}
@media (max-width:820px){.hero-emblem{display:none}}

/* flottements illustration */
.float{animation:float 7s ease-in-out infinite}
.float-rev{animation:float 6s ease-in-out infinite reverse}
.float-slow{animation:float 9s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@media (prefers-reduced-motion:reduce){.float,.float-rev,.float-slow,.hero-emblem .ring{animation:none}}

/* ---------- fil d'ariane / sommaire ---------- */
.crumbs{padding-top:22px;font-size:.86rem;color:var(--muted)}
.crumbs ol{display:flex;flex-wrap:wrap;gap:.55rem;list-style:none;margin:0;padding:0}
.crumbs a{color:var(--muted);text-decoration:none;font-weight:600}
.crumbs a:hover{color:var(--brand)}
.crumbs li+li::before{content:"›";margin-right:.55rem;color:#a9b8ac}
.crumbs [aria-current]{font-weight:800;color:var(--ink)}
.toc{display:flex;flex-wrap:wrap;gap:9px;margin-top:34px}
.toc a{
  padding:.42rem .95rem;border-radius:999px;font-size:.83rem;font-weight:700;text-decoration:none;
  background:var(--surface);border:1px solid var(--line);color:var(--muted);transition:.2s;
}
.toc a:hover{border-color:var(--brand);color:var(--brand)}

/* ---------- sections ---------- */
.section{padding-block:76px}
.section--alt{background:var(--surface);border-block:1px solid var(--line)}
.section-head{max-width:760px;margin-bottom:40px}
.section-head .lead{margin-top:16px}
.grid{display:grid;gap:20px}
.cols-2{grid-template-columns:repeat(2,1fr)}
.cols-3{grid-template-columns:repeat(3,1fr)}
.cols-4{grid-template-columns:repeat(4,1fr)}
@media (max-width:960px){.cols-3,.cols-4{grid-template-columns:repeat(2,1fr)}}
@media (max-width:640px){.cols-2,.cols-3,.cols-4{grid-template-columns:1fr}}

.card{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
  padding:26px;box-shadow:var(--shadow-1);
  transition:transform .25s,box-shadow .25s,border-color .25s;
}
a.card{text-decoration:none;display:block}
.card:hover{transform:translateY(-4px);box-shadow:var(--shadow-2);border-color:#cfe0d2}
.card h3{margin-bottom:10px}
.card p{color:var(--muted);font-size:.95rem;line-height:1.65}

.icon-tile{
  display:grid;place-items:center;width:52px;height:52px;border-radius:16px;margin-bottom:18px;
  background:var(--brand-soft);color:var(--brand);
}
.icon-tile .ic{width:26px;height:26px}
.card:hover .icon-tile{background:linear-gradient(135deg,#1a8a5c,var(--brand-deep));color:#fff}
.icon-tile,.card .icon-tile{transition:background .25s,color .25s}

/* carte métier */
.metier-card .cat{font-size:.74rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.metier-card h3{margin:6px 0 10px}
.metier-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.metier-links a{
  display:inline-flex;align-items:center;gap:.4rem;
  font-size:.84rem;font-weight:800;color:var(--brand);text-decoration:none;
  padding:.4rem .85rem;border-radius:999px;background:var(--brand-soft);transition:.2s;
}
.metier-links a:hover{background:var(--brand);color:#fff}
.metier-links .ic{width:14px;height:14px}

/* listes stylées */
.list{display:grid;gap:12px;padding:0;margin:0;list-style:none}
.list li{
  display:flex;gap:14px;align-items:flex-start;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);
  padding:15px 18px;font-weight:600;box-shadow:var(--shadow-1);
}
.list .ic{width:21px;height:21px;margin-top:3px}
.list-check .ic{color:var(--brand)}
.list-x .ic{color:var(--accent)}
.list-x li{background:#fffaf8;border-color:#f4ddd3}

/* étapes numérotées */
.steps{counter-reset:s;display:grid;gap:14px;padding:0;margin:0;list-style:none}
.steps li{
  counter-increment:s;position:relative;display:flex;gap:18px;align-items:flex-start;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);
  padding:17px 20px;font-weight:600;box-shadow:var(--shadow-1);
}
.steps li::before{
  content:counter(s);flex:none;display:grid;place-items:center;width:34px;height:34px;
  border-radius:11px;font-size:.95rem;font-weight:800;color:#fff;
  background:linear-gradient(135deg,#1a8a5c,var(--brand-deep));
  box-shadow:0 4px 10px rgba(21,113,75,.3);
}

/* timeline plan 7 jours */
.timeline{position:relative;display:grid;gap:0;padding:0;margin:0;list-style:none;counter-reset:d}
.timeline li{
  counter-increment:d;position:relative;padding:0 0 26px 66px;font-weight:600;
}
.timeline li::before{
  content:"J" counter(d);position:absolute;left:0;top:-4px;
  display:grid;place-items:center;width:44px;height:44px;border-radius:14px;
  font-size:.9rem;font-weight:800;color:#fff;
  background:linear-gradient(135deg,var(--accent),#c53d18);
  box-shadow:0 6px 14px rgba(228,87,46,.35);
}
.timeline li::after{
  content:"";position:absolute;left:21px;top:44px;bottom:2px;width:2px;
  background:linear-gradient(180deg,#f0c9ba,transparent);
}
.timeline li:last-child{padding-bottom:0}
.timeline li:last-child::after{display:none}

/* chips mots-clés */
.chips{display:flex;flex-wrap:wrap;gap:11px}
.chips span{
  display:inline-flex;align-items:center;gap:.55rem;
  padding:.62rem 1.15rem;border-radius:999px;font-weight:700;font-size:.93rem;
  background:var(--surface);border:1px solid var(--line);box-shadow:var(--shadow-1);
  transition:border-color .2s,transform .2s;
}
.chips span:hover{border-color:var(--brand);transform:translateY(-2px)}
.chips .ic{width:16px;height:16px;color:var(--gold)}

/* encadré situation client */
.aside-card{
  background:linear-gradient(160deg,#0f3d29,var(--dark));color:#eaf4ec;
  border-radius:var(--r);padding:30px;box-shadow:var(--shadow-2);
}
.aside-card h3{color:#fff;display:flex;align-items:center;gap:.6rem;margin-bottom:16px}
.aside-card h3 .ic{color:var(--gold)}
.aside-card ul{margin:0;padding:0;list-style:none;display:grid;gap:12px}
.aside-card li{display:flex;gap:12px;align-items:flex-start;font-size:.95rem;line-height:1.55}
.aside-card li .ic{width:18px;height:18px;margin-top:4px;color:#7fc9a4}
.split{display:grid;gap:36px;grid-template-columns:1.1fr .9fr;align-items:start}
@media (max-width:880px){.split{grid-template-columns:1fr}}

/* ressources */
.res-card{
  display:grid;gap:22px;grid-template-columns:auto 1fr;align-items:start;
  background:linear-gradient(135deg,#fdf6ee,#fbefe6);border:1px solid #f0dcc8;
  border-radius:var(--r);padding:30px;margin-top:44px;box-shadow:var(--shadow-1);
}
.res-card .icon-tile{background:#fff;color:var(--accent);margin:0}
.res-card h3{margin-bottom:10px}
.res-card p{color:#6b5d4e;font-size:.97rem;line-height:1.7;margin-top:8px}
@media (max-width:640px){.res-card{grid-template-columns:1fr}}

/* FAQ */
.faq{display:grid;gap:14px}
.faq details{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);
  box-shadow:var(--shadow-1);overflow:hidden;transition:border-color .2s;
}
.faq details[open]{border-color:#bcd9c6}
.faq summary{
  display:flex;align-items:center;justify-content:space-between;gap:16px;
  padding:19px 22px;cursor:pointer;list-style:none;
  font-weight:800;font-size:1.04rem;font-family:var(--font-body);
}
.faq summary::-webkit-details-marker{display:none}
.faq summary .ic{color:var(--brand);transition:transform .3s}
.faq details[open] summary .ic{transform:rotate(180deg)}
.faq .faq-a{padding:0 22px 21px;color:var(--muted);line-height:1.7}

/* bandeau CTA */
.cta-band{
  position:relative;overflow:hidden;border-radius:calc(var(--r) + 8px);
  background:linear-gradient(140deg,#124b32,var(--dark));color:#fff;
  padding:clamp(40px,6vw,72px);text-align:center;box-shadow:var(--shadow-2);
}
.cta-band::before{
  content:"";position:absolute;inset:0;opacity:.35;pointer-events:none;
  background:radial-gradient(500px 260px at 12% 0%,rgba(127,201,164,.5),transparent 60%),
             radial-gradient(460px 260px at 92% 110%,rgba(228,87,46,.42),transparent 60%);
}
.cta-band h2{position:relative;color:#fff}
.cta-band p{position:relative;color:#c7dccd;max-width:36em;margin:18px auto 0}
.cta-band .btn{position:relative;margin-top:30px}

/* ---------- footer ---------- */
.footer{background:var(--dark);color:#b9cdbf;margin-top:96px}
.footer a{color:#cfe3d5;text-decoration:none;transition:color .2s}
.footer a:hover{color:#fff}
.footer-grid{display:grid;gap:44px;grid-template-columns:1.3fr 1fr 1fr;padding-block:64px}
@media (max-width:820px){.footer-grid{grid-template-columns:1fr}}
.footer .logo{color:#fff}
.footer .about{margin-top:18px;font-size:.93rem;line-height:1.7;max-width:30em;color:#9fb5a6}
.footer h4{color:#fff;font-size:.85rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;margin:0 0 18px}
.footer ul{margin:0;padding:0;list-style:none;display:grid;gap:11px;font-size:.93rem;font-weight:600}
.footer-bottom{border-top:1px solid rgba(255,255,255,.09);padding-block:22px;font-size:.84rem;color:#8aa192;display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between}

/* ---------- reveal ---------- */
html.js .reveal{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
html.js .reveal.in{opacity:1;transform:none}
html.js .reveal[data-d="1"]{transition-delay:.08s}
html.js .reveal[data-d="2"]{transition-delay:.16s}
html.js .reveal[data-d="3"]{transition-delay:.24s}
@media (prefers-reduced-motion:reduce){html.js .reveal{opacity:1;transform:none;transition:none}}

.skip{position:absolute;left:-9999px;top:0;background:#fff;color:var(--brand);padding:.8rem 1.2rem;font-weight:800;z-index:100;border-radius:0 0 12px 0}
.skip:focus{left:0}
"""

JS = """
document.documentElement.classList.add('js');
addEventListener('DOMContentLoaded',function(){
  var h=document.querySelector('.header');
  var onScroll=function(){h.classList.toggle('scrolled',scrollY>8)};
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}});
    },{threshold:.1,rootMargin:'0px 0px -40px 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  }else{
    document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});
  }
});
"""


# ---------------------------------------------------------------------------
# Gabarit de page
# ---------------------------------------------------------------------------

def nav_links(active=""):
    items = [
        (C.HUBS["creation"]["path"], C.HUBS["creation"]["nav"]),
        (C.HUBS["visibilite"]["path"], C.HUBS["visibilite"]["nav"]),
        (C.PILIER["path"], C.PILIER["nav"]),
    ]
    out = []
    for path, label in items:
        cur = ' aria-current="page"' if path == active else ""
        out.append(f'<a href="{path}"{cur}>{label}</a>')
    out.append(f'<a class="btn" href="/#metiers">Mon guide métier {icon("arrow")}</a>')
    return "\n".join(out)


def footer():
    metier_links = "\n".join(
        f'<li><a href="/creation-site-internet-{m}/">Site internet {de_pluriel(m).replace("de ", "pour ").replace("d’", "pour ")}</a></li>'
        for m in []
    )
    # liens métiers : libellés naturels
    metier_links = "\n".join(
        f'<li><a href="/creation-site-internet-{m}/">Site {C.METIERS[m]["de"]}</a></li>'
        for m in C.ORDER
    )
    return f"""
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="logo" href="/"><span class="logo-mark">L</span> Localto</a>
        <p class="about">{C.SITE["footer_about"]}</p>
      </div>
      <div>
        <h4>Vos guides</h4>
        <ul>
          <li><a href="{C.HUBS["creation"]["path"]}">{C.HUBS["creation"]["nav"]}</a></li>
          <li><a href="{C.HUBS["visibilite"]["path"]}">{C.HUBS["visibilite"]["nav"]}</a></li>
          <li><a href="{C.PILIER["path"]}">{C.PILIER["nav"]}</a></li>
        </ul>
      </div>
      <div>
        <h4>Par métier</h4>
        <ul>
          {metier_links}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Localto — Tous droits réservés.</span>
      <span>Fait avec soin pour les professionnels de proximité.</span>
    </div>
  </div>
</footer>"""


def page(*, path, title, description, body, jsonld, active=""):
    canonical = URL + path
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>'
        for j in jsonld
    )
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Localto">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{URL}{C.SITE["og_image"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#15714b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script>document.documentElement.classList.add('js')</script>
{ld}
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="header">
  <div class="container">
    <a class="logo" href="/" aria-label="Localto, retour à l'accueil"><span class="logo-mark">L</span> Localto</a>
    <nav class="nav" aria-label="Navigation principale">
      {nav_links(active)}
    </nav>
  </div>
</header>
<main id="contenu">
{body}
</main>
{footer()}
<script>{JS}</script>
</body>
</html>"""


def breadcrumb_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": URL + p}
            for i, (n, p) in enumerate(items)
        ],
    }


def crumbs_html(items):
    lis = []
    for i, (n, p) in enumerate(items):
        if i < len(items) - 1:
            lis.append(f'<li><a href="{p}">{n}</a></li>')
        else:
            lis.append(f'<li><span aria-current="page">{n}</span></li>')
    return f"""
<nav class="crumbs container" aria-label="Fil d'Ariane"><ol>{''.join(lis)}</ol></nav>"""


def section(inner, alt=False, sid=""):
    cls = "section section--alt" if alt else "section"
    idattr = f' id="{sid}"' if sid else ""
    return f'<section class="{cls}"{idattr}><div class="container">{inner}</div></section>'


def head_block(eyebrow, h2, intro=None):
    intro_html = f'<p class="lead">{intro}</p>' if intro else ""
    return f"""
<div class="section-head reveal">
  <p class="eyebrow">{eyebrow}</p>
  <h2>{h2}</h2>
  {intro_html}
</div>"""


def metier_grid(link_type="both"):
    cards = []
    for i, m in enumerate(C.ORDER):
        info = C.METIERS[m]
        links = []
        if link_type in ("both", "creation"):
            links.append(
                f'<a href="/creation-site-internet-{m}/">{icon("layout")} Créer mon site</a>'
            )
        if link_type in ("both", "visibilite"):
            links.append(
                f'<a href="/visibilite-google-{m}/">{icon("search")} Visibilité Google</a>'
            )
        cards.append(f"""
<article class="card metier-card reveal" data-d="{i % 3}">
  <div class="icon-tile">{icon(info["icon"])}</div>
  <p class="cat">{info["categorie"]}</p>
  <h3>{info["nom"][0].upper() + info["nom"][1:]}</h3>
  <p>{info["card_home"]}</p>
  <div class="metier-links">{''.join(links)}</div>
</article>""")
    return f'<div class="grid cols-3">{"".join(cards)}</div>'


def resources_card():
    return f"""
<div class="res-card reveal">
  <div class="icon-tile">{icon("bulb")}</div>
  <div>
    <h3>{C.SECTIONS["ressources_title"]}</h3>
    <p>{C.SECTIONS["ressources_p1"]}</p>
    <p>{C.SECTIONS["ressources_p2"]}</p>
  </div>
</div>"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def render_home():
    H = C.HOME
    points = "".join(f"<li>{icon('check')} {p}</li>" for p in H["hero_points"])
    hero = f"""
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="badge">{icon("pin")} {H["hero_eyebrow"]}</span>
      <h1>{H["hero_h1_before"]}<br><span class="accent">{H["hero_h1_accent"]}</span></h1>
      <p class="lead">{H["hero_intro"]}</p>
      <div class="hero-cta">
        <a class="btn" href="#metiers">{H["hero_cta1"]} {icon("arrow")}</a>
        <a class="btn btn-ghost" href="{C.PILIER["path"]}">{H["hero_cta2"]}</a>
      </div>
      <ul class="hero-points">{points}</ul>
    </div>
    {hero_art()}
  </div>
</section>"""

    metiers = section(
        head_block(H["metiers_eyebrow"], H["metiers_h2"], H["metiers_intro"]) + metier_grid(),
        sid="metiers",
    )

    feats = "".join(
        f"""
<article class="card reveal" data-d="{i}">
  <div class="icon-tile">{icon(f["icon"])}</div>
  <h3>{f["title"]}</h3>
  <p>{f["text"]}</p>
</article>"""
        for i, f in enumerate(H["features"])
    )
    features = section(
        head_block(H["features_eyebrow"], H["features_h2"]) + f'<div class="grid cols-4">{feats}</div>',
        alt=True,
    )

    steps = "".join(
        f'<li class="reveal" data-d="{i}"><div><h3>{s["title"]}</h3>'
        f'<p style="color:var(--muted);font-weight:400;margin-top:6px">{s["text"]}</p></div></li>'
        for i, s in enumerate(H["steps"])
    )
    method = section(
        f"""<div class="split">
  <div>{head_block(H["steps_eyebrow"], H["steps_h2"])}<ol class="steps">{steps}</ol></div>
  <div class="reveal" data-d="1">{resources_card().replace('margin-top:44px', '')}</div>
</div>"""
    )

    cta = section(
        f"""
<div class="cta-band reveal">
  <h2>{H["cta_h2"]}</h2>
  <p>{H["cta_text"]}</p>
  <a class="btn btn-light" href="#metiers">{H["cta_btn"]} {icon("arrow")}</a>
</div>"""
    )

    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Localto",
            "url": URL + "/",
            "description": H["description"],
            "inLanguage": "fr-FR",
        },
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Localto",
            "url": URL + "/",
            "logo": URL + C.SITE["og_image"],
        },
        breadcrumb_ld([("Accueil", "/")]),
    ]
    body = hero + metiers + features + method + cta
    return page(path="/", title=H["title"], description=H["description"], body=body, jsonld=jsonld)


def render_hub(kind):
    HUB = C.HUBS[kind]
    crumb_items = [("Accueil", "/"), (HUB["nav"], HUB["path"])]
    hero = f"""
<section class="hero hero-page">
  {crumbs_html(crumb_items)}
  <div class="container hero-grid">
    <div>
      <span class="badge">{icon("star")} {HUB["badge"]}</span>
      <h1 style="margin-top:20px">{HUB["h1"]}</h1>
      <p class="lead">{HUB["intro"]}</p>
      <div class="hero-cta">
        <a class="btn" href="#metiers">Choisir mon métier {icon("arrow")}</a>
        <a class="btn btn-ghost" href="{C.PILIER["path"]}">La méthode SEO local</a>
      </div>
    </div>
    <div class="hero-emblem">
      <span class="ring"></span><span class="dot"></span>
      <span class="disc">{icon("layout" if kind == "creation" else "search")}</span>
    </div>
  </div>
</section>"""

    points = "".join(f"<li>{icon('check')} {p}</li>" for p in HUB["method_points"])
    method = section(
        f"""<div class="split">
  <div>
    {head_block(HUB["method_eyebrow"], HUB["method_h2"], HUB["method_intro"])}
  </div>
  <div class="aside-card reveal" data-d="1">
    <h3>{icon("shield")} Vos fondamentaux</h3>
    <ul>{points}</ul>
  </div>
</div>""" + resources_card()
    )

    grid = section(
        head_block(HUB["grid_eyebrow"], HUB["grid_h2"]) + metier_grid(HUB["metier_link"]),
        alt=True,
        sid="metiers",
    )

    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": HUB["title"],
            "description": HUB["description"],
            "author": {"@type": "Organization", "name": "Localto", "url": URL},
            "publisher": {"@type": "Organization", "name": "Localto", "url": URL},
            "mainEntityOfPage": URL + HUB["path"],
            "inLanguage": "fr-FR",
        },
        breadcrumb_ld(crumb_items),
    ]
    return page(
        path=HUB["path"], title=HUB["title"], description=HUB["description"],
        body=hero + method + grid, jsonld=jsonld, active=HUB["path"],
    )


def render_pilier():
    P = C.PILIER
    crumb_items = [("Accueil", "/"), (P["nav"], P["path"])]
    hero = f"""
<section class="hero hero-page">
  {crumbs_html(crumb_items)}
  <div class="container hero-grid">
    <div>
      <span class="badge">{icon("pin")} {P["badge"]}</span>
      <h1 style="margin-top:20px">{P["h1"]}</h1>
      <p class="lead">{P["intro"]}</p>
      <div class="hero-cta">
        <a class="btn" href="#metiers">Voir mon métier {icon("arrow")}</a>
      </div>
    </div>
    <div class="hero-emblem">
      <span class="ring"></span><span class="dot"></span>
      <span class="disc">{icon("pin")}</span>
    </div>
  </div>
</section>"""

    steps = "".join(f"<li class='reveal'>{p}</li>" for p in P["method_points"])
    method = section(
        head_block(P["method_eyebrow"], P["method_h2"], P["method_intro"])
        + f'<ol class="steps" style="max-width:820px">{steps}</ol>'
        + resources_card()
    )
    grid = section(
        head_block(P["grid_eyebrow"], P["grid_h2"], P["grid_intro"]) + metier_grid(),
        alt=True,
        sid="metiers",
    )
    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": P["title"],
            "description": P["description"],
            "author": {"@type": "Organization", "name": "Localto", "url": URL},
            "publisher": {"@type": "Organization", "name": "Localto", "url": URL},
            "mainEntityOfPage": URL + P["path"],
            "inLanguage": "fr-FR",
        },
        breadcrumb_ld(crumb_items),
    ]
    return page(
        path=P["path"], title=P["title"], description=P["description"],
        body=hero + method + grid, jsonld=jsonld, active=P["path"],
    )


def render_metier(m, kind):
    """kind: 'creation' ou 'visibilite'."""
    info = C.METIERS[m]
    d = DATA[kind][m]
    S = C.SECTIONS
    is_crea = kind == "creation"
    path = f"/creation-site-internet-{m}/" if is_crea else f"/visibilite-google-{m}/"
    other_path = f"/visibilite-google-{m}/" if is_crea else f"/creation-site-internet-{m}/"
    hub = C.HUBS["creation" if is_crea else "visibilite"]
    title = info["crea_title"] if is_crea else info["vis_title"]
    desc = info["crea_desc"] if is_crea else info["vis_desc"]
    h1 = info["crea_h1"] if is_crea else info["vis_h1"]
    intro = info["crea_intro"] if is_crea else info["vis_intro"]

    crumb_items = [("Accueil", "/"), (hub["nav"], hub["path"]), (info["nom"].capitalize(), path)]

    toc = f"""
<nav class="toc" aria-label="Dans ce guide">
  <a href="#clients">Vos clients</a>
  <a href="#structure">Structure du site</a>
  <a href="#pages">Pages indispensables</a>
  <a href="#mots-cles">Mots-clés</a>
  <a href="#articles">Idées d'articles</a>
  <a href="#erreurs">Erreurs à éviter</a>
  <a href="#plan-7-jours">Plan 7 jours</a>
  <a href="#faq">FAQ</a>
</nav>"""

    other_label = (
        f"Guide visibilité Google {info['de']}" if is_crea else f"Guide création de site {info['de']}"
    )
    hero = f"""
<section class="hero hero-page">
  {crumbs_html(crumb_items)}
  <div class="container hero-grid">
    <div>
      <span class="badge">{icon("pin")} {info["vocatif"]} · {info["categorie"]}</span>
      <h1 style="margin-top:20px">{h1}</h1>
      <p class="lead">{intro}</p>
      <div class="hero-cta">
        <a class="btn" href="#plan-7-jours">Mon plan d'action 7 jours {icon("arrow")}</a>
        <a class="btn btn-ghost" href="{other_path}">{other_label}</a>
      </div>
      {toc}
    </div>
    <div class="hero-emblem">
      <span class="ring"></span><span class="dot"></span>
      <span class="disc">{icon(info["icon"])}</span>
    </div>
  </div>
</section>"""

    # --- vos clients ---
    exemples = "".join(f"<li>{icon('quote')} {e}</li>" for e in d.get("exemples", []))
    probleme = section(
        f"""<div class="split">
  <div>
    {head_block(S["probleme_eyebrow"], S["probleme_h2"])}
    <p class="lead reveal" style="margin-bottom:18px">{d["persona_pain"]}</p>
    <p class="reveal" style="color:var(--muted)">{S["probleme_intro"].format(intention=d["intention"])}</p>
  </div>
  <div class="aside-card reveal" data-d="1">
    <h3>{icon("search")} {S["exemples_label"]}</h3>
    <ul>{exemples}</ul>
  </div>
</div>""",
        sid="clients",
    )

    # --- structure ---
    structure_items = "".join(f"<li class='reveal'>{s}</li>" for s in d["structure"])
    structure = section(
        head_block(S["structure_eyebrow"], S["structure_h2"], S["structure_intro"])
        + f'<ol class="steps" style="max-width:820px">{structure_items}</ol>',
        alt=True,
        sid="structure",
    )

    # --- pages indispensables ---
    pages_cards = "".join(
        f'<li class="reveal" data-d="{i % 3}">{icon("check", "ic")} {p}</li>'
        for i, p in enumerate(d["pages_indispensables"])
    )
    pages_sec = section(
        head_block(S["pages_eyebrow"], S["pages_h2"].format(de_metier=info["de"]), S["pages_intro"])
        + f'<ul class="list list-check grid cols-2" style="max-width:900px">{pages_cards}</ul>',
        sid="pages",
    )

    # --- mots-clés ---
    kw = "".join(f"<span>{icon('key')} {k}</span>" for k in d["keywords"])
    kw_h2 = S["keywords_h2_crea"] if is_crea else S["keywords_h2_vis"]
    keywords = section(
        head_block(S["keywords_eyebrow"], kw_h2, S["keywords_intro"])
        + f'<div class="chips reveal">{kw}</div>',
        alt=True,
        sid="mots-cles",
    )

    # --- articles ---
    art = "".join(f"<li class='reveal'>{icon('bulb')} {a}</li>" for a in d["articles"])
    articles = section(
        head_block(S["articles_eyebrow"], S["articles_h2"], S["articles_intro"])
        + f'<ul class="list" style="max-width:820px">{art}</ul>'
        + resources_card(),
        sid="articles",
    )

    # --- erreurs + preuves ---
    err = "".join(f"<li class='reveal'>{icon('x')} {e}</li>" for e in d["erreurs"])
    prv = "".join(f"<li class='reveal'>{icon('check')} {p}</li>" for p in d["preuves"])
    err_prv = section(
        f"""<div class="split" style="grid-template-columns:1fr 1fr;gap:56px">
  <div id="erreurs">
    {head_block(S["erreurs_eyebrow"], S["erreurs_h2"], S["erreurs_intro"].format(de_pluriel=de_pluriel(m)))}
    <ul class="list list-x">{err}</ul>
  </div>
  <div id="preuves">
    {head_block(S["preuves_eyebrow"], S["preuves_h2"], S["preuves_intro"])}
    <ul class="list list-check">{prv}</ul>
  </div>
</div>""",
        alt=True,
    )

    # --- plan 7 jours ---
    plan = "".join(f"<li class='reveal'>{p}</li>" for p in d["plan"])
    plan_sec = section(
        head_block(S["plan_eyebrow"], S["plan_h2"], S["plan_intro"])
        + f'<ol class="timeline" style="max-width:760px">{plan}</ol>',
        sid="plan-7-jours",
    )

    # --- FAQ ---
    faq_items = "".join(
        f"""
<details class="reveal">
  <summary><span>{f["q"]}</span>{icon("chevron")}</summary>
  <div class="faq-a">{f["a"]}</div>
</details>"""
        for f in d["faq"]
    )
    faq = section(
        head_block(S["faq_eyebrow"], S["faq_h2"])
        + f'<div class="faq" style="max-width:820px">{faq_items}</div>',
        alt=True,
        sid="faq",
    )

    # --- pour aller plus loin ---
    idx = C.ORDER.index(m)
    n1, n2 = C.ORDER[(idx + 1) % len(C.ORDER)], C.ORDER[(idx + 2) % len(C.ORDER)]
    if is_crea:
        related = [
            (other_path, f"Visibilité Google pour {info['nom']}",
             "Faites remonter votre activité dans les recherches locales.", "search"),
            (C.PILIER["path"], "La méthode SEO local complète",
             "Fiche Google, avis, pages locales : la vue d'ensemble.", "pin"),
            (f"/creation-site-internet-{n1}/", f"Créer un site {C.METIERS[n1]['de']}",
             f"Le guide dédié aux {C.METIERS[n1]['pluriel']}.", C.METIERS[n1]["icon"]),
            (f"/creation-site-internet-{n2}/", f"Créer un site {C.METIERS[n2]['de']}",
             f"Le guide dédié aux {C.METIERS[n2]['pluriel']}.", C.METIERS[n2]["icon"]),
        ]
    else:
        related = [
            (other_path, f"Créer un site internet {info['de']}",
             "La structure et les pages qui transforment les visiteurs en clients.", "layout"),
            (C.PILIER["path"], "La méthode SEO local complète",
             "Fiche Google, avis, pages locales : la vue d'ensemble.", "pin"),
            (f"/visibilite-google-{n1}/", f"Visibilité Google pour {C.METIERS[n1]['nom']}",
             f"Le guide dédié aux {C.METIERS[n1]['pluriel']}.", C.METIERS[n1]["icon"]),
            (f"/visibilite-google-{n2}/", f"Visibilité Google pour {C.METIERS[n2]['nom']}",
             f"Le guide dédié aux {C.METIERS[n2]['pluriel']}.", C.METIERS[n2]["icon"]),
        ]
    rel_cards = "".join(
        f"""
<a class="card reveal" data-d="{i % 3}" href="{href}">
  <div class="icon-tile">{icon(ic)}</div>
  <h3>{t}</h3>
  <p>{txt}</p>
</a>"""
        for i, (href, t, txt, ic) in enumerate(related)
    )
    related_sec = section(
        head_block(S["related_eyebrow"], S["related_h2"])
        + f'<div class="grid cols-4">{rel_cards}</div>'
    )

    cta = section(
        f"""
<div class="cta-band reveal">
  <h2>Passez à l'action dès aujourd'hui</h2>
  <p>Votre plan est prêt : une action par jour pendant 7 jours pour que vos clients vous trouvent — et vous choisissent.</p>
  <a class="btn btn-light" href="#plan-7-jours">Revoir mon plan d'action {icon("arrow")}</a>
</div>"""
    )

    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "author": {"@type": "Organization", "name": "Localto", "url": URL},
            "publisher": {"@type": "Organization", "name": "Localto", "url": URL},
            "mainEntityOfPage": URL + path,
            "inLanguage": "fr-FR",
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
                }
                for f in d["faq"]
            ],
        },
        breadcrumb_ld(crumb_items),
    ]
    body = (
        hero + probleme + structure + pages_sec + keywords + articles
        + err_prv + plan_sec + faq + related_sec + cta
    )
    return page(path=path, title=title, description=desc, body=body, jsonld=jsonld, active=hub["path"])


# ---------------------------------------------------------------------------
# Favicon
# ---------------------------------------------------------------------------

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#1a8a5c"/><stop offset="1" stop-color="#0e5638"/></linearGradient></defs>
<rect width="64" height="64" rx="16" fill="url(#g)"/>
<path d="M32 50c0 0-13-10.4-13-19a13 13 0 1 1 26 0c0 8.6-13 19-13 19z" fill="#fff"/>
<circle cx="32" cy="30" r="5.5" fill="#e4572e"/>
</svg>"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def write(path, content):
    p = OUT / path.lstrip("/")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    write("favicon.svg", FAVICON)
    # Force l'UTF-8 et les bons types MIME côté serveur (Apache / LiteSpeed)
    write(
        ".htaccess",
        "AddDefaultCharset UTF-8\n"
        "AddCharset UTF-8 .html .css .js .svg .xml .txt\n"
        "AddType image/svg+xml .svg\n"
        "DirectoryIndex index.html\n"
        "Options -Indexes\n",
    )
    shutil.copy(ROOT / "localto-dashboard.png", OUT / "localto-dashboard.png")

    pages = {"/": render_home()}
    pages[C.HUBS["creation"]["path"]] = render_hub("creation")
    pages[C.HUBS["visibilite"]["path"]] = render_hub("visibilite")
    pages[C.PILIER["path"]] = render_pilier()
    for m in C.ORDER:
        pages[f"/creation-site-internet-{m}/"] = render_metier(m, "creation")
        pages[f"/visibilite-google-{m}/"] = render_metier(m, "visibilite")

    for path, html_out in pages.items():
        write(path.rstrip("/") + "/index.html" if path != "/" else "index.html", html_out)

    # robots + sitemaps (le robots.txt reste servi, mais n'est plus lié dans le site)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap-index.xml\n")
    lastmod = "2026-07-09T00:00:00.000Z"
    urls = "".join(
        f"<url><loc>{URL}{p}</loc><lastmod>{lastmod}</lastmod></url>" for p in pages
    )
    write(
        "sitemap-0.xml",
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>",
    )
    write(
        "sitemap-index.xml",
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<sitemap><loc>{URL}/sitemap-0.xml</loc></sitemap></sitemapindex>",
    )
    print(f"OK — {len(pages)} pages générées dans {OUT}")


if __name__ == "__main__":
    main()
