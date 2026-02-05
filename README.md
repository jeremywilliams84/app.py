# Local SEO Multi-Niche - Projet Astro

Projet Astro complet pour le SEO local multi-niche (services locaux) avec génération statique (SSG), fort maillage interne et optimisation conversion.

## Caractéristiques

- **Multi-services** : Plombier, Électricien (extensible)
- **Multi-zones** : Départements et villes
- **SEO optimisé** : Title/Meta uniques, Schema.org, Breadcrumbs, Sitemap
- **Anti-duplicate** : Système de variantes par blocs avec seed stable
- **Conversion** : Formulaires, CTA sticky, preuves sociales
- **Performance** : Génération statique (SSG), CSS minimal

## Structure du projet

```
local-seo-multi-niche/
├── astro.config.mjs          # Configuration Astro + Sitemap
├── package.json
├── tsconfig.json
├── data/                     # Données JSON
│   ├── services.json         # Services (plombier, électricien...)
│   ├── departements.json     # Départements couverts
│   ├── villes.json           # Villes avec infos locales
│   └── variantes.json        # Contenu modulaire anti-duplicate
├── public/
│   ├── robots.txt
│   └── favicon.svg
└── src/
    ├── components/           # Composants réutilisables
    │   ├── Breadcrumbs.astro
    │   ├── ContactForm.astro
    │   ├── CTASticky.astro
    │   ├── FAQSection.astro
    │   ├── InternalLinks.astro
    │   ├── LocalBusinessSchema.astro
    │   └── TrustBadges.astro
    ├── layouts/
    │   └── Layout.astro      # Layout principal avec SEO
    ├── pages/
    │   ├── index.astro       # Page d'accueil
    │   ├── 404.astro         # Page 404
    │   ├── contact/
    │   ├── services/
    │   ├── departements/
    │   ├── villes/
    │   ├── mentions-legales/
    │   ├── politique-confidentialite/
    │   └── [service]/
    │       ├── index.astro           # /plombier/
    │       └── [departement]/
    │           ├── index.astro       # /plombier/paris/
    │           └── [ville].astro     # /plombier/paris/paris-15eme/
    ├── styles/
    │   └── global.css        # Styles CSS globaux
    └── utils/
        └── content-generator.ts   # Générateur de contenu avec seed
```

## Installation

```bash
# Cloner le projet
cd local-seo-multi-niche

# Installer les dépendances
npm install

# Lancer en développement
npm run dev

# Build pour production
npm run build

# Prévisualiser le build
npm run preview
```

## Configuration

### 1. Domaine

Modifier `astro.config.mjs` :

```javascript
export default defineConfig({
  site: 'https://votre-domaine.fr',  // Votre domaine
  // ...
});
```

### 2. Informations de contact

Modifier dans les fichiers :
- `src/layouts/Layout.astro` : email, téléphone dans le footer
- `src/pages/contact/index.astro` : coordonnées
- `src/components/LocalBusinessSchema.astro` : téléphone, email

## Ajouter un service

1. **Ajouter les données** dans `data/services.json` :

```json
{
  "id": "serrurier",
  "slug": "serrurier",
  "name": "Serrurier",
  "namePlural": "Serruriers",
  "metaTitle": "Serrurier {ville} ({departement}) - Dépannage 24h/24",
  "metaDescription": "Serrurier à {ville}. Ouverture de porte, changement de serrure. Intervention rapide dans le {departement}.",
  "schemaType": "ProfessionalService",
  "serviceType": "Locksmith",
  "keywords": ["serrurier", "ouverture de porte", "changement serrure", "blindage"],
  "priceRange": "€€",
  "openingHours": "Mo-Su 00:00-24:00",
  "areaServed": "{departement}",
  "icon": "🔐"
}
```

2. **Ajouter les variantes** dans `data/variantes.json` :

```json
{
  "serrurier": {
    "intros": [
      "Vous cherchez un **serrurier {prefix} {ville}** ? ...",
      // 4 autres variantes
    ],
    "sections_services": [...],
    "sections_zone": [...],
    "sections_tarifs": [...],
    "faqs": [...],
    "ctas": [...]
  }
}
```

3. **Relancer le build** : `npm run build`

## Ajouter une ville

Ajouter dans `data/villes.json` :

```json
{
  "id": "marseille-1",
  "slug": "marseille-1er",
  "name": "Marseille 1er",
  "nameFull": "Marseille 1er arrondissement",
  "departementSlug": "bouches-du-rhone",  // Doit exister dans departements.json
  "departementCode": "13",
  "codePostal": "13001",
  "population": 40000,
  "latitude": 43.2965,
  "longitude": 5.3698,
  "prefix": "à",
  "quartiers": ["Vieux-Port", "Le Panier", "Belsunce", "Noailles"],
  "communesProches": ["Marseille 2ème", "Marseille 6ème", "Marseille 7ème"],
  "reperes": ["Vieux-Port", "Notre-Dame de la Garde", "MuCEM"],
  "transports": ["Métro 1", "Métro 2", "Tramway T2"],
  "caracteristiques": ["centre historique", "quartier touristique", "vie nocturne"]
}
```

## Ajouter un département

1. Ajouter dans `data/departements.json` :

```json
{
  "id": "13",
  "code": "13",
  "slug": "bouches-du-rhone",
  "name": "Bouches-du-Rhône",
  "nameFull": "Bouches-du-Rhône (13)",
  "region": "Provence-Alpes-Côte d'Azur",
  "population": 2024000,
  "prefix": "dans les",
  "article": "des"
}
```

2. Ajouter les villes correspondantes dans `data/villes.json`

## Système anti-duplicate

Le système utilise un **seed stable** basé sur le slug de la page pour sélectionner les variantes de contenu.

### Fonctionnement

```typescript
// Dans src/utils/content-generator.ts

// 1. Hash du slug pour créer un seed unique
const seed = hashString(`${serviceSlug}-${departementSlug}-${villeSlug}`);

// 2. Sélection déterministe des variantes
const intro = selectVariant(variantes.intros, seed, 0);        // offset 0
const sectionServices = selectVariant(..., seed, 100);          // offset 100
const sectionZone = selectVariant(..., seed, 200);              // offset 200
// etc.
```

### Avantages

- **Cohérence** : Même contenu généré à chaque build
- **Unicité** : Chaque page a une combinaison unique
- **Maintenabilité** : 5 variantes × 5 sections = 3125 combinaisons possibles

### Ajouter des variantes

Pour augmenter la diversité, ajoutez des variantes dans `data/variantes.json` :

```json
{
  "plombier": {
    "intros": [
      // Variante 1 : ton professionnel
      "Vous recherchez un **plombier professionnel {prefix} {ville}** ? ...",
      // Variante 2 : ton urgence
      "Besoin d'un **plombier {prefix} {ville}** en urgence ? ...",
      // Variante 3 : ton confiance
      "Faites confiance à un **plombier local** {prefix} {ville}...",
      // Variante 4 : ton expertise
      "Notre entreprise de **plomberie {prefix} {ville}**...",
      // Variante 5 : ton proximité
      "Un **plombier proche de chez vous** {prefix} {ville}..."
    ]
  }
}
```

## Variables de template

Variables disponibles dans les variantes :

| Variable | Description | Exemple |
|----------|-------------|---------|
| `{ville}` | Nom de la ville | Paris 15ème |
| `{villeFull}` | Nom complet | Paris 15ème arrondissement |
| `{prefix}` | Préposition | à, dans le |
| `{departement}` | Nom département | Paris |
| `{departementFull}` | Nom + code | Paris (75) |
| `{departementCode}` | Code | 75 |
| `{region}` | Région | Île-de-France |
| `{codePostal}` | Code postal | 75015 |
| `{quartiers}` | Liste quartiers | Grenelle, Javel, ... |
| `{communes_proches}` | Villes proches | Paris 14ème, ... |
| `{reperes}` | Points d'intérêt | Tour Eiffel, ... |
| `{transports}` | Transports | Métro 6, RER C |
| `{service}` | Nom service | Plombier |
| `{serviceLower}` | Nom minuscule | plombier |

## SEO

### Schema.org

Chaque page locale inclut :
- **LocalBusiness/ProfessionalService** : informations entreprise
- **BreadcrumbList** : fil d'Ariane structuré
- **FAQPage** : questions fréquentes

### Sitemap

Généré automatiquement via `@astrojs/sitemap`. Accessible à `/sitemap-index.xml`.

### Canonical

Chaque page a une URL canonique définie automatiquement.

## Déploiement

### Vercel

```bash
npm install -g vercel
vercel
```

### Netlify

```bash
npm run build
# Déployer le dossier dist/
```

### Cloudflare Pages

```bash
npm run build
# Configurer le dossier de sortie : dist
```

## Personnalisation

### Couleurs

Modifier dans `src/styles/global.css` :

```css
:root {
  --color-primary: #2563eb;      /* Couleur principale */
  --color-primary-dark: #1d4ed8;
  --color-secondary: #059669;    /* Couleur secondaire */
  --color-text: #1f2937;
  /* ... */
}
```

### Logo

Remplacer le texte "LocalServices" dans :
- `src/layouts/Layout.astro` (header)

### Formulaire de contact

Le formulaire est préconfiguré pour une soumission côté client. Pour le connecter à un backend :

1. Modifier `src/components/ContactForm.astro`
2. Remplacer la simulation par un appel API réel

```javascript
// Exemple avec fetch
const response = await fetch('/api/contact', {
  method: 'POST',
  body: formData
});
```

## Performance

- **CSS minimal** : ~10KB non compressé
- **Pas de JavaScript framework** : JavaScript vanilla uniquement
- **Images optimisées** : utiliser des formats WebP/AVIF
- **SSG** : pages pré-rendues, 0 temps de serveur

## Support

Pour toute question ou amélioration, ouvrez une issue sur le dépôt.

## Licence

MIT
