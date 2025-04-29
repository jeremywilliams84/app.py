import streamlit as st
import whois
import re
import datetime
import requests

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
            return datetime.datetime.now().year - creation_date.year
        else:
            return 0
    except:
        return 0

# Fonction pour obtenir un volume de recherche approximatif via API (placeholder ici)
def get_search_volume(keyword):
    return 1000  # Supposons un volume moyen pour la démo

# Fonction pour estimer la valeur
def estimate_value(extension, length, brandable, no_numbers, age, volume):
    value = 0
    value += 30 if extension == ".com" else 15 if extension == ".fr" else 0
    value += 20 if length <= 12 else 0
    value += 30 if brandable else 0
    value += 20  # Hypothèse : tendance probable pour cette démo
    value += (volume / 500) * 10
    value += (age) * 5
    value += (no_numbers * 2)
    return round(value, 2)

# Streamlit Interface
st.title("Domain Value Estimator 📈")

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

    estimated_value = estimate_value(extension, length, brandable, no_numbers, age, volume)

    st.subheader("🔢 Metrics")
    st.write(f"**Extension:** {extension}")
    st.write(f"**Longueur:** {length}")
    st.write(f"**Brandable:** {'Oui' if brandable else 'Non'}")
    st.write(f"**Pas de chiffres/tirets:** {'Oui' if no_numbers else 'Non'}")
    st.write(f"**Âge du domaine:** {age} ans")
    st.write(f"**Volume de recherche estimé:** {volume} recherches/mois")

    st.subheader("📈 Estimation de Valeur")
    st.success(f"Valeur estimée: {estimated_value} €")

    if estimated_value >= 300:
        st.balloons()
        st.info("Ce domaine a un potentiel de revente supérieur à 300 €. GO!")
    else:
        st.warning("Potentiel plus faible pour revente rapide.")
