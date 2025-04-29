import streamlit as st
import whois
import re
import datetime
import requests
import urllib.parse

# Fonction pour extraire l'extension
def get_extension(domain):
    match = re.search(r'\.(\w+)$', domain)
    return f".{match.group(1)}" if match else ""

# Fonction pour estimer si le domaine est brandable
def is_brandable(domain):
    domain = domain.replace('-', '').replace('.', '')
    return len(domain) <= 12 and domain.isalpha()

# Fonction pour calculer la longueur
def domain_length(domain):
    return len(domain.replace('-', '').replace('.', ''))

# Fonction pour détecter chiffres/tirets
def has_no_numbers_hyphens(domain):
    return 1 if not re.search(r'[-\d]', domain) else 0

# Fonction pour récupérer l'âge du domaine
def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            today = datetime.datetime.now()
            age = today.year - creation_date.year - ((today.month, today.day) < (creation_date.month, creation_date.day))
            return max(age, 0)
        else:
            return 0
    except:
        return 0

# Fonction pour obtenir un volume de recherche approximatif via API (placeholder ici)
def get_search_volume(keyword):
    try:
        encoded_keyword = urllib.parse.quote(keyword)
        response = requests.get(f"https://api.publicapis.io/keywordvolume/{encoded_keyword}")  # Exemple fictif
        if response.status_code == 200:
            data = response.json()
            return data.get('volume', 100)
        else:
            return 100
    except:
        return 100

# Fonction pour simuler Domain Authority (simple bonus pour démo)
def get_domain_authority(domain):
    return 10  # Valeur fixe pour démo (entre 10 et 30 selon évaluations simplistes)

# Fonction pour estimer l'intention du mot-clé
def is_transactional_keyword(keyword):
    transactional_keywords = ['acheter', 'devis', 'urgent', 'commande', 'prix', 'solution', 'comparatif']
    return any(kw in keyword.lower() for kw in transactional_keywords)

# Fonction pour estimer la valeur
def estimate_value(extension, length, brandable, no_numbers, age, volume, authority, transactional):
    value = 0
    value += 40 if extension == ".com" else 20 if extension == ".fr" else 10
    value += 20 if length <= 12 else 0
    value += 30 if brandable else 0
    value += 10 if no_numbers else 0
    value += (volume / 500) * 10
    value += (authority / 5) * 10
    value += 30 if transactional else 0
    value += (age) * 5
    return round(value, 2)

# Streamlit Interface
st.title("Domain Value Estimator 📈 (Version Avancée)")

# Input
domain = st.text_input("Entrez le nom du domaine (ex: exemple.com)")

if domain:
    extension = get_extension(domain)
    length = domain_length(domain)
    brandable = is_brandable(domain)
    no_numbers = has_no_numbers_hyphens(domain)
    age = get_domain_age(domain)
    keyword = domain.split('.')[0]
    volume = get_search_volume(keyword)
    authority = get_domain_authority(domain)
    transactional = is_transactional_keyword(keyword)

    estimated_value = estimate_value(extension, length, brandable, no_numbers, age, volume, authority, transactional)

    st.subheader("🔢 Metrics Analysés")
    st.write(f"**Extension:** {extension}")
    st.write(f"**Longueur:** {length}")
    st.write(f"**Brandable:** {'Oui' if brandable else 'Non'}")
    st.write(f"**Pas de chiffres/tirets:** {'Oui' if no_numbers else 'Non'}")
    st.write(f"**\u00c2ge du domaine:** {age} ans")
    st.write(f"**Volume de recherche estimé:** {volume} recherches/mois")
    st.write(f"**Autorité de domaine estimée:** {authority}")
    st.write(f"**Intention Transactionnelle:** {'Oui' if transactional else 'Non'}")

    st.subheader("📈 Estimation Finale de la Valeur")
    st.success(f"Valeur estimée: {estimated_value} €")

    if estimated_value >= 300:
        st.balloons()
        st.info("Ce domaine a un potentiel de revente supérieur à 300 €. GO!")
    else:
        st.warning("Potentiel plus faible pour revente rapide.")
