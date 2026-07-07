const WISEWAND_URL = "https://wisewand.ai/?fpr=wisewand-seo";
const HOSTINGER_URL = "https://www.hostg.xyz/SHJit";

function cap(str) { return (str || '').trim().replace(/^./, c => c.toUpperCase()); }
function slug(str) { return (str || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,''); }
function q(sel) { return document.querySelector(sel); }
function esc(str) { const d = document.createElement('div'); d.textContent = str; return d.innerHTML; }

const REDUCED_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ------------------------------------------------------------ générateur */
function generateLocalPage() {
  const metier = (q('#metier')?.value || 'artisan').trim();
  const ville = (q('#ville')?.value || 'votre ville').trim();
  const service = (q('#service')?.value || 'prestation principale').trim();
  const title = `${cap(metier)} à ${cap(ville)} : ${service} et devis personnalisé`;
  const url = `/${slug(metier)}-${slug(ville)}/`;
  const meta = `${cap(metier)} à ${cap(ville)} pour ${service}. Découvrez les prestations, la zone d’intervention, les étapes, les réponses aux questions fréquentes et demandez un devis.`;
  const searches = [
    `${metier} ${ville}`,
    `devis ${metier} ${ville}`,
    `${service} ${ville}`,
    `${metier} près de moi`,
    `entreprise ${metier} ${ville}`
  ];
  const sections = [
    `Pourquoi faire appel à un ${metier} à ${ville} ?`,
    `Nos prestations pour ${service}`,
    `Zone d’intervention autour de ${ville}`,
    `Exemples de demandes fréquentes`,
    `Comment se déroule une demande de devis ?`,
    `Questions fréquentes avant de choisir un ${metier}`,
    `Demander un devis ou être rappelé`
  ];
  const faqs = [
    `Intervenez-vous uniquement à ${ville} ?`,
    `Combien coûte une prestation de ${service} ?`,
    `Sous quel délai peut-on obtenir un devis ?`,
    `Quelles informations donner pour recevoir une réponse précise ?`
  ];
  const planText = `Titre : ${title}
URL conseillée : ${url}
Meta description : ${meta}
Recherches simples : ${searches.join(', ')}
Sections : ${sections.join(' | ')}
FAQ : ${faqs.join(' | ')}`;

  const html = `
    <span class="label">Plan généré</span>
    <strong>${esc(title)}</strong>
    <p><b>URL conseillée :</b> ${esc(url)}</p>
    <p><b>Description Google :</b> ${esc(meta)}</p>
    <h3>Recherches simples à viser</h3>
    <ul>${searches.map(s => `<li>${esc(s)}</li>`).join('')}</ul>
    <h3>Structure de page recommandée</h3>
    <ul>${sections.map(s => `<li>${esc(s)}</li>`).join('')}</ul>
    <h3>Questions fréquentes à ajouter</h3>
    <ul>${faqs.map(s => `<li>${esc(s)}</li>`).join('')}</ul>
    <h3>Texte d’introduction possible</h3>
    <p>Vous cherchez un ${esc(metier)} à ${esc(ville)} pour ${esc(service)} ? Cette page présente les prestations, les étapes, les informations utiles avant devis et les moyens de contact pour obtenir une réponse claire.</p>
    <div class="result-actions">
      <button class="secondary-btn copy-btn" type="button" id="copyPlanBtn">Copier le plan</button>
      <a class="primary-btn" href="${WISEWAND_URL}" rel="sponsored noopener" target="_blank">Rédiger cette page avec Wisewand <span class="btn-arrow">→</span></a>
      <a class="secondary-btn" href="${HOSTINGER_URL}" rel="sponsored noopener" target="_blank">Publier mon site avec Hostinger</a>
    </div>`;
  const panel = q('#resultPanel');
  if (panel) {
    panel.innerHTML = html;
    panel.classList.remove('pop');
    void panel.offsetWidth; // relance l'animation
    panel.classList.add('pop');
    panel.scrollIntoView({ behavior: REDUCED_MOTION ? 'auto' : 'smooth', block: 'nearest' });
  }
  const copyBtn = q('#copyPlanBtn');
  if (copyBtn) copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(planText);
      copyBtn.textContent = '✓ Plan copié';
      setTimeout(() => { copyBtn.textContent = 'Copier le plan'; }, 2200);
    } catch (e) { copyBtn.textContent = 'Copie impossible'; }
  });
  const hidden = q('#generatedPlanInput');
  if (hidden) hidden.value = planText;
  try { localStorage.setItem('lastGeneratedPlan', planText); } catch (e) {}
}

function initDefaults() {
  const card = document.querySelector('.tool-card');
  if (!card) return;
  const metier = card.getAttribute('data-default-metier');
  const service = card.getAttribute('data-default-service');
  if (metier && q('#metier')) q('#metier').value = metier;
  if (service && q('#service')) q('#service').value = service;
}

/* ------------------------------------------------------------- formulaire */
function initLeadForm() {
  const form = q('#leadForm');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!q('#generatedPlanInput')?.value) generateLocalPage();
    const status = q('#formStatus');
    if (status) status.textContent = 'Envoi en cours...';
    try {
      const res = await fetch(form.getAttribute('action'), { method: 'POST', body: new FormData(form), headers: { 'X-Requested-With': 'fetch' } });
      const data = await res.json();
      if (data.ok) {
        if (status) status.textContent = 'C’est bon : le plan a été enregistré. Vérifiez votre boîte email si l’envoi est activé côté serveur.';
        form.reset();
      } else { throw new Error(data.error || 'Erreur inconnue'); }
    } catch (err) {
      if (status) status.textContent = 'Le formulaire est prêt, mais l’envoi serveur doit être activé sur votre hébergement. Votre plan reste affiché ci-dessus.';
    }
  });
}

/* ------------------------------------------------------------- navigation */
function initMenu() {
  const btn = document.querySelector('.menu-btn');
  const nav = document.querySelector('.nav');
  if (!btn || !nav) return;
  btn.setAttribute('aria-expanded', 'false');
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('.navlinks a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
  }));
}

function initTopbar() {
  const bar = document.querySelector('.topbar');
  if (!bar) return;
  const onScroll = () => bar.classList.toggle('scrolled', window.scrollY > 12);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

function initFloatingCta() {
  const cta = document.querySelector('.floating-cta');
  if (!cta) return;
  const target = document.getElementById('generateur');
  const onScroll = () => {
    let show = window.scrollY > 500;
    if (show && target) {
      const r = target.getBoundingClientRect();
      // masque le bouton quand le générateur est déjà à l'écran
      if (r.top < window.innerHeight && r.bottom > 0) show = false;
    }
    cta.classList.toggle('show', show);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

/* -------------------------------------------------------------- animations */
function initReveal() {
  const groups = ['.cards-3', '.trade-grid', '.solution-cards', '.hero-stats', '.keyword-box'];
  groups.forEach(sel => document.querySelectorAll(sel).forEach(group => {
    Array.from(group.children).forEach((el, i) => {
      el.classList.add('reveal');
      el.style.setProperty('--d', `${Math.min(i * .08, .5)}s`);
    });
  }));
  document.querySelectorAll('.note-card,.pricing-card,.faq-item,.browser-card,.prose,.side-card').forEach(el => el.classList.add('reveal'));
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
  }), { threshold: .1, rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
}

function initTypewriter() {
  const line = document.querySelector('.search-line[data-queries]');
  if (!line) return;
  let queries;
  try { queries = JSON.parse(line.getAttribute('data-queries')); } catch (e) { return; }
  if (!Array.isArray(queries) || !queries.length) return;
  const textEl = document.createElement('span');
  line.textContent = '';
  line.appendChild(textEl);
  if (REDUCED_MOTION) { textEl.textContent = queries[0]; return; }
  const cursor = document.createElement('span');
  cursor.className = 'type-cursor';
  line.appendChild(cursor);
  let qi = 0, ci = 0, deleting = false;
  (function tick() {
    const current = queries[qi];
    if (!deleting) {
      ci++;
      textEl.textContent = current.slice(0, ci);
      if (ci === current.length) { deleting = true; return setTimeout(tick, 2100); }
      return setTimeout(tick, 46 + Math.random() * 54);
    }
    ci--;
    textEl.textContent = current.slice(0, ci);
    if (ci === 0) { deleting = false; qi = (qi + 1) % queries.length; return setTimeout(tick, 420); }
    setTimeout(tick, 22);
  })();
}

function initCounters() {
  const els = document.querySelectorAll('[data-count]');
  if (!els.length) return;
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (!e.isIntersecting) return;
    io.unobserve(e.target);
    const el = e.target;
    const end = parseInt(el.getAttribute('data-count'), 10) || 0;
    const suffix = el.getAttribute('data-suffix') || '';
    if (REDUCED_MOTION) { el.textContent = end + suffix; return; }
    const dur = 1200, start = performance.now();
    (function frame(now) {
      const p = Math.min((now - start) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) requestAnimationFrame(frame);
    })(start);
  }), { threshold: .5 });
  els.forEach(el => io.observe(el));
}

document.addEventListener('DOMContentLoaded', () => {
  initDefaults();
  initLeadForm();
  initMenu();
  initTopbar();
  initFloatingCta();
  initReveal();
  initTypewriter();
  initCounters();
});
