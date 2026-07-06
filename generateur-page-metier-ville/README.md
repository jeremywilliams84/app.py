# Générateur de page “métier + ville”

Site final prêt à charger chez un hébergeur compatible PHP, par exemple Hostinger.

## Positionnement

Promesse visible : aider un artisan, une TPE ou un indépendant à créer une page simple pour être trouvé par des clients dans sa ville.

Le site évite de parler de “SEO” en façade. Il utilise plutôt : clients locaux, demandes de devis, être trouvé sur Google, page métier + ville.

## Génération des pages

Les pages HTML sont générées par `../build_site.py` à partir de `../metiers_data.json`.
Pour modifier le header, le footer, le générateur, un contenu métier ou le balisage SEO :

1. Éditez `build_site.py` (structure) ou `metiers_data.json` (contenus par métier).
2. Lancez `python3 build_site.py`.
3. Rechargez le dossier chez votre hébergeur.

Ne modifiez pas les fichiers HTML à la main : ils seraient écrasés à la prochaine génération.

## Optimisations intégrées

- Design premium : typographie Fraunces/Inter, animations d’apparition, effet machine à écrire, compteurs, menu mobile accessible, bouton flottant intelligent.
- SEO on-page : titres et descriptions uniques et calibrés, canonical, Open Graph + Twitter Cards avec image `assets/og-cover.png`, fil d’Ariane visible.
- Données structurées : WebSite, WebApplication, Organization, Article, BreadcrumbList et FAQPage (60 questions/réponses uniques réparties sur les 15 pages métiers + 5 sur l’accueil).
- Maillage interne : bandeau métiers, liens croisés entre pages métiers, footer avec les 15 pages, breadcrumbs.
- Technique : `.htaccess` (HTTPS forcé, redirection `index.html` → `/`, compression, cache navigateur, en-têtes de sécurité), page 404 personnalisée, `sitemap.xml` avec `lastmod` et priorités réalistes, script chargé en `defer`.

## Liens affiliés intégrés

- Wisewand : https://wisewand.ai/?fpr=wisewand-seo
- Hostinger : https://www.hostg.xyz/SHJit

## Capture email

Le formulaire envoie les leads vers `lead.php`. Sur un hébergement PHP, les emails sont enregistrés dans `/leads/leads.csv`. Le dossier `/leads/` contient un `.htaccess` pour éviter l’accès direct. Vérifiez la protection selon votre hébergeur.

## À modifier avant publication

1. Remplacer le domaine dans `build_site.py` (constante `DOMAIN`) si vous utilisez un autre nom de domaine, puis régénérer.
2. Compléter les mentions légales.
3. Optionnel : décommenter la fonction `mail()` dans `lead.php` pour recevoir une notification email.
4. Ajouter vos propres exemples, photos et articles pour renforcer l’autorité.
5. Après mise en ligne : déclarer `sitemap.xml` dans Google Search Console et demander l’indexation de la page d’accueil.

## Pages incluses

- `index.html` (générateur + FAQ)
- `exemples-metiers.html`
- `metiers/*.html` : 15 pages métiers avec FAQ dédiées (pisciniste, couvreur, plombier, électricien, chauffagiste, paysagiste, menuisier, carreleur, maçon, serrurier, conciergerie Airbnb, sophrologue, secrétaire indépendante, wedding planner, photographe mariage)
- `pourquoi-votre-site-ne-ramene-pas-de-clients.html`, `rediger-page-avec-wisewand.html`, `ou-heberger-son-site-pro.html`
- `mentions-legales.html`, `politique-confidentialite.html`, `404.html`
- `lead.php`, `sitemap.xml`, `robots.txt`, `.htaccess`

## Requêtes simples visées

- comment être visible sur Google quand on est artisan
- comment avoir plus de clients dans sa ville
- créer une page métier ville
- que mettre sur une page artisan + ville
- pourquoi mon site internet ne m’apporte pas de clients
- comment recevoir plus de demandes de devis
- site vitrine artisan qui rapporte des clients
- apparaître sur Google dans sa commune
