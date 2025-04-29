import streamlit as st
import whois
import re
import datetime
import requests
import pandas as pd
from config import OPENPAGERANK_API_KEY

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

# Fonction pour obtenir Domain Authority via OpenPageRank
def get_openpagerank(domain):
    try:
        url = f"https://openpagerank.com/api/v1.0/getPageRank?domains[]={domain}"
        headers = {"API-OPR": OPENPAGERANK_API_KEY}
        response = requests.get(url, headers=headers)
        data = response.json()
        opr = data['response'][0]['page_rank_integer']
        return opr
    except:
        return 0

# Fonction pour simuler Volume Mot-clé (faute de meilleure API simple gratuite)
def get_search_volume(keyword):
    return 500  # Placeholder pour l'instant

# Fonction pour estimer si mot-clé est transactionnel
def is_transactional_keyword(keyword):
    transactional_keywords = ['acheter', 'devis', 'urgent', 'commande', 'prix', 'solution', 'comparatif']
    return any(kw in keyword.lower() for kw in transactional_keywords)

# Fonction pour estimer la valeur du domaine
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

# --- INTERFACE STREAMLIT ---

st.title("Domain Value Estimator PRO 🚀")

mode = st.radio("Mode d'analyse :", ("1 Domaine", "Batch (plusieurs domaines)"))

if mode == "1 Domaine":
    domain = st.text_input("Entrez le nom du domaine (ex: exemple.com)")
    if domain:
        extension = get_extension(domain)
        length = domain_length(domain)
        brandable = is_brandable(domain)
        no_numbers = has_no_numbers_hyphens(domain)
        age = get_domain_age(domain)
        keyword = domain.split('.')[0]
        volume = get_search_volume(keyword)
        authority = get_openpagerank(domain)
        transactional = is_transactional_keyword(keyword)

        estimated_value = estimate_value(extension, length, brandable, no_numbers, age, volume, authority, transactional)

        st.subheader("📊 Résultats")
        st.write(f"Extension : {extension}")
        st.write(f"Longueur : {length}")
        st.write(f"Brandable : {'Oui' if brandable else 'Non'}")
        st.write(f"Pas de chiffres/tirets : {'Oui' if no_numbers else 'Non'}")
        st.write(f"Âge du domaine : {age} ans")
        st.write(f"Volume mot-clé estimé : {volume}")
        st.write(f"Autorité OpenPageRank : {authority}")
        st.write(f"Transactionnel : {'Oui' if transactional else 'Non'}")
        st.success(f"💰 Valeur estimée : {estimated_value} €")

elif mode == "Batch (plusieurs domaines)":
    uploaded_file = st.file_uploader("Upload ton fichier CSV (1 domaine par ligne)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        results = []
        for domain in df['domaine']:
            extension = get_extension(domain)
            length = domain_length(domain)
            brandable = is_brandable(domain)
            no_numbers = has_no_numbers_hyphens(domain)
            age = get_domain_age(domain)
            keyword = domain.split('.')[0]
            volume = get_search_volume(keyword)
            authority = get_openpagerank(domain)
            transactional = is_transactional_keyword(keyword)

            estimated_value = estimate_value(extension, length, brandable, no_numbers, age, volume, authority, transactional)

            results.append({
                "Domaine": domain,
                "Valeur Estimée (€)": estimated_value
            })

        result_df = pd.DataFrame(results)
        st.dataframe(result_df)
        st.download_button("Télécharger les résultats", result_df.to_csv(index=False), "résultats.csv")

