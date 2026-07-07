
const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.main-nav');
if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });
}

const progress = document.createElement('div');
progress.className = 'progress-bar';
document.body.prepend(progress);

const floatingCta = document.createElement('a');
floatingCta.className = 'floating-cta';
floatingCta.href = 'outil-seo-pisciniste.html';
floatingCta.textContent = 'Voir l’outil SEO';
document.body.appendChild(floatingCta);

function updateProgress(){
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = docHeight > 0 ? Math.min(100, (scrollTop / docHeight) * 100) : 0;
  progress.style.width = ratio + '%';
  floatingCta.classList.toggle('show', scrollTop > 620);
}
window.addEventListener('scroll', updateProgress, { passive: true });
updateProgress();

const revealTargets = document.querySelectorAll('.card,.note-card,.score-card,.tool-panel,.mini-card,.table-wrap,.timeline article,.idea-grid article,.steps>div,.prompt-box,.prose,.pool-dashboard,.pipeline-grid article,.calculator');
revealTargets.forEach((el, index) => {
  el.classList.add('reveal');
  el.style.transitionDelay = `${Math.min(index % 4, 3) * 70}ms`;
});
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealTargets.forEach(el => observer.observe(el));
} else {
  revealTargets.forEach(el => el.classList.add('is-visible'));
}

const generateButton = document.querySelector('#generateIdeas');
if (generateButton) {
  const output = document.querySelector('#ideasOutput');
  const zoneInput = document.querySelector('#zone');
  const serviceInput = document.querySelector('#service');
  const seasonInput = document.querySelector('#season');

  generateButton.addEventListener('click', () => {
    const zone = zoneInput?.value.trim() || 'votre zone';
    const service = serviceInput?.value || 'construction piscine';
    const season = seasonInput?.value || 'printemps';
    const maps = {
      'construction piscine': ['prix piscine 8x4', 'piscine coque ou béton', 'terrassement piscine', 'piscine petit jardin', 'déclaration préalable'],
      'piscine coque': ['prix piscine coque', 'avantages piscine coque', 'pose piscine coque', 'terrain difficile', 'délai de chantier'],
      'rénovation piscine': ['changer liner', 'rénover margelles', 'fuite piscine', 'membrane armée', 'moderniser filtration'],
      'entretien piscine': ['remise en route', 'hivernage', 'eau verte', 'contrat entretien', 'traitement au sel'],
      'dépannage piscine': ['pompe en panne', 'filtre pression élevée', 'robot bloqué', 'fuite local technique', 'eau trouble urgente'],
      'spa et bien-être': ['installation spa', 'spa extérieur', 'entretien spa', 'spa ou piscine', 'abri spa'],
      'sécurité piscine': ['alarme piscine', 'volet roulant', 'barrière piscine', 'abri piscine', 'normes sécurité']
    };
    const selected = maps[service] || maps['construction piscine'];
    const ideas = [
      `Combien coûte une ${service} à ${zone} en ${season} ?`,
      `${selected[0]} : les facteurs qui font varier le devis à ${zone}`,
      `${service} à ${zone} : comment choisir le bon pisciniste ?`,
      `Les erreurs à éviter avant de lancer une ${service} à ${zone}`,
      `${selected[1]} : avantages, limites et profils adaptés`,
      `Projet piscine à ${zone} : quelles étapes avant le premier devis ?`,
      `${selected[2]} : ce qu’un particulier doit vérifier avant de signer`,
      `${service} : quels délais prévoir en ${season} ?`,
      `${selected[3]} : dans quels cas demander une visite technique ?`,
      `${selected[4]} : questions fréquentes avant une demande de devis`,
      `Pourquoi demander un devis local pour une ${service} à ${zone} ?`,
      `Checklist ${service} : les informations à préparer avant d’appeler un pisciniste`
    ];
    output.innerHTML = '<ul>' + ideas.map(i => `<li>${i}</li>`).join('') + '</ul>';
    output.scrollIntoView({behavior:'smooth', block:'nearest'});
  });
}

const calcButton = document.querySelector('#calcLeads');
if (calcButton) {
  calcButton.addEventListener('click', () => {
    const avg = Number(document.querySelector('#avgProject')?.value || 0);
    const leads = Number(document.querySelector('#leadsMonth')?.value || 0);
    const rate = Number(document.querySelector('#closeRate')?.value || 0) / 100;
    const potential = Math.round(avg * leads * rate);
    const formatted = potential.toLocaleString('fr-FR', { style:'currency', currency:'EUR', maximumFractionDigits:0 });
    document.querySelector('#calcResult').innerHTML = `Avec ces hypothèses, ${leads} demandes/mois peuvent représenter environ <strong>${formatted}</strong> de chiffre d’affaires potentiel mensuel.`;
  });
}
