#!/usr/bin/env python3
"""Génère les pages HTML du site « Générateur de page métier + ville ».

Usage : python3 build_site.py

Le script lit metiers_data.json (contenus par métier) et écrit dans
generateur-page-metier-ville/ :
  - index.html, exemples-metiers.html, les 3 articles, les pages légales
  - metiers/<slug>.html (15 pages)
  - sitemap.xml, 404.html
  - assets/og-cover.png (si Pillow est installé)

Toute modification de structure (header, footer, générateur, SEO) se fait
ici, en un seul endroit, puis se propage à tout le site.
"""

import json
import os
import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "generateur-page-metier-ville")

DOMAIN = "https://generateur-page-metier-ville.fr"
SITE_NAME = "Métier + Ville"
WISEWAND_URL = "https://wisewand.ai/?fpr=wisewand-seo"
HOSTINGER_URL = "https://www.hostg.xyz/SHJit"
TODAY = datetime.date.today().isoformat()
YEAR = datetime.date.today().year

FONTS_URL = ("https://fonts.googleapis.com/css2"
             "?family=Fraunces:opsz,wght@9..144,400..700"
             "&family=Inter:wght@400..700&display=swap")

with open(os.path.join(BASE, "metiers_data.json"), encoding="utf-8") as f:
    METIERS = json.load(f)

# Ordre d'affichage (nav, footer, marquee, pages liées)
ORDER = ["pisciniste", "couvreur", "plombier", "electricien", "chauffagiste",
         "paysagiste", "menuisier", "carreleur", "macon", "serrurier",
         "conciergerie-airbnb", "sophrologue", "secretaire-independante",
         "wedding-planner", "photographe-mariage"]


def ld(schema):
    return ('<script type="application/ld+json">'
            + json.dumps(schema, ensure_ascii=False) + "</script>")


def head(title, desc, path, schemas=(), og_type="website", noindex=False):
    url = DOMAIN + path
    robots = '\n  <meta name="robots" content="noindex, follow">' if noindex else ""
    schema_html = "\n  ".join(ld(s) for s in schemas)
    if schema_html:
        schema_html = "\n  " + schema_html
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">{robots}
  <link rel="canonical" href="{url}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMAIN}/assets/og-cover.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{DOMAIN}/assets/og-cover.png">
  <meta name="theme-color" content="#12403a">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FONTS_URL}">
  <link rel="stylesheet" href="/assets/styles.css">{schema_html}
</head>
<body>
<a class="skip-link" href="#main">Aller au contenu</a>"""


def header():
    return """
<header class="topbar">
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="Accueil Métier + Ville">
      <span class="brand-mark">MV</span><span><strong>Métier + Ville</strong><small>Pages locales utiles</small></span>
    </a>
    <nav class="navlinks" aria-label="Navigation principale">
      <a href="/#generateur">Générateur</a>
      <a href="/exemples-metiers.html">Exemples métiers</a>
      <a href="/pourquoi-votre-site-ne-ramene-pas-de-clients.html">Pourquoi ça bloque</a>
      <a href="/rediger-page-avec-wisewand.html">Rédiger la page</a>
      <a class="nav-cta" href="/#generateur">Créer ma page</a>
    </nav>
    <button class="menu-btn" type="button" aria-label="Ouvrir le menu" aria-expanded="false">Menu</button>
  </div>
</header>"""


def breadcrumbs(items):
    """items : liste (label, href) — le dernier est la page courante (href ignoré)."""
    lis = []
    for i, (label, href) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li><span aria-current="page">{label}</span></li>')
        else:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
    return ('<nav class="breadcrumbs" aria-label="Fil d’Ariane"><ol>'
            + "".join(lis) + "</ol></nav>")


def breadcrumbs_schema(items, path):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label,
             "item": DOMAIN + (href if i < len(items) - 1 else path)}
            for i, (label, href) in enumerate(items)
        ],
    }


def tool_section(default_metier="", default_service=""):
    return f"""
  <section class="tool-section" id="generateur">
    <div class="wrap">
      <div class="tool-card" data-default-metier="{default_metier}" data-default-service="{default_service}">
        <div class="tool-intro">
          <p class="eyebrow">Outil gratuit</p>
          <h2>Générateur de page “métier&nbsp;+&nbsp;ville”</h2>
          <p>Indiquez votre métier, votre ville et une prestation importante. Vous obtenez une structure de page simple : titre, sections, questions fréquentes, appels à l’action et idées de recherches à viser.</p>
          <ul class="plain-list compact">
            <li>Pas de jargon technique.</li>
            <li>Un plan réutilisable pour chaque ville.</li>
            <li>Une sortie prête à transmettre à votre rédacteur ou à créer avec Wisewand.</li>
          </ul>
        </div>
        <div class="tool-form">
          <div class="form-grid">
            <label>Votre métier
              <input id="metier" name="metier" value="pisciniste" placeholder="Ex : pisciniste, couvreur, sophrologue">
            </label>
            <label>Votre ville principale
              <input id="ville" name="ville" value="Avignon" placeholder="Ex : Avignon">
            </label>
            <label>Votre prestation prioritaire
              <input id="service" name="service" value="construction de piscine" placeholder="Ex : rénovation de toiture">
            </label>
            <label>Votre client idéal
              <select id="clientType" name="clientType">
                <option>particuliers près de chez moi</option>
                <option>propriétaires de maison</option>
                <option>dirigeants de petites entreprises</option>
                <option>futurs mariés</option>
                <option>professionnels du bâtiment</option>
              </select>
            </label>
          </div>
          <button class="primary-btn" type="button" onclick="generateLocalPage()">Générer mon plan de page <span class="btn-arrow">→</span></button>
          <p class="microcopy">Le résultat apparaît immédiatement. Vous pourrez aussi l’envoyer par email.</p>
        </div>
        <div class="result-panel" id="resultPanel" aria-live="polite">
          <div class="empty-state">
            <span>Exemple</span>
            <strong>“Pisciniste à Avignon : construction et rénovation de piscine”</strong>
            <p>Le générateur va créer une base de page locale utile, avec des textes simples et des questions fréquentes.</p>
          </div>
        </div>
        <div class="lead-capture" id="leadCapture">
          <div>
            <strong>Recevoir le plan par email</strong>
            <p>Récupérez le plan généré et une checklist de publication. Vous pourrez ensuite rédiger la page avec Wisewand ou la publier sur votre site.</p>
          </div>
          <form id="leadForm" action="/lead.php" method="post">
            <input type="text" name="name" placeholder="Prénom" autocomplete="given-name" aria-label="Prénom">
            <input type="email" name="email" placeholder="Email professionnel" required autocomplete="email" aria-label="Email professionnel">
            <input type="hidden" name="source" value="generateur-page-metier-ville">
            <input type="hidden" name="generated_plan" id="generatedPlanInput">
            <button class="secondary-btn" type="submit">M’envoyer le plan</button>
            <p class="form-status" id="formStatus" role="status"></p>
          </form>
        </div>
      </div>
    </div>
  </section>"""


def soft_cta():
    return f"""
  <section class="soft-cta">
    <div class="wrap cta-grid">
      <div>
        <p class="eyebrow">Étape suivante</p>
        <h2>Vous avez le plan. Il faut maintenant publier la page.</h2>
        <p>Le plus long n’est pas de trouver l’idée. C’est de rédiger une page claire, complète, puis de la mettre en ligne sur un site rapide. Voici les deux solutions naturelles après le générateur.</p>
      </div>
      <div class="solution-cards">
        <a class="solution-card" href="{WISEWAND_URL}" rel="sponsored noopener" target="_blank">
          <span>Rédaction</span>
          <strong>Créer la page avec Wisewand</strong>
          <p>Utilisez le plan généré comme base pour obtenir une page structurée et prête à retravailler.</p>
        </a>
        <a class="solution-card" href="{HOSTINGER_URL}" rel="sponsored noopener" target="_blank">
          <span>Mise en ligne</span>
          <strong>Héberger le site avec Hostinger</strong>
          <p>Solution simple pour publier un site vitrine ou WordPress sans infrastructure compliquée.</p>
        </a>
      </div>
    </div>
  </section>"""


def faq_section(faq, title="Questions fréquentes", eyebrow="On vous répond"):
    items = "\n".join(
        f"""      <details class="faq-item">
        <summary>{q}</summary>
        <div class="faq-body"><p>{a}</p></div>
      </details>""" for q, a in faq)
    return f"""
  <section class="section faq-section">
    <div class="wrap">
      <p class="eyebrow">{eyebrow}</p>
      <h2>{title}</h2>
{items}
    </div>
  </section>"""


def faq_schema(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }


def footer():
    half = (len(ORDER) + 1) // 2
    metier_links = "".join(
        f'<a href="/metiers/{s}.html">{METIERS[s]["label"]}</a>' for s in ORDER)
    return f"""
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="brand footer-brand" href="/"><span class="brand-mark">MV</span><span><strong>Métier + Ville</strong><small>Un outil simple pour créer les bonnes pages locales.</small></span></a>
      <p>Ce site aide les artisans, indépendants et TPE à préparer des pages plus claires pour être trouvés par des clients locaux. Certains liens sont affiliés.</p>
    </div>
    <div>
      <h3>Outils</h3>
      <a href="/#generateur">Générateur de page métier + ville</a>
      <a href="/exemples-metiers.html">Exemples par métier</a>
      <a href="/ou-heberger-son-site-pro.html">Héberger son site pro</a>
    </div>
    <div>
      <h3>Ressources</h3>
      <a href="/pourquoi-votre-site-ne-ramene-pas-de-clients.html">Pourquoi votre site ne rapporte pas</a>
      <a href="/rediger-page-avec-wisewand.html">Rédiger avec Wisewand</a>
      <a href="/mentions-legales.html">Mentions légales</a>
      <a href="/politique-confidentialite.html">Confidentialité</a>
    </div>
    <div>
      <h3>Pages métiers</h3>
      <div class="footer-metiers">{metier_links}</div>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© {YEAR} {SITE_NAME}. Tous droits réservés.</span>
    <span>Fait pour les artisans, TPE et indépendants en France.</span>
  </div>
</footer>
<a class="floating-cta" href="/#generateur">⚡ Générer ma page</a>
<script src="/assets/script.js" defer></script>
</body>
</html>"""


def marquee():
    links = "".join(
        f'<a href="/metiers/{s}.html">{METIERS[s]["label"]}</a>' for s in ORDER)
    # piste doublée pour un défilement continu ; la copie est masquée aux lecteurs d'écran
    return f"""
  <div class="marquee" aria-label="Métiers couverts">
    <div class="marquee-track">{links}<span aria-hidden="true" style="display:contents">{links}</span></div>
  </div>"""


def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "url": DOMAIN + "/",
        "logo": DOMAIN + "/assets/favicon.svg",
        "description": "Outil gratuit pour aider les artisans, TPE et indépendants à créer des pages métier + ville et être trouvés par des clients locaux.",
    }


# --------------------------------------------------------------------- pages

HOME_FAQ = [
    ["Le générateur de page métier + ville est-il gratuit ?",
     "Oui, entièrement. Vous indiquez votre métier, votre ville et votre prestation principale, et vous obtenez immédiatement un plan de page complet : titre, structure, questions fréquentes et recherches à viser. Aucune inscription n’est nécessaire."],
    ["À qui s’adresse cet outil ?",
     "Aux artisans, TPE et indépendants qui veulent être trouvés par des clients de leur ville : pisciniste, couvreur, plombier, électricien, paysagiste, mais aussi sophrologue, wedding planner, conciergerie Airbnb ou secrétaire indépendante."],
    ["Que contient le plan de page généré ?",
     "Un titre optimisé, une URL conseillée, une description pour Google, la liste des recherches simples à viser, les sections recommandées et les questions fréquentes à ajouter. Vous pouvez le copier, le recevoir par email ou le transmettre à votre rédacteur."],
    ["Pourquoi créer une page par métier et par ville ?",
     "Parce que vos clients ne tapent pas le nom de votre entreprise : ils tapent un besoin et une ville, comme « devis piscine Avignon » ou « réparation toiture Cavaillon ». Une page dédiée qui répond précisément à cette recherche a beaucoup plus de chances d’apparaître sur Google qu’une page d’accueil générale."],
    ["Combien de temps pour être visible sur Google ?",
     "Cela dépend de la concurrence locale et de la qualité de la page, mais une page complète et utile sur un site rapide peut se positionner en quelques semaines sur des recherches « métier + ville » peu disputées."],
]


def build_home():
    path = "/"
    title = "Générateur de page métier + ville | Attirer des clients locaux"
    desc = ("Créez gratuitement le plan d’une page métier + ville pour être trouvé sur Google "
            "par des clients de votre commune. Pensé pour artisans, TPE et indépendants.")
    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE_NAME,
            "url": DOMAIN + "/",
            "inLanguage": "fr-FR",
            "publisher": org_schema(),
        },
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Générateur de page métier + ville",
            "url": DOMAIN + "/",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web",
            "inLanguage": "fr-FR",
            "description": "Un générateur gratuit pour préparer une page locale simple par métier et par ville.",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        },
        faq_schema(HOME_FAQ),
    ]
    six = ORDER[:6]
    mini_cards = "".join(
        f'<a class="mini-card" href="/metiers/{s}.html"><strong>{METIERS[s]["label"]}</strong>'
        f'<span>{METIERS[s]["objectif"][0].lower() + METIERS[s]["objectif"][1:-1]}</span>'
        f'<span class="card-cta">Voir l’exemple <span class="btn-arrow">→</span></span></a>'
        for s in six)
    queries = json.dumps([
        "pisciniste avignon devis piscine",
        "couvreur cavaillon réparation toiture",
        "sophrologue lyon 3 gestion du stress",
        "plombier marseille dépannage urgent",
        "paysagiste aix-en-provence création jardin",
    ], ensure_ascii=False).replace('"', "&quot;")

    html = head(title, desc, path, schemas) + header() + f"""
<main id="main">
  <section class="hero">
    <div class="orb orb-a" aria-hidden="true"></div>
    <div class="orb orb-b" aria-hidden="true"></div>
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <p class="eyebrow">Pour artisans, TPE et indépendants</p>
        <h1>Créez une page <span class="hl">“métier&nbsp;+&nbsp;ville”</span> pour être trouvé par vos clients locaux.</h1>
        <p class="lead">Exemples : <strong>pisciniste Avignon</strong>, <strong>couvreur Cavaillon</strong>, <strong>sophrologue Lyon 3</strong>. L’outil vous aide à préparer une page claire, utile et orientée demandes de devis.</p>
        <div class="hero-actions">
          <a class="primary-btn" href="#generateur">Générer ma page gratuitement <span class="btn-arrow">→</span></a>
          <a class="ghost-btn" href="/exemples-metiers.html">Voir les exemples métiers</a>
        </div>
        <div class="trust-row">
          <span>✓ 100 % gratuit</span><span>✓ sans inscription</span><span>✓ résultat immédiat</span><span>✓ langage simple</span>
        </div>
        <div class="hero-stats">
          <div><strong data-count="15">15</strong><span>métiers guidés</span></div>
          <div><strong data-count="7">7</strong><span>sections par plan</span></div>
          <div><strong data-count="100" data-suffix=" %">100 %</strong><span>gratuit, sans compte</span></div>
        </div>
      </div>
      <div class="hero-panel" aria-hidden="true">
        <div class="browser-card">
          <div class="browser-top"><span></span><span></span><span></span></div>
          <div class="search-line" data-queries="{queries}">pisciniste avignon devis piscine</div>
          <div class="page-preview">
            <small>Page recommandée</small>
            <strong>Pisciniste à Avignon : construction et rénovation de piscine</strong>
            <p>Une page claire qui explique les prestations, la zone d’intervention, les prix indicatifs, les réalisations et les prochaines étapes pour demander un devis.</p>
          </div>
          <div class="mini-list"><span>H1 optimisé</span><span>Questions fréquentes</span><span>CTA devis</span><span>Zones proches</span></div>
        </div>
      </div>
    </div>
  </section>
{marquee()}
  <section class="section narrow-intro">
    <div class="wrap">
      <p class="eyebrow">Le vrai problème</p>
      <h2>La plupart des petits sites ne manquent pas de design. Ils manquent de pages qui répondent aux recherches locales.</h2>
      <p>Un client ne tape pas toujours le nom de votre entreprise. Il tape souvent un besoin, un métier et une ville : “réparation toiture Cavaillon”, “devis piscine Avignon”, “secrétaire indépendante Marseille”. Ce site vous aide à construire ces pages sans parler en jargon technique.</p>
    </div>
  </section>

  <section class="section cards-section">
    <div class="wrap cards-3">
      <article class="info-card">
        <span>1</span>
        <h3>Choisissez un métier</h3>
        <p>Pisciniste, couvreur, plombier, paysagiste, sophrologue, conciergerie Airbnb, wedding planner...</p>
      </article>
      <article class="info-card">
        <span>2</span>
        <h3>Ajoutez une ville</h3>
        <p>Votre commune principale ou une zone où vous voulez recevoir plus de demandes.</p>
      </article>
      <article class="info-card">
        <span>3</span>
        <h3>Publiez une vraie page</h3>
        <p>Un titre clair, des sections utiles, des questions fréquentes et un bouton de contact visible.</p>
      </article>
    </div>
  </section>
{tool_section()}
  <section class="section">
    <div class="wrap split">
      <div>
        <p class="eyebrow">Requêtes simples à viser</p>
        <h2>Des formulations que les pros comprennent et que les prospects utilisent.</h2>
        <p>Le site évite de mettre “SEO” partout. Les pages parlent de clients, de ville, de demandes, de devis et de visibilité sur Google.</p>
      </div>
      <div class="keyword-box">
        <span>comment être visible sur Google quand on est artisan</span><span>comment avoir plus de clients dans sa ville</span><span>créer une page métier ville</span><span>que mettre sur une page artisan + ville</span><span>pourquoi mon site internet ne m’apporte pas de clients</span><span>comment recevoir plus de demandes de devis</span><span>site vitrine artisan qui rapporte des clients</span><span>apparaître sur Google dans sa commune</span>
      </div>
    </div>
  </section>

  <section class="section examples-strip">
    <div class="wrap">
      <div class="section-title-row">
        <div>
          <p class="eyebrow">Pages prêtes à indexer</p>
          <h2>Exemples par métier</h2>
        </div>
        <a class="ghost-btn" href="/exemples-metiers.html">Tout voir <span class="btn-arrow">→</span></a>
      </div>
      <div class="cards-3 small-cards">
        {mini_cards}
      </div>
    </div>
  </section>
{faq_section(HOME_FAQ, "Questions fréquentes sur le générateur")}{soft_cta()}
</main>""" + footer()
    write("index.html", html)


def build_exemples():
    path = "/exemples-metiers.html"
    title = "Exemples de pages métier + ville | Artisans, TPE, indépendants"
    desc = ("Des exemples concrets de pages métier + ville pour piscinistes, couvreurs, plombiers, "
            "paysagistes, sophrologues et autres pros locaux.")
    crumbs = [("Accueil", "/"), ("Exemples métiers", path)]
    schemas = [
        breadcrumbs_schema(crumbs, path),
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": title,
            "url": DOMAIN + path,
            "inLanguage": "fr-FR",
            "description": desc,
        },
    ]
    cards = "".join(f"""
      <a class="trade-card" href="/metiers/{s}.html">
        <span>{METIERS[s]['default_metier']}</span>
        <h2>Créer une page {METIERS[s]['default_metier']} + ville</h2>
        <p>{METIERS[s]['why_p']}</p>
        <strong>Voir l’exemple <span class="btn-arrow">→</span></strong>
      </a>""" for s in ORDER)
    html = head(title, desc, path, schemas) + header() + f"""
<main id="main">
  <section class="page-hero compact-hero">
    <div class="orb orb-a" aria-hidden="true"></div>
    <div class="wrap">
      {breadcrumbs(crumbs)}
      <p class="eyebrow">Exemples concrets</p>
      <h1>Pages <span class="hl">“métier&nbsp;+&nbsp;ville”</span> par secteur</h1>
      <p class="lead">Chaque page cible des recherches simples : un métier, une ville, une prestation, un besoin de devis ou de rendez-vous.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap trade-grid">{cards}
    </div>
  </section>
{tool_section()}{soft_cta()}
</main>""" + footer()
    write("exemples-metiers.html", html)


def related_links(exclude=None):
    links = "".join(
        f'<a href="/metiers/{s}.html">{METIERS[s]["label"]}</a>'
        for s in ORDER if s != exclude)
    return f"""
  <section class="section related-section">
    <div class="wrap">
      <p class="eyebrow">Autres exemples</p>
      <h2>Explorer les autres métiers</h2>
      <div class="related-links">{links}</div>
    </div>
  </section>"""


def build_metier(slug):
    m = METIERS[slug]
    path = f"/metiers/{slug}.html"
    crumbs = [("Accueil", "/"), ("Exemples métiers", "/exemples-metiers.html"),
              (m["label"], path)]
    faq = m["faq"]
    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": m["title"],
            "description": m["desc"],
            "inLanguage": "fr-FR",
            "mainEntityOfPage": DOMAIN + path,
            "datePublished": TODAY,
            "dateModified": TODAY,
            "author": org_schema(),
            "publisher": org_schema(),
        },
        breadcrumbs_schema(crumbs, path),
        faq_schema(faq),
    ]
    tags = "".join(f"<span>{t}</span>" for t in m["tags"])
    searches = "".join(f"<li>{s}</li>" for s in m["searches"])
    sections = "".join(f"<li>{s}</li>" for s in m["sections"])
    html = head(m["title"], m["desc"], path, schemas, og_type="article") + header() + f"""
<main id="main">
  <section class="page-hero metier-hero">
    <div class="orb orb-a" aria-hidden="true"></div>
    <div class="orb orb-b" aria-hidden="true"></div>
    <div class="wrap hero-grid">
      <div>
        {breadcrumbs(crumbs)}
        <p class="eyebrow">Exemple métier</p>
        <h1>{m['h1']}</h1>
        <p class="lead">{m['lead']}</p>
        <a class="primary-btn" href="#generateur">Générer une page {m['default_metier']} + ville <span class="btn-arrow">→</span></a>
      </div>
      <div class="note-card">
        <h2>Objectif de la page</h2>
        <p>{m['objectif']}</p>
        <div class="query-tags">{tags}</div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap split align-start">
      <article class="prose">
        <p class="eyebrow">Problème concret</p>
        <h2>{m['why_h2']}</h2>
        <p>{m['why_p']}</p>
        <h2>Recherches simples à viser</h2>
        <p>Ces formulations ne sont pas réservées aux experts. Elles correspondent à des demandes concrètes que les prospects peuvent taper avant d’appeler.</p>
        <ul>{searches}</ul>
        <h2>Sections à prévoir sur la page</h2>
        <ul>{sections}</ul>
        <h2>Exemple de titre clair</h2>
        <blockquote>{m['blockquote']}</blockquote>
        <h2>CTA recommandé</h2>
        <p>{m['cta_p']}</p>
      </article>
      <aside class="sticky-side">
        <div class="side-card">
          <h3>Plan rapide</h3>
          <ol>
            <li>Métier + ville dans le titre.</li>
            <li>Prestation principale visible.</li>
            <li>Photos ou preuves locales.</li>
            <li>Questions fréquentes.</li>
            <li>Bouton de contact clair.</li>
          </ol>
          <a class="primary-btn" href="#generateur" style="margin-top:14px;width:100%">Créer mon plan <span class="btn-arrow">→</span></a>
        </div>
      </aside>
    </div>
  </section>
{tool_section(m['default_metier'], m['default_service'])}{faq_section(faq, f"Questions fréquentes : page {m['default_metier']} + ville")}{soft_cta()}{related_links(exclude=slug)}
</main>""" + footer()
    write(f"metiers/{slug}.html", html)


def article_shell(path, title, desc, h1, lead_text, eyebrow, body, crumb_label,
                  default_metier="", default_service=""):
    crumbs = [("Accueil", "/"), (crumb_label, path)]
    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "inLanguage": "fr-FR",
            "mainEntityOfPage": DOMAIN + path,
            "datePublished": TODAY,
            "dateModified": TODAY,
            "author": org_schema(),
            "publisher": org_schema(),
        },
        breadcrumbs_schema(crumbs, path),
    ]
    html = head(title, desc, path, schemas, og_type="article") + header() + f"""
<main id="main">
  <section class="page-hero compact-hero">
    <div class="orb orb-a" aria-hidden="true"></div>
    <div class="wrap article-wrap">
      {breadcrumbs(crumbs)}
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead_text}</p>
    </div>
  </section>
{body}
{tool_section(default_metier, default_service)}{soft_cta()}{related_links()}
</main>""" + footer()
    return html


def build_articles():
    # 1. Pourquoi votre site ne ramène pas de clients
    body = """
  <article class="section article-wrap prose">
    <h2>1. Votre site parle de vous, pas du besoin du client</h2>
    <p>Un visiteur veut savoir si vous intervenez dans sa ville, pour son problème précis, avec des preuves et un moyen simple de vous contacter.</p>
    <h2>2. Vous avez une seule page pour toutes vos prestations</h2>
    <p>Un pisciniste qui fait construction, rénovation, entretien et dépannage ne devrait pas tout cacher dans une seule page. Chaque prestation importante peut mériter une page claire.</p>
    <h2>3. Votre zone d’intervention est trop vague</h2>
    <p>“Nous intervenons dans tout le département” est moins parlant qu’une page dédiée à une ville prioritaire, avec les communes proches et les types de demandes traitées.</p>
    <h2>4. Vous n’avez pas de questions fréquentes</h2>
    <p>Prix, délais, garanties, déplacement, devis, entretien : ces questions rassurent le prospect et donnent de la matière utile à Google.</p>
    <h2>5. Le site n’invite pas clairement à l’action</h2>
    <p>Chaque page doit guider vers un appel, un formulaire, une demande de devis ou une prise de rendez-vous.</p>
    <blockquote>La bonne question n’est pas “mon site est-il joli ?” mais “ma page répond-elle à la recherche d’un client de ma ville ?”</blockquote>
  </article>"""
    write("pourquoi-votre-site-ne-ramene-pas-de-clients.html", article_shell(
        "/pourquoi-votre-site-ne-ramene-pas-de-clients.html",
        "Pourquoi mon site ne m’apporte pas de clients ? | Pages locales utiles",
        "Votre site est en ligne mais ne génère pas de demandes ? Découvrez les causes fréquentes et comment créer des pages simples qui répondent aux recherches locales.",
        "Pourquoi votre site ne vous apporte pas de clients ?",
        "Souvent, le problème n’est pas que le site est “moche”. Le problème est qu’il ne répond pas clairement aux recherches des personnes qui cherchent votre métier dans votre ville.",
        "Diagnostic simple", body, "Pourquoi ça bloque"))

    # 2. Rédiger avec Wisewand
    body = f"""
  <section class="section">
    <div class="wrap split">
      <div>
        <p class="eyebrow">Quand l’utiliser ?</p>
        <h2>Du plan généré à la page publiée.</h2>
        <p>Le générateur vous donne la structure. Wisewand peut ensuite vous aider à rédiger une page complète, à retravailler le texte et à publier plus régulièrement : une page par ville prioritaire, une page par service, des articles qui répondent aux questions clients.</p>
        <a class="primary-btn" href="{WISEWAND_URL}" target="_blank" rel="sponsored noopener">Découvrir Wisewand <span class="btn-arrow">→</span></a>
      </div>
      <div class="note-card">
        <h2>Cas d’usage</h2>
        <ul class="plain-list">
          <li>Créer une page par ville prioritaire.</li>
          <li>Rédiger une page service claire.</li>
          <li>Publier des articles qui répondent aux questions clients.</li>
          <li>Garder un ton simple, local et commercial.</li>
        </ul>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap cards-3">
      <article class="info-card"><span>1</span><h3>Générez le plan</h3><p>Utilisez le générateur pour obtenir le titre, les sections et les questions fréquentes.</p></article>
      <article class="info-card"><span>2</span><h3>Rédigez la page</h3><p>Collez le plan dans Wisewand et demandez un texte clair, utile, local et orienté contact.</p></article>
      <article class="info-card"><span>3</span><h3>Publiez et améliorez</h3><p>Ajoutez vos photos, vos preuves, vos réalisations et un bouton de contact visible.</p></article>
    </div>
  </section>"""
    write("rediger-page-avec-wisewand.html", article_shell(
        "/rediger-page-avec-wisewand.html",
        "Rédiger une page métier + ville avec Wisewand | Plan prêt à publier",
        "Utilisez le générateur pour obtenir un plan de page locale, puis transformez-le en page complète avec Wisewand.",
        "Transformez votre plan “métier + ville” en page prête à publier.",
        "Le générateur vous donne la structure. Wisewand peut ensuite vous aider à rédiger une page complète, à retravailler le texte et à publier plus régulièrement.",
        "Rédaction de contenu", body, "Rédiger la page"))

    # 3. Où héberger son site pro
    body = f"""
  <section class="section">
    <div class="wrap split">
      <div>
        <p class="eyebrow">Conseil pratique</p>
        <h2>Commencez simple.</h2>
        <p>Pour un artisan ou une TPE, un hébergement mutualisé sérieux suffit souvent pour un site vitrine, quelques pages locales et un blog. Le plus important est de publier régulièrement des pages utiles et de garder le site rapide sur mobile.</p>
        <ul class="plain-list">
          <li>Installation WordPress simple.</li>
          <li>Certificat HTTPS inclus.</li>
          <li>Support accessible.</li>
          <li>Sauvegardes et performance correctes.</li>
          <li>Possibilité de gérer plusieurs sites.</li>
        </ul>
      </div>
      <div class="pricing-card">
        <span>Affiliation hébergement</span>
        <h3>Publier votre site avec Hostinger</h3>
        <p>Lien partenaire intégré. À utiliser naturellement après le générateur, quand vous voulez mettre votre page en ligne.</p>
        <a class="secondary-btn" href="{HOSTINGER_URL}" target="_blank" rel="sponsored noopener" style="margin-top:14px">Accéder à Hostinger <span class="btn-arrow">→</span></a>
      </div>
    </div>
  </section>"""
    write("ou-heberger-son-site-pro.html", article_shell(
        "/ou-heberger-son-site-pro.html",
        "Où héberger son site pro ? | Site vitrine rapide pour artisan et TPE",
        "Conseils simples pour choisir un hébergement de site professionnel, rapide et fiable pour publier un site vitrine ou WordPress.",
        "Où héberger un site pro simple, rapide et fiable ?",
        "Une page locale utile ne sert à rien si le site est lent, introuvable ou compliqué à gérer. Pour un site vitrine ou WordPress, l’objectif est d’avoir une base claire, stable et facile à maintenir.",
        "Mise en ligne", body, "Héberger son site pro"))


def legal_shell(path, title, desc, h1, lead_text, body):
    crumbs = [("Accueil", "/"), (h1, path)]
    html = head(title, desc, path, [breadcrumbs_schema(crumbs, path)]) + header() + f"""
<main id="main">
  <section class="page-hero compact-hero">
    <div class="wrap article-wrap">
      {breadcrumbs(crumbs)}
      <h1>{h1}</h1>
      <p class="lead">{lead_text}</p>
    </div>
  </section>
  <article class="section article-wrap prose">{body}
  </article>
</main>""" + footer()
    return html


def build_legal():
    body = """
    <h2>Éditeur</h2>
    <p>Nom / raison sociale : à compléter<br>Adresse : à compléter<br>Email : à compléter<br>SIRET : à compléter</p>
    <h2>Hébergement</h2>
    <p>À compléter selon votre hébergeur.</p>
    <h2>Affiliation</h2>
    <p>Certains liens présents sur ce site sont des liens affiliés. Si vous cliquez sur ces liens et souscrivez à une solution, l’éditeur du site peut percevoir une commission, sans coût supplémentaire pour vous.</p>
    <h2>Responsabilité</h2>
    <p>Les informations sont fournies à titre indicatif et ne garantissent aucun résultat de positionnement, de trafic ou de chiffre d’affaires.</p>"""
    write("mentions-legales.html", legal_shell(
        "/mentions-legales.html",
        "Mentions légales | Métier + Ville",
        "Mentions légales du site Générateur de page métier + ville.",
        "Mentions légales",
        "À compléter avant publication avec vos informations d’éditeur.", body))

    body = """
    <h2>Données collectées</h2>
    <p>Le formulaire peut collecter votre prénom, votre adresse email, le métier, la ville et le plan généré afin de vous envoyer le résultat demandé.</p>
    <h2>Finalité</h2>
    <p>Les données sont utilisées pour répondre à votre demande et, si vous l’acceptez, vous envoyer des conseils liés à la visibilité locale.</p>
    <h2>Conservation</h2>
    <p>Les données sont conservées le temps nécessaire au suivi de la demande. Vous pouvez demander leur suppression à tout moment.</p>
    <h2>Affiliation</h2>
    <p>Le site contient des liens affiliés vers Wisewand et Hostinger.</p>"""
    write("politique-confidentialite.html", legal_shell(
        "/politique-confidentialite.html",
        "Politique de confidentialité | Métier + Ville",
        "Politique de confidentialité du site Générateur de page métier + ville.",
        "Politique de confidentialité",
        "À adapter selon les outils utilisés pour l’emailing, les statistiques et les formulaires.", body))


def build_404():
    html = head("Page introuvable | Métier + Ville",
                "Cette page n’existe pas ou plus. Retrouvez le générateur de page métier + ville et les exemples par métier.",
                "/404.html", noindex=True) + header() + f"""
<main id="main">
  <section class="page-hero compact-hero">
    <div class="orb orb-a" aria-hidden="true"></div>
    <div class="wrap article-wrap">
      <p class="eyebrow">Erreur 404</p>
      <h1>Cette page n’existe pas (ou plus).</h1>
      <p class="lead">Pas de panique : le générateur, lui, fonctionne toujours. Reprenez depuis l’accueil ou explorez les exemples métiers.</p>
      <div class="hero-actions">
        <a class="primary-btn" href="/">Retour à l’accueil <span class="btn-arrow">→</span></a>
        <a class="ghost-btn" href="/exemples-metiers.html">Voir les exemples métiers</a>
      </div>
    </div>
  </section>
{related_links()}
</main>""" + footer()
    write("404.html", html)


def build_sitemap():
    def url(loc, priority, changefreq):
        return (f"  <url><loc>{DOMAIN}{loc}</loc><lastmod>{TODAY}</lastmod>"
                f"<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>")
    lines = [url("/", "1.0", "weekly"),
             url("/exemples-metiers.html", "0.9", "weekly"),
             url("/pourquoi-votre-site-ne-ramene-pas-de-clients.html", "0.7", "monthly"),
             url("/rediger-page-avec-wisewand.html", "0.7", "monthly"),
             url("/ou-heberger-son-site-pro.html", "0.7", "monthly")]
    lines += [url(f"/metiers/{s}.html", "0.8", "monthly") for s in ORDER]
    lines += [url("/mentions-legales.html", "0.3", "yearly"),
              url("/politique-confidentialite.html", "0.3", "yearly")]
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(lines) + "\n</urlset>\n")
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("  sitemap.xml")


def build_og_image():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("  (Pillow absent : og-cover.png non régénérée)")
        return
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#0f2620")
    dr = ImageDraw.Draw(img)
    # dégradé vertical vert profond -> vert brand
    top, bottom = (15, 38, 32), (18, 64, 58)
    for y in range(H):
        t = y / H
        dr.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    # halos décoratifs
    halo = Image.new("L", (W, H), 0)
    hd = ImageDraw.Draw(halo)
    hd.ellipse((820, -220, 1420, 380), fill=70)
    hd.ellipse((-260, 320, 340, 920), fill=55)
    img.paste(Image.new("RGB", (W, H), "#d8914b"), (0, 0), halo)

    def font(size, bold=True):
        for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
                  else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
        return ImageFont.load_default()

    # badge marque
    dr.rounded_rectangle((80, 80, 156, 156), radius=22, fill="#f3dcc2")
    dr.text((118, 118), "MV", font=font(34), fill="#0f2620", anchor="mm")
    dr.text((176, 118), "Métier + Ville", font=font(30), fill="#eef8f3", anchor="lm")
    dr.text((80, 250), "Créez votre page", font=font(76), fill="#ffffff")
    dr.text((80, 345), "« métier + ville »", font=font(76), fill="#e8b47c")
    dr.text((80, 470), "Générateur gratuit — soyez trouvé par les clients", font=font(33, False), fill="#bdd3cc")
    dr.text((80, 515), "de votre commune sur Google.", font=font(33, False), fill="#bdd3cc")
    img.save(os.path.join(SITE, "assets", "og-cover.png"), optimize=True)
    print("  assets/og-cover.png")


def write(rel, html):
    p = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html + "\n")
    print(f"  {rel}")


if __name__ == "__main__":
    print("Génération du site :")
    build_home()
    build_exemples()
    for slug in ORDER:
        build_metier(slug)
    build_articles()
    build_legal()
    build_404()
    build_sitemap()
    build_og_image()
    print("Terminé.")
