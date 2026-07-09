# -*- coding: utf-8 -*-
"""Contenus éditoriaux Localto — textes adressés au professionnel (persona),
optimisés SEO. Les données factuelles (listes, mots-clés, FAQ) proviennent
de data.json ; ce fichier porte la réécriture rédactionnelle."""

SITE = {
    "name": "Localto",
    "url": "https://localto.fr",
    "tagline": "Le guide SEO local des indépendants, artisans et professions libérales",
    "footer_about": (
        "Localto vous aide à créer un site internet qui inspire confiance, à "
        "remonter sur Google dans votre ville et à attirer des clients locaux "
        "— avec des guides concrets, pensés pour votre métier."
    ),
    "og_image": "/localto-dashboard.png",
}

# ---------------------------------------------------------------------------
# Métiers : contenus adressés directement au professionnel
# ---------------------------------------------------------------------------

METIERS = {
    "plombier": {
        "nom": "plombier",
        "pluriel": "plombiers",
        "de": "de plombier",
        "vocatif": "Plombiers & chauffagistes",
        "categorie": "Artisan",
        "icon": "wrench",
        "card_home": (
            "Vos clients vous cherchent dans l'urgence et appellent le premier "
            "plombier crédible près de chez eux. Soyez celui-là."
        ),
        "crea_title": "Création site internet plombier : guide et plan d'action",
        "crea_desc": (
            "Créez un site de plombier qui fait sonner le téléphone : structure, "
            "pages indispensables, mots-clés locaux, erreurs à éviter et plan en 7 jours."
        ),
        "crea_h1": "Un site internet de plombier qui fait sonner le téléphone",
        "crea_intro": (
            "Fuite d'eau, chauffe-eau en panne, salle de bain à rénover : vos "
            "futurs clients vous cherchent sur Google au moment exact où ils ont "
            "besoin de vous. Votre site doit les rassurer en quelques secondes — "
            "numéro visible, zones desservies, avis récents — et transformer "
            "leur urgence en appel. Voici comment le construire, page par page."
        ),
        "vis_title": "Visibilité Google plombier : attirer des clients locaux",
        "vis_desc": (
            "Remontez sur Google dans votre ville : mots-clés d'urgence et de travaux, "
            "avis clients, fiche Google Business et plan d'action SEO en 7 jours pour plombier."
        ),
        "vis_h1": "Visibilité Google pour plombier : devenez l'artisan qu'on appelle en premier",
        "vis_intro": (
            "Quand un habitant de votre ville tape « plombier urgence », c'est "
            "votre nom qui doit sortir. Votre visibilité Google se construit avec "
            "des pages services locales, des avis récents et des contenus qui "
            "répondent aux vraies situations : urgence bien sûr, mais aussi "
            "chauffe-eau, recherche de fuite et rénovation — les chantiers les "
            "plus rentables."
        ),
    },
    "electricien": {
        "nom": "électricien",
        "pluriel": "électriciens",
        "de": "d'électricien",
        "vocatif": "Électriciens",
        "categorie": "Artisan",
        "icon": "bolt",
        "card_home": (
            "Vos clients redoutent les pannes dangereuses et les devis flous. "
            "Montrez-leur que vous sécurisez, expliquez et intervenez vite."
        ),
        "crea_title": "Création site internet électricien : guide et plan d'action",
        "crea_desc": (
            "Créez un site d'électricien qui rassure et convertit : structure, pages "
            "indispensables, mots-clés locaux, erreurs à éviter et plan d'action en 7 jours."
        ),
        "crea_h1": "Un site internet d'électricien qui inspire confiance et déclenche l'appel",
        "crea_intro": (
            "Vos clients ont deux peurs : la panne dangereuse et le devis flou. "
            "Votre site doit rendre la sécurité compréhensible — expliquer ce que "
            "vous vérifiez, ce que vous remplacez et ce que le client reçoit à la "
            "fin : une installation fonctionnelle, conforme et documentée. C'est "
            "ce qui vous distingue des annuaires impersonnels."
        ),
        "vis_title": "Visibilité Google électricien : attirer des clients locaux",
        "vis_desc": (
            "Soyez trouvé par vos clients : mots-clés locaux (mise aux normes, dépannage, "
            "borne de recharge), avis, fiche Google Business et plan SEO en 7 jours pour électricien."
        ),
        "vis_h1": "Visibilité Google pour électricien : soyez trouvé avant vos concurrents",
        "vis_intro": (
            "Mise aux normes, tableau électrique, borne de recharge : chaque "
            "recherche cache un chantier. Pour capter ces demandes dans votre "
            "secteur, combinez pages locales, contenus de prévention et preuves "
            "de savoir-faire. Ce guide vous montre exactement quoi publier, et "
            "dans quel ordre."
        ),
    },
    "coiffeur": {
        "nom": "coiffeur",
        "pluriel": "coiffeurs",
        "de": "de coiffeur",
        "vocatif": "Coiffeurs & salons",
        "categorie": "Artisan",
        "icon": "scissors",
        "card_home": (
            "Vos clients veulent voir le style du salon, les prestations, les prix "
            "et les créneaux avant de réserver. Donnez-leur envie de pousser la porte."
        ),
        "crea_title": "Création site internet coiffeur : guide et plan d'action",
        "crea_desc": (
            "Créez un site de coiffeur qui remplit votre agenda : réservation facile, pages "
            "prestations, mots-clés locaux, erreurs à éviter et plan d'action en 7 jours."
        ),
        "crea_h1": "Un site internet de coiffeur qui remplit votre agenda",
        "crea_intro": (
            "Avant de réserver, vos clients veulent trois choses : voir le style "
            "de votre salon, connaître vos prestations et vos prix, et réserver "
            "en deux clics. Votre site doit faciliter la réservation et mettre en "
            "avant vos prestations phares — chacune mérite sa page, plutôt qu'une "
            "simple liste tarifaire."
        ),
        "vis_title": "Visibilité Google coiffeur : attirer des clients en salon",
        "vis_desc": (
            "Faites remonter votre salon sur Google : mots-clés par prestation, photos, "
            "avis clients, fiche Google Business et plan d'action SEO en 7 jours pour coiffeur."
        ),
        "vis_h1": "Visibilité Google pour coiffeur : le salon que l'on trouve (et que l'on choisit)",
        "vis_intro": (
            "« Balayage », « coupe homme », « coiffure mariage » : vos futurs "
            "clients cherchent une prestation précise, près de chez eux. Pour "
            "ressortir sur Google, travaillez chaque requête locale avec une page "
            "dédiée, des photos récentes et des avis qui parlent de votre salon. "
            "Voici la méthode, étape par étape."
        ),
    },
    "avocat": {
        "nom": "avocat",
        "pluriel": "avocats",
        "de": "d'avocat",
        "vocatif": "Avocats & cabinets",
        "categorie": "Profession libérale",
        "icon": "scale",
        "card_home": (
            "Vos futurs clients hésitent à vous contacter : ils ne savent pas si "
            "leur problème relève de votre domaine. Levez ce doute dès la première page."
        ),
        "crea_title": "Création site internet avocat : guide et plan d'action",
        "crea_desc": (
            "Créez un site d'avocat crédible et efficace : structure par domaine de droit, "
            "page honoraires, mots-clés, déontologie et plan d'action en 7 jours."
        ),
        "crea_h1": "Un site internet d'avocat qui transforme les visiteurs en rendez-vous",
        "crea_intro": (
            "Votre futur client hésite : il ne sait pas si son problème relève de "
            "votre domaine, ni comment se passe un premier échange. Votre site "
            "doit conjuguer crédibilité, clarté et mesure : aider le visiteur à "
            "se reconnaître dans une situation juridique — sans transformer la "
            "page en consultation — et l'amener naturellement vers la prise de "
            "rendez-vous."
        ),
        "vis_title": "Visibilité Google avocat : développer votre clientèle locale",
        "vis_desc": (
            "Développez la visibilité Google de votre cabinet : pages par domaine de droit, "
            "contenus pédagogiques, avis, fiche Google Business et plan SEO en 7 jours."
        ),
        "vis_h1": "Visibilité Google pour avocat : le cabinet que l'on trouve en premier",
        "vis_intro": (
            "Les recherches « avocat + ville + domaine » amènent des clients bien "
            "plus qualifiés qu'une requête générique. Votre visibilité repose sur "
            "trois piliers : des pages par domaine de droit, des contenus "
            "pédagogiques conformes à la déontologie et une présence locale "
            "cohérente. Ce guide vous donne le plan complet."
        ),
    },
    "architecte": {
        "nom": "architecte",
        "pluriel": "architectes",
        "de": "d'architecte",
        "vocatif": "Architectes",
        "categorie": "Profession libérale",
        "icon": "compass",
        "card_home": (
            "Vos clients choisissent un architecte dont le style, la méthode et "
            "l'expérience locale collent à leur projet. Montrez les trois."
        ),
        "crea_title": "Création site internet architecte : guide et plan d'action",
        "crea_desc": (
            "Créez un site d'architecte qui attire les bons projets : portfolio structuré, "
            "pages typologies, mots-clés locaux et plan d'action en 7 jours."
        ),
        "crea_h1": "Un site internet d'architecte qui attire les bons projets",
        "crea_intro": (
            "Vos maîtres d'ouvrage ne choisissent pas qu'un style : ils choisissent "
            "une méthode et une expérience locale. Votre site doit rendre votre "
            "façon de travailler aussi visible que vos réalisations : chaque "
            "projet doit raconter le besoin, les contraintes, la mission confiée "
            "et la solution retenue."
        ),
        "vis_title": "Visibilité Google architecte : attirer des projets qualifiés",
        "vis_desc": (
            "Gagnez en visibilité sur Google : pages par typologie de projet, requêtes permis "
            "et extension, réalisations détaillées et plan d'action SEO en 7 jours pour architecte."
        ),
        "vis_h1": "Visibilité Google pour architecte : captez les projets de votre région",
        "vis_intro": (
            "Les recherches autour du permis de construire et de l'extension sont "
            "parmi les plus qualifiées de votre métier. Votre visibilité Google "
            "se construit sur trois leviers : des pages par typologie de projet, "
            "des pages locales et des réalisations détaillées qui prouvent votre "
            "expérience du terrain."
        ),
    },
    "expert-comptable": {
        "nom": "expert-comptable",
        "pluriel": "experts-comptables",
        "de": "d'expert-comptable",
        "vocatif": "Experts-comptables",
        "categorie": "Profession libérale",
        "icon": "calculator",
        "card_home": (
            "Vos clients cherchent un cabinet disponible, clair sur ses offres et "
            "qui comprend leur secteur — sans jargon comptable."
        ),
        "crea_title": "Création site internet expert-comptable : guide complet",
        "crea_desc": (
            "Créez un site d'expert-comptable qui attire les bons clients : pages missions, "
            "offres claires, mots-clés, erreurs à éviter et plan d'action en 7 jours."
        ),
        "crea_h1": "Un site internet d'expert-comptable qui attire les bons dossiers",
        "crea_intro": (
            "Vos prospects veulent savoir une chose : votre cabinet est-il fait "
            "pour eux ? Votre site doit clarifier pour qui vous travaillez, ce que "
            "comprend l'accompagnement et comment se déroulent les premières "
            "semaines. Plus c'est concret, plus les demandes entrantes sont "
            "qualifiées."
        ),
        "vis_title": "Visibilité Google expert-comptable : gagner des clients",
        "vis_desc": (
            "Développez la visibilité Google de votre cabinet comptable : pages missions, "
            "contenus créateurs d'entreprise, avis et plan d'action SEO en 7 jours."
        ),
        "vis_h1": "Visibilité Google pour expert-comptable : le cabinet que l'on recommande",
        "vis_intro": (
            "Création d'entreprise, comptabilité, paie : chaque mission mérite sa "
            "page et ses mots-clés. Votre visibilité progresse avec des contenus "
            "qui répondent à des décisions concrètes de vos clients — pas "
            "seulement des commentaires d'actualité fiscale. Voici le plan pour y "
            "arriver."
        ),
    },
    "osteopathe": {
        "nom": "ostéopathe",
        "pluriel": "ostéopathes",
        "de": "d'ostéopathe",
        "vocatif": "Ostéopathes",
        "categorie": "Santé",
        "icon": "hand",
        "card_home": (
            "Vos patients veulent savoir si vous recevez leur profil, comment se "
            "déroule la séance et si le cabinet est facile d'accès."
        ),
        "crea_title": "Création site internet ostéopathe : guide et plan d'action",
        "crea_desc": (
            "Créez un site d'ostéopathe qui remplit votre agenda : prise de rendez-vous, "
            "motifs de consultation, mots-clés locaux et plan d'action en 7 jours."
        ),
        "crea_h1": "Un site internet d'ostéopathe qui remplit votre agenda de consultations",
        "crea_intro": (
            "Avant de prendre rendez-vous, vos patients se posent des questions "
            "très pratiques : recevez-vous leur profil ? Comment se déroule une "
            "séance ? Le cabinet est-il facile d'accès ? Votre site doit lever "
            "ces freins — pratiques et émotionnels — et rendre la prise de "
            "rendez-vous évidente."
        ),
        "vis_title": "Visibilité Google ostéopathe : attirer de nouveaux patients",
        "vis_desc": (
            "Soyez visible sur Google dans votre ville : motifs de consultation, publics "
            "accompagnés, avis patients et plan d'action SEO en 7 jours pour ostéopathe."
        ),
        "vis_h1": "Visibilité Google pour ostéopathe : le cabinet que l'on trouve près de chez soi",
        "vis_intro": (
            "Vos patients cherchent « ostéopathe + ville », mais aussi un motif : "
            "mal de dos, nourrisson, sportif, femme enceinte. Associez votre "
            "métier, votre ville, les motifs de consultation et les publics que "
            "vous accompagnez — avec des contenus prudents et informatifs, "
            "conformes à votre cadre d'exercice."
        ),
    },
    "coach-sportif": {
        "nom": "coach sportif",
        "pluriel": "coachs sportifs",
        "de": "de coach sportif",
        "vocatif": "Coachs sportifs",
        "categorie": "Indépendant",
        "icon": "dumbbell",
        "card_home": (
            "Vos prospects veulent un coach proche, crédible, qui s'adapte à leur "
            "niveau — sans jugement ni promesse irréaliste."
        ),
        "crea_title": "Création site internet coach sportif : guide complet",
        "crea_desc": (
            "Créez un site de coach sportif qui convertit : pages par objectif, formats, "
            "mots-clés locaux, erreurs à éviter et plan d'action en 7 jours."
        ),
        "crea_h1": "Un site internet de coach sportif qui transforme les curieux en clients",
        "crea_intro": (
            "Vos prospects n'achètent pas une silhouette : ils achètent une "
            "méthode et un cadre. Votre site doit montrer votre façon "
            "d'accompagner — l'écoute, la progression, les formats disponibles "
            "près de chez eux — et prouver que vous vous adaptez à leur niveau, "
            "sans jugement."
        ),
        "vis_title": "Visibilité Google coach sportif : trouver des clients locaux",
        "vis_desc": (
            "Développez votre visibilité Google : pages par objectif et par zone, coaching à "
            "domicile, avis clients et plan d'action SEO en 7 jours pour coach sportif."
        ),
        "vis_h1": "Visibilité Google pour coach sportif : soyez le coach que l'on trouve",
        "vis_intro": (
            "« Coach sportif à domicile », « perte de poids », « reprise du "
            "sport » : chaque objectif attire une intention différente et mérite "
            "sa propre page. En travaillant vos pages par objectif et par zone, "
            "vous captez des demandes qualifiées au lieu d'attendre le "
            "bouche-à-oreille."
        ),
    },
    "photographe": {
        "nom": "photographe",
        "pluriel": "photographes",
        "de": "de photographe",
        "vocatif": "Photographes",
        "categorie": "Indépendant",
        "icon": "camera",
        "card_home": (
            "Vos clients vous choisissent sur la confiance visuelle : style, "
            "prestations et lieux couverts doivent sauter aux yeux."
        ),
        "crea_title": "Création site internet photographe : guide et plan d'action",
        "crea_desc": (
            "Créez un site de photographe rapide et vendeur : portfolio par prestation, "
            "mots-clés locaux, erreurs à éviter et plan d'action en 7 jours."
        ),
        "crea_h1": "Un site internet de photographe qui vend votre regard",
        "crea_intro": (
            "Vos clients vous choisissent en quelques secondes, sur la confiance "
            "visuelle. S'ils ne voient pas immédiatement votre style, vos "
            "prestations et les lieux que vous couvrez, ils passent au portfolio "
            "suivant. Votre site doit montrer votre regard sans sacrifier la "
            "vitesse — chaque prestation mérite sa page, avec portfolio ciblé, "
            "déroulé et livrables."
        ),
        "vis_title": "Visibilité Google photographe : attirer des séances locales",
        "vis_desc": (
            "Faites remonter votre portfolio sur Google : galeries contextualisées, mots-clés "
            "par séance et par lieu, avis clients et plan d'action SEO en 7 jours."
        ),
        "vis_h1": "Visibilité Google pour photographe : un portfolio que Google comprend",
        "vis_intro": (
            "De belles images ne suffisent pas : Google ne « voit » pas vos "
            "photos. Votre visibilité progresse quand chaque galerie est "
            "contextualisée — type de séance, lieu, intention du client, "
            "mots-clés locaux. Ce guide vous montre comment transformer votre "
            "portfolio en aimant à demandes."
        ),
    },
}

ORDER = [
    "plombier", "electricien", "coiffeur", "avocat", "architecte",
    "expert-comptable", "osteopathe", "coach-sportif", "photographe",
]

# ---------------------------------------------------------------------------
# Textes des sections (gabarits adressés au persona)
# ---------------------------------------------------------------------------

SECTIONS = {
    "probleme_eyebrow": "Ce que vivent vos clients",
    "probleme_h2": "Ce que vos clients cherchent avant de vous contacter",
    "probleme_intro": (
        "Votre priorité : répondre à l'intention dominante de vos clients — "
        "<strong>{intention}</strong>. C'est elle qui doit guider vos pages, "
        "vos mots-clés et les preuves que vous affichez."
    ),
    "exemples_label": "Des situations bien réelles :",
    "structure_eyebrow": "Architecture du site",
    "structure_h2": "La structure de site qui transforme vos visiteurs en clients",
    "structure_intro": (
        "Ne concentrez pas tout sur une seule page : chaque intention de "
        "recherche mérite la sienne. Cette architecture crée un chemin clair "
        "entre la découverte, la confiance et la prise de contact."
    ),
    "pages_eyebrow": "Vos pages prioritaires",
    "pages_h2": "Les pages indispensables de votre site {de_metier}",
    "pages_intro": (
        "Commencez par ces pages : ce sont elles que vos clients attendent, et "
        "elles couvrent les recherches Google les plus fréquentes de votre métier."
    ),
    "keywords_eyebrow": "Référencement",
    "keywords_h2_crea": "Les mots-clés qui amènent vos clients jusqu'à vous",
    "keywords_h2_vis": "Les mots-clés à viser pour gagner en visibilité",
    "keywords_intro": (
        "Prenez ces requêtes comme point de départ, puis adaptez-les à votre "
        "ville, votre quartier, vos spécialités et aux mots que vos clients "
        "emploient vraiment."
    ),
    "articles_eyebrow": "Contenu qui attire",
    "articles_h2": "Des idées d'articles pour attirer un trafic qualifié",
    "articles_intro": (
        "Un article n'est utile que s'il répond à une question précise que vos "
        "clients se posent avant de vous contacter — puis les guide vers votre "
        "page service ou votre page locale la plus proche."
    ),
    "ressources_title": "Passez de l'idée à la publication",
    "ressources_p1": (
        "Pour rédiger plus vite vos pages et vos articles sans y passer vos "
        "soirées, <a class=\"link\" href=\"https://wisewand.ai/?fpr=wisewand-seo\" rel=\"sponsored noopener\" "
        "target=\"_blank\">Wisewand</a> vous aide à produire des contenus utiles, "
        "adaptés à votre métier et à votre ville."
    ),
    "ressources_p2": (
        "Et pour que vos pages se chargent vite — un critère que Google et vos "
        "clients regardent — hébergez votre site chez un "
        "<a class=\"link\" href=\"https://www.hostg.xyz/SHJit\" rel=\"sponsored noopener\" "
        "target=\"_blank\">hébergeur web rapide et fiable</a>."
    ),
    "erreurs_eyebrow": "À éviter absolument",
    "erreurs_h2": "Les erreurs qui vous coûtent des clients",
    "erreurs_intro": (
        "Ces erreurs reviennent sur la majorité des sites {de_pluriel} — et "
        "chacune fait fuir des clients prêts à vous contacter."
    ),
    "preuves_eyebrow": "Réassurance",
    "preuves_h2": "Les preuves qui font pencher la balance en votre faveur",
    "preuves_intro": (
        "Le SEO local ne se joue pas qu'avec des mots-clés. Ces preuves visibles "
        "aident vos visiteurs à vous choisir, vous — et renforcent la cohérence "
        "entre votre site, votre fiche Google et vos avis."
    ),
    "plan_eyebrow": "Votre plan d'action",
    "plan_h2": "7 jours pour faire décoller votre présence en ligne",
    "plan_intro": (
        "Une action par jour, une semaine pour changer la donne. Suivez ce plan "
        "dans l'ordre : chaque étape prépare la suivante."
    ),
    "faq_eyebrow": "On vous répond",
    "faq_h2": "Vos questions les plus fréquentes",
    "related_eyebrow": "Continuez votre lecture",
    "related_h2": "Pour aller plus loin",
}

# ---------------------------------------------------------------------------
# Page d'accueil
# ---------------------------------------------------------------------------

HOME = {
    "title": "Localto : un site internet qui attire des clients locaux",
    "description": (
        "Créez un site internet qui inspire confiance et remontez sur Google dans "
        "votre ville. Guides SEO concrets par métier pour artisans, professions "
        "libérales et indépendants."
    ),
    "hero_eyebrow": "Artisans · Professions libérales · Indépendants",
    "hero_h1_before": "Vos clients vous cherchent sur Google.",
    "hero_h1_accent": "Faites-vous trouver.",
    "hero_intro": (
        "Localto vous donne un plan clair pour créer un site internet qui "
        "inspire confiance et remonter dans les recherches locales : les bonnes "
        "pages, les bons mots-clés, les bonnes preuves — adaptés à votre métier, "
        "sans jargon."
    ),
    "hero_cta1": "Trouver mon guide métier",
    "hero_cta2": "Découvrir la méthode",
    "hero_points": ["9 métiers couverts", "Plan d'action en 7 jours", "100 % concret, 0 jargon"],
    "metiers_eyebrow": "Guides par métier",
    "metiers_h2": "Choisissez votre métier, suivez le guide",
    "metiers_intro": (
        "Chaque métier a ses urgences, ses preuves de confiance et ses "
        "recherches Google. Un plombier doit capter l'urgence, un avocat lever "
        "les doutes, un photographe montrer son style sans ralentir son site. "
        "Vos guides sont construits pour votre réalité — pas pour un « artisan "
        "moyen » qui n'existe pas."
    ),
    "features_eyebrow": "Ce que vous obtenez",
    "features_h2": "Dans chaque guide, tout ce qu'il faut pour passer à l'action",
    "features": [
        {
            "icon": "layout",
            "title": "La structure de votre site",
            "text": "Les pages à créer en priorité et comment les organiser pour transformer vos visiteurs en clients.",
        },
        {
            "icon": "search",
            "title": "Vos mots-clés locaux",
            "text": "Les requêtes que vos clients tapent vraiment sur Google, prêtes à adapter à votre ville et vos spécialités.",
        },
        {
            "icon": "shield",
            "title": "Les preuves qui rassurent",
            "text": "Avis, photos, certifications : ce qui fait pencher la balance en votre faveur au moment du choix.",
        },
        {
            "icon": "calendar",
            "title": "Un plan d'action en 7 jours",
            "text": "Une action concrète par jour pour améliorer votre présence en ligne — sans y passer vos week-ends.",
        },
    ],
    "steps_eyebrow": "La méthode",
    "steps_h2": "Trois étapes pour devenir visible près de chez vous",
    "steps": [
        {
            "title": "Ouvrez le guide de votre métier",
            "text": "Structure de site, pages indispensables, mots-clés : tout est déjà adapté à votre activité et aux attentes de vos clients.",
        },
        {
            "title": "Appliquez le plan d'action 7 jours",
            "text": "Chaque jour, une action simple et concrète : vos pages, vos avis, votre fiche Google Business Profile.",
        },
        {
            "title": "Récoltez des demandes locales",
            "text": "Un site clair + des contenus utiles + des preuves visibles : c'est ce qui fait sonner le téléphone durablement.",
        },
    ],
    "cta_h2": "Prêt à attirer plus de clients locaux ?",
    "cta_text": (
        "Choisissez votre métier et suivez un plan concret : votre site, vos "
        "mots-clés et votre fiche Google alignés en 7 jours."
    ),
    "cta_btn": "Choisir mon métier",
}

# ---------------------------------------------------------------------------
# Pages hub / pilier
# ---------------------------------------------------------------------------

HUBS = {
    "creation": {
        "path": "/creation-site-internet-metier/",
        "nav": "Création de site par métier",
        "title": "Création de site internet par métier : le guide complet",
        "description": (
            "Créez un site internet adapté à votre métier : structure, pages "
            "indispensables, contenus SEO et preuves locales pour attirer des "
            "clients près de chez vous."
        ),
        "badge": "Guide complet",
        "h1": "Créez un site internet pensé pour votre métier — et pour vos clients",
        "intro": (
            "Un bon site professionnel ne commence pas par un design : il "
            "commence par les questions de vos clients, les preuves dont ils ont "
            "besoin et les pages que Google peut comprendre. Choisissez votre "
            "métier et suivez un plan adapté à votre réalité."
        ),
        "method_eyebrow": "Les fondations",
        "method_h2": "La structure qui fonctionne pour un site local",
        "method_intro": (
            "La base solide est toujours la même : une page d'accueil claire, des "
            "pages services précises, une page zone d'intervention ou cabinet, "
            "des preuves concrètes et des contenus de conseil. La différence se "
            "joue ensuite sur votre métier : urgence, rendez-vous, portfolio, "
            "honoraires, devis ou preuves réglementaires."
        ),
        "method_points": [
            "Une page d'accueil qui dit en 5 secondes qui vous êtes, où vous intervenez et comment vous contacter.",
            "Une page par service ou prestation — jamais tout sur une seule page.",
            "Une page zone d'intervention ou accès au cabinet, avec les communes réellement couvertes.",
            "Des preuves visibles : avis, photos de réalisations, certifications, garanties.",
            "Des contenus de conseil qui répondent aux questions posées avant la prise de contact.",
        ],
        "grid_eyebrow": "Votre métier",
        "grid_h2": "Choisissez votre guide de création de site",
        "metier_link": "creation",
    },
    "visibilite": {
        "path": "/visibilite-google-metier/",
        "nav": "Visibilité Google par métier",
        "title": "Visibilité Google par métier : attirer plus de clients locaux",
        "description": (
            "Améliorez votre visibilité sur Google : pages ciblées, fiche Google "
            "Business, avis clients et contenus locaux — la méthode adaptée à "
            "votre métier."
        ),
        "badge": "Guide complet",
        "h1": "Améliorez votre visibilité Google quand vos clients sont près de chez vous",
        "intro": (
            "Vos clients ne cherchent pas seulement un métier : ils cherchent une "
            "solution proche, crédible, disponible et adaptée à leur situation. "
            "Votre présence sur Google doit refléter cette intention — voici "
            "comment, métier par métier."
        ),
        "method_eyebrow": "Les 4 piliers",
        "method_h2": "Ce qui fait vraiment remonter votre activité sur Google",
        "method_intro": (
            "La visibilité locale repose sur quatre piliers : des pages ciblées "
            "sur les demandes rentables, une fiche Google Business Profile "
            "cohérente, des avis clients précis et des contenus qui répondent aux "
            "questions posées avant la prise de contact."
        ),
        "method_points": [
            "Des pages construites sur les demandes les plus rentables de votre activité.",
            "Une fiche Google Business Profile complète et cohérente avec votre site.",
            "Des avis clients qui mentionnent le service rendu et votre ville.",
            "Des contenus qui répondent aux questions que vos clients se posent avant d'appeler.",
        ],
        "grid_eyebrow": "Votre métier",
        "grid_h2": "Choisissez votre guide de visibilité Google",
        "metier_link": "visibilite",
    },
}

PILIER = {
    "path": "/seo-local-metier/",
    "nav": "SEO local par métier",
    "title": "SEO local par métier : la méthode pour être visible",
    "description": (
        "La méthode SEO local complète : fiche Google Business, pages locales, "
        "avis clients, contenus longue traîne — adaptée à votre métier pour "
        "attirer des clients de proximité."
    ),
    "badge": "La méthode",
    "h1": "SEO local : reliez votre expertise aux recherches de proximité",
    "intro": (
        "Le SEO local consiste à prouver à Google — et surtout à vos clients — "
        "que vous êtes le bon professionnel pour une demande précise, dans une "
        "zone précise, avec des preuves précises. Voici la méthode complète, puis "
        "son application à votre métier."
    ),
    "method_eyebrow": "Pas à pas",
    "method_h2": "La méthode SEO local, dans l'ordre",
    "method_intro": (
        "Commencez par votre fiche Google Business Profile, puis alignez votre "
        "site : mêmes services, mêmes zones, mêmes preuves. Créez ensuite des "
        "pages pour les intentions fortes, et enfin des contenus longue traîne "
        "qui répondent aux questions réelles de vos clients."
    ),
    "method_points": [
        "Nom, adresse, téléphone et horaires identiques partout — site, fiche Google, annuaires.",
        "Des pages services construites sur vos demandes les plus rentables.",
        "Des avis clients qui mentionnent le service rendu et votre ville.",
        "Des photos, réalisations, cas clients ou preuves professionnelles visibles.",
        "Un maillage clair entre votre page d'accueil, vos pages services et vos articles.",
    ],
    "grid_eyebrow": "Applications métier",
    "grid_h2": "Le SEO local appliqué à votre métier",
    "grid_intro": (
        "Les preuves attendues par vos clients ne sont pas les mêmes selon votre "
        "activité. Choisissez votre métier pour une méthode vraiment adaptée."
    ),
}
