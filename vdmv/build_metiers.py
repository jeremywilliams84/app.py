# -*- coding: utf-8 -*-
"""Régénère le contenu éditorial des 15 pages métiers de Visible dans ma ville.

Le design, le générateur, les FAQ, le footer et les liens croisés sont
conservés : seuls les blocs éditoriaux (head SEO, héro, article, plan latéral)
sont réécrits à partir des données propres à chaque métier.

Usage :  python3 vdmv/build_metiers.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
BASE = json.loads((ROOT / "metiers_base.json").read_text())
DATA = json.loads((ROOT / "metiers_data.json").read_text())

DATE_MODIFIED = "2026-07-17"

# Rotations de titres de sections (chaque formulation ne sert que 3 fois,
# toujours suivie d'un contenu propre au métier).
INTENTS_H2 = [
    "Les recherches qui précèdent le premier contact",
    "Ce que vos clients tapent réellement sur Google",
    "Les formulations à viser sur votre page",
    "Des recherches concrètes, pas du jargon",
    "Les requêtes locales qui comptent",
]
PREUVES_H2 = [
    "La réassurance à intégrer sur la page",
    "Ce que votre page doit prouver",
    "Les éléments de confiance à afficher",
    "Les preuves qui font choisir votre page",
    "De quoi lever les doutes avant le contact",
]
ERREURS_H2 = [
    "Les pièges propres à votre métier",
    "Les erreurs qui plombent ce type de page",
    "Ce qu'il faut éviter d'écrire",
    "Les faux pas fréquents à corriger",
    "Les erreurs qui coûtent des contacts",
]

ORDER = [
    "pisciniste", "couvreur", "plombier", "electricien", "chauffagiste",
    "paysagiste", "menuisier", "carreleur", "macon", "serrurier",
    "conciergerie-airbnb", "sophrologue", "secretaire-independante",
    "wedding-planner", "photographe-mariage",
]


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_prose(slug, i):
    b, d = BASE[slug], DATA[slug]
    recherches = "".join(f"<li>{r}</li>" for r in b["recherches"])
    services = "".join(f"<li>{s}</li>" for s in d["services"])
    structure = "".join(f"<li>{s}</li>" for s in d["pageStructure"])
    trust = "".join(f"<li>{s}</li>" for s in d["trustSignals"])
    mistakes = "".join(f"<li>{m}</li>" for m in d["mistakes"])
    localto = ""
    if d.get("localto_link"):
        localto = f"<p>{d['localto_link']['text']}</p>"
    return f"""<article class="prose">
        <p class="eyebrow">Enjeux locaux</p>
        <h2>{d["enjeux_h2"]}</h2>
        <p>{b["pourquoi"]}</p>
        <p>{d["enjeux_extra"]}</p>
        <h2>{INTENTS_H2[i % 5]}</h2>
        <p>{d["intents_intro"]}</p>
        <ul>{recherches}</ul>
        <h2>{d["services_h2"]}</h2>
        <ul>{services}</ul>
        <h2>{d["modele_h2"]}</h2>
        <p>Un exemple de title pour les résultats Google :</p>
        <blockquote>{d["titleExample"]}</blockquote>
        <p>Une meta description possible :</p>
        <blockquote>{d["metaExample"]}</blockquote>
        <p>Le H1 affiché en haut de la page :</p>
        <blockquote>{d["h1Example"]}</blockquote>
        <p>Puis les sections (H2) à enchaîner dans l'ordre :</p>
        <ol>{structure}</ol>
        <h2>{PREUVES_H2[i % 5]}</h2>
        <ul>{trust}</ul>
        <h2>{ERREURS_H2[i % 5]}</h2>
        <ul>{mistakes}</ul>
        {localto}
      </article>"""


def build_sideplan(slug):
    d = DATA[slug]
    steps = "".join(f"<li>{s}</li>" for s in d["sidePlan"])
    return f"<h3>Plan express pour votre page</h3>\n          <ol>{steps}</ol>"


def patch_jsonld(s, title, desc):
    def repl(m):
        try:
            j = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        if j.get("@type") == "Article":
            j["headline"] = title
            j["description"] = desc
            j["dateModified"] = DATE_MODIFIED
            return ('<script type="application/ld+json">'
                    + json.dumps(j, ensure_ascii=False) + "</script>")
        return m.group(0)
    return re.sub(r'<script type="application/ld\+json">(\{.*?\})</script>',
                  repl, s, flags=re.S)


def patch_page(slug, i):
    f = SITE / "metiers" / f"{slug}.html"
    s = f.read_text()
    d = DATA[slug]
    title, desc = d["title"], d["desc"]

    # head
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", s, 1)
    for attr in ("name=\"description\"", "property=\"og:description\"", "name=\"twitter:description\""):
        s = re.sub(rf'(<meta {attr} content=")[^"]*(")', rf"\g<1>{desc}\g<2>", s, 1)
    for attr in ("property=\"og:title\"", "name=\"twitter:title\""):
        s = re.sub(rf'(<meta {attr} content=")[^"]*(")', rf"\g<1>{title}\g<2>", s, 1)
    s = patch_jsonld(s, title, desc)

    # héro
    s = re.sub(r'<p class="eyebrow">Exemple métier</p>',
               '<p class="eyebrow">Modèle métier</p>', s, 1)
    s = re.sub(r"<h1>.*?</h1>", f"<h1>{d['h1']}</h1>", s, 1, flags=re.S)
    s = re.sub(r'<p class="lead">.*?</p>', f'<p class="lead">{d["lead"]}</p>', s, 1, flags=re.S)
    s = re.sub(r'<a class="primary-btn" href="#generateur">.*?</a>',
               f'<a class="primary-btn" href="#generateur">{d["cta_hero"]} '
               '<span class="btn-arrow">→</span></a>', s, 1, flags=re.S)

    # article éditorial
    s = re.sub(r'<article class="prose">.*?</article>', build_prose(slug, i), s, 1, flags=re.S)

    # plan latéral + bouton
    s = re.sub(r"<h3>Plan rapide</h3>\s*<ol>.*?</ol>", build_sideplan(slug), s, 1, flags=re.S)
    s = re.sub(r'(<a class="primary-btn" href="#generateur" style="[^"]*">).*?(<span class="btn-arrow">)',
               rf"\g<1>{DATA[slug]['cta_side']} \g<2>", s, 1, flags=re.S)

    f.write_text(s)
    return title


def main():
    seen = set()
    for i, slug in enumerate(ORDER):
        t = patch_page(slug, i)
        assert t not in seen, f"title dupliqué : {t}"
        seen.add(t)
        print(f"  ✓ {slug}: {t}")
    # sitemap : rafraîchir le lastmod des pages métiers
    sm = SITE / "sitemap.xml"
    x = sm.read_text()
    x = re.sub(r"(<loc>https://visible-dans-ma-ville\.fr/metiers/[^<]+</loc>\s*<lastmod>)[^<]+(</lastmod>)",
               rf"\g<1>{DATE_MODIFIED}\g<2>", x)
    sm.write_text(x)
    print(f"OK — {len(ORDER)} pages métiers régénérées")


if __name__ == "__main__":
    main()
