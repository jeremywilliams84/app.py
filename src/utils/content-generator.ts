/**
 * Générateur de contenu modulaire anti-duplicate
 * Utilise un seed stable basé sur le slug pour garantir des variantes cohérentes
 */

import servicesData from '../../data/services.json';
import departementsData from '../../data/departements.json';
import villesData from '../../data/villes.json';
import variantesData from '../../data/variantes.json';

export interface Service {
  id: string;
  slug: string;
  name: string;
  namePlural: string;
  metaTitle: string;
  metaDescription: string;
  schemaType: string;
  serviceType: string;
  keywords: string[];
  priceRange: string;
  openingHours: string;
  areaServed: string;
  icon: string;
}

export interface Departement {
  id: string;
  code: string;
  slug: string;
  name: string;
  nameFull: string;
  region: string;
  population: number;
  prefix: string;
  article: string;
}

export interface Ville {
  id: string;
  slug: string;
  name: string;
  nameFull: string;
  departementSlug: string;
  departementCode: string;
  codePostal: string;
  population: number;
  latitude: number;
  longitude: number;
  prefix: string;
  quartiers: string[];
  communesProches: string[];
  reperes: string[];
  transports: string[];
  caracteristiques: string[];
}

export interface FAQ {
  question: string;
  answers: string[];
}

export interface ServiceVariantes {
  intros: string[];
  sections_services: string[];
  sections_zone: string[];
  sections_tarifs: string[];
  faqs: FAQ[];
  ctas: string[];
}

// Fonction de hash simple pour générer un seed numérique à partir d'un string
function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

// Générateur pseudo-aléatoire avec seed (Mulberry32)
function seededRandom(seed: number): () => number {
  return function() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

// Sélectionne un élément d'un tableau en fonction du seed
function selectVariant<T>(array: T[], seed: number, offset: number = 0): T {
  const random = seededRandom(seed + offset);
  const index = Math.floor(random() * array.length);
  return array[index];
}

// Remplace les variables de template dans le contenu
function replaceVariables(
  content: string,
  ville: Ville,
  departement: Departement,
  service: Service
): string {
  return content
    .replace(/{ville}/g, ville.name)
    .replace(/{villeFull}/g, ville.nameFull)
    .replace(/{prefix}/g, ville.prefix)
    .replace(/{departement}/g, departement.name)
    .replace(/{departementFull}/g, departement.nameFull)
    .replace(/{departementCode}/g, departement.code)
    .replace(/{region}/g, departement.region)
    .replace(/{codePostal}/g, ville.codePostal)
    .replace(/{quartiers}/g, ville.quartiers.join(', '))
    .replace(/{communes_proches}/g, ville.communesProches.join(', '))
    .replace(/{reperes}/g, ville.reperes.join(', '))
    .replace(/{transports}/g, ville.transports.join(', '))
    .replace(/{caracteristiques}/g, ville.caracteristiques.join(', '))
    .replace(/{service}/g, service.name)
    .replace(/{serviceLower}/g, service.name.toLowerCase())
    .replace(/{serviceSlug}/g, service.slug);
}

// Génère le contenu complet pour une page locale
export function generatePageContent(
  serviceSlug: string,
  departementSlug: string,
  villeSlug: string
) {
  const service = (servicesData as Service[]).find(s => s.slug === serviceSlug);
  const departement = (departementsData as Departement[]).find(d => d.slug === departementSlug);
  const ville = (villesData as Ville[]).find(v => v.slug === villeSlug && v.departementSlug === departementSlug);

  if (!service || !departement || !ville) {
    return null;
  }

  const variantes = (variantesData as Record<string, ServiceVariantes>)[serviceSlug];
  if (!variantes) {
    return null;
  }

  // Seed unique basé sur le slug complet
  const slug = `${serviceSlug}-${departementSlug}-${villeSlug}`;
  const seed = hashString(slug);

  // Sélection des variantes avec offsets différents pour chaque section
  const intro = replaceVariables(
    selectVariant(variantes.intros, seed, 0),
    ville, departement, service
  );

  const sectionServices = replaceVariables(
    selectVariant(variantes.sections_services, seed, 100),
    ville, departement, service
  );

  const sectionZone = replaceVariables(
    selectVariant(variantes.sections_zone, seed, 200),
    ville, departement, service
  );

  const sectionTarifs = replaceVariables(
    selectVariant(variantes.sections_tarifs, seed, 300),
    ville, departement, service
  );

  const cta = replaceVariables(
    selectVariant(variantes.ctas, seed, 400),
    ville, departement, service
  );

  // Sélection de 4-6 FAQs avec leurs réponses variées
  const faqCount = 4 + (seed % 3); // 4, 5 ou 6 FAQs
  const shuffledFaqs = [...variantes.faqs].sort((a, b) => {
    const random = seededRandom(seed + 500);
    return random() - 0.5;
  }).slice(0, faqCount);

  const faqs = shuffledFaqs.map((faq, index) => ({
    question: replaceVariables(faq.question, ville, departement, service),
    answer: replaceVariables(
      selectVariant(faq.answers, seed, 600 + index),
      ville, departement, service
    )
  }));

  // Métadonnées
  const metaTitle = replaceVariables(service.metaTitle, ville, departement, service);
  const metaDescription = replaceVariables(service.metaDescription, ville, departement, service);

  // H1 unique avec variante
  const h1Variants = [
    `${service.name} ${ville.prefix} ${ville.name} (${departement.code})`,
    `${service.name} professionnel ${ville.prefix} ${ville.name}`,
    `Votre ${service.name.toLowerCase()} ${ville.prefix} ${ville.name} - ${departement.name}`,
    `${service.name} qualifié ${ville.prefix} ${ville.name} (${ville.codePostal})`,
    `${service.name} de confiance ${ville.prefix} ${ville.name}`
  ];
  const h1 = selectVariant(h1Variants, seed, 700);

  return {
    service,
    departement,
    ville,
    slug,
    seed,
    metaTitle,
    metaDescription,
    h1,
    intro,
    sectionServices,
    sectionZone,
    sectionTarifs,
    cta,
    faqs
  };
}

// Récupère les données brutes
export function getServices(): Service[] {
  return servicesData as Service[];
}

export function getDepartements(): Departement[] {
  return departementsData as Departement[];
}

export function getVilles(): Ville[] {
  return villesData as Ville[];
}

export function getVillesByDepartement(departementSlug: string): Ville[] {
  return (villesData as Ville[]).filter(v => v.departementSlug === departementSlug);
}

export function getService(slug: string): Service | undefined {
  return (servicesData as Service[]).find(s => s.slug === slug);
}

export function getDepartement(slug: string): Departement | undefined {
  return (departementsData as Departement[]).find(d => d.slug === slug);
}

export function getVille(slug: string, departementSlug?: string): Ville | undefined {
  if (departementSlug) {
    return (villesData as Ville[]).find(v => v.slug === slug && v.departementSlug === departementSlug);
  }
  return (villesData as Ville[]).find(v => v.slug === slug);
}

// Récupère les villes proches pour le maillage interne
export function getNearbyVilles(ville: Ville, limit: number = 4): Ville[] {
  const allVilles = villesData as Ville[];

  // D'abord les villes du même département
  const sameDept = allVilles.filter(v =>
    v.departementSlug === ville.departementSlug && v.slug !== ville.slug
  );

  // Trier par distance géographique
  sameDept.sort((a, b) => {
    const distA = Math.sqrt(
      Math.pow(a.latitude - ville.latitude, 2) +
      Math.pow(a.longitude - ville.longitude, 2)
    );
    const distB = Math.sqrt(
      Math.pow(b.latitude - ville.latitude, 2) +
      Math.pow(b.longitude - ville.longitude, 2)
    );
    return distA - distB;
  });

  return sameDept.slice(0, limit);
}

// Génère tous les chemins possibles pour les pages locales
export function getAllLocalePaths() {
  const services = servicesData as Service[];
  const villes = villesData as Ville[];

  const paths: Array<{
    service: string;
    departement: string;
    ville: string;
  }> = [];

  for (const service of services) {
    for (const ville of villes) {
      paths.push({
        service: service.slug,
        departement: ville.departementSlug,
        ville: ville.slug
      });
    }
  }

  return paths;
}
