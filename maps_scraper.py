import streamlit as st
import requests
import pandas as pd
import time
import io
from config import GOOGLE_MAPS_API_KEY

TEXTSEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
DETAILS_FIELDS = "name,formatted_phone_number,international_phone_number,website,formatted_address,rating,user_ratings_total,types,geometry,url,business_status,opening_hours"


def text_search(query: str, api_key: str) -> list[dict]:
    """Fetch all paginated results for a text search query."""
    results = []
    params = {"query": query, "key": api_key, "language": "fr"}
    while True:
        resp = requests.get(TEXTSEARCH_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")
        if status not in ("OK", "ZERO_RESULTS"):
            st.warning(f"API Text Search — statut inattendu : {status}")
            break
        results.extend(data.get("results", []))
        next_token = data.get("next_page_token")
        if not next_token:
            break
        # Google requires a short delay before the next_page_token is valid
        time.sleep(2)
        params = {"pagetoken": next_token, "key": api_key}
    return results


def get_place_details(place_id: str, api_key: str) -> dict:
    """Fetch enriched details (phone, website, etc.) for a place_id."""
    params = {"place_id": place_id, "fields": DETAILS_FIELDS, "key": api_key, "language": "fr"}
    resp = requests.get(DETAILS_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") == "OK":
        return data.get("result", {})
    return {}


def parse_result(place: dict, details: dict) -> dict:
    geo = place.get("geometry", {}).get("location", {})
    types = place.get("types", [])
    category = types[0].replace("_", " ").title() if types else ""
    hours = details.get("opening_hours", {})
    open_now = hours.get("open_now")
    if open_now is True:
        open_status = "Ouvert"
    elif open_now is False:
        open_status = "Fermé"
    else:
        open_status = ""
    return {
        "Nom": details.get("name") or place.get("name", ""),
        "Catégorie": category,
        "Adresse": details.get("formatted_address") or place.get("formatted_address", ""),
        "Téléphone": details.get("formatted_phone_number", ""),
        "Téléphone international": details.get("international_phone_number", ""),
        "Site web": details.get("website", ""),
        "Note": place.get("rating", ""),
        "Nombre d'avis": place.get("user_ratings_total", ""),
        "Statut": details.get("business_status", "").replace("_", " ").title(),
        "Ouvert maintenant": open_status,
        "Latitude": geo.get("lat", ""),
        "Longitude": geo.get("lng", ""),
        "URL Google Maps": details.get("url") or f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id', '')}",
        "Place ID": place.get("place_id", ""),
    }


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Résultats")
        ws = writer.sheets["Résultats"]
        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 60)
    return buf.getvalue()


# ── UI ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Google Maps Scraper", page_icon="📍", layout="wide")
st.title("📍 Google Maps Scraper — Prospection locale")
st.caption("Extrait les fiches d'entreprises depuis Google Maps via l'API Places.")

if not GOOGLE_MAPS_API_KEY:
    st.error("Clé API Google Maps manquante. Ajoutez `GOOGLE_MAPS_API_KEY` dans `config.py`.")
    st.stop()

with st.sidebar:
    st.header("⚙️ Paramètres")
    fetch_details = st.toggle("Enrichir avec détails (téléphone, site web)", value=True,
                               help="Effectue un appel API supplémentaire par fiche. Plus lent mais données complètes.")
    max_results = st.number_input("Nombre max de résultats par recherche", min_value=1, max_value=200, value=60)
    st.divider()
    st.markdown("**Coût API estimé :**")
    st.markdown("- Text Search : ~0,017 $/requête")
    st.markdown("- Place Details : ~0,017 $/requête")
    st.markdown("[Tarifs Google Maps](https://developers.google.com/maps/billing/pricing)")

tab_single, tab_batch = st.tabs(["🔍 Recherche simple", "📋 Recherche batch"])

# ── SINGLE SEARCH ─────────────────────────────────────────────────────────────

with tab_single:
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Mot-clé métier", placeholder="kinésiologue, plombier, dentiste…")
    with col2:
        location = st.text_input("Localisation", placeholder="Paris 75001, Lyon, Hérault…")

    if st.button("Lancer la recherche", type="primary", disabled=not (keyword and location)):
        query = f"{keyword} {location}"
        with st.spinner(f"Recherche en cours : « {query} »…"):
            try:
                places = text_search(query, GOOGLE_MAPS_API_KEY)
            except requests.RequestException as e:
                st.error(f"Erreur réseau : {e}")
                st.stop()

        places = places[:max_results]
        if not places:
            st.info("Aucun résultat trouvé.")
        else:
            st.success(f"{len(places)} fiches trouvées.")
            rows = []
            progress = st.progress(0, text="Récupération des détails…")
            for i, place in enumerate(places):
                details = get_place_details(place["place_id"], GOOGLE_MAPS_API_KEY) if fetch_details else {}
                rows.append(parse_result(place, details))
                progress.progress((i + 1) / len(places), text=f"{i+1}/{len(places)} fiches traitées")
            progress.empty()

            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)

            col_csv, col_xlsx = st.columns(2)
            with col_csv:
                st.download_button("⬇️ Télécharger CSV", df.to_csv(index=False).encode("utf-8-sig"),
                                   f"{keyword}_{location}.csv", "text/csv")
            with col_xlsx:
                st.download_button("⬇️ Télécharger Excel", to_excel_bytes(df),
                                   f"{keyword}_{location}.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ── BATCH SEARCH ──────────────────────────────────────────────────────────────

with tab_batch:
    st.markdown("Entrez une recherche par ligne au format **`mot-clé | localisation`**")
    batch_input = st.text_area(
        "Recherches",
        placeholder="kinésiologue | Hérault\nkinésiologue | Gard\nphysiothérapeute | Montpellier",
        height=180,
    )
    st.markdown("— ou importez un CSV (colonnes `keyword` et `location`) :")
    uploaded = st.file_uploader("Importer CSV", type=["csv"], label_visibility="collapsed")

    searches = []
    if batch_input.strip():
        for line in batch_input.strip().splitlines():
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 2 and parts[0] and parts[1]:
                searches.append((parts[0], parts[1]))
            else:
                st.warning(f"Ligne ignorée (format invalide) : `{line}`")
    if uploaded:
        try:
            batch_df = pd.read_csv(uploaded)
            for _, row in batch_df.iterrows():
                searches.append((str(row["keyword"]).strip(), str(row["location"]).strip()))
        except Exception as e:
            st.error(f"Impossible de lire le CSV : {e}")

    if searches:
        st.info(f"{len(searches)} recherche(s) en file d'attente.")

    if st.button("Lancer le batch", type="primary", disabled=not searches):
        all_rows = []
        total = len(searches)
        overall = st.progress(0, text="Démarrage du batch…")
        for idx, (kw, loc) in enumerate(searches):
            query = f"{kw} {loc}"
            st.write(f"🔎 `{query}`")
            try:
                places = text_search(query, GOOGLE_MAPS_API_KEY)
            except requests.RequestException as e:
                st.warning(f"Erreur pour « {query} » : {e}")
                overall.progress((idx + 1) / total)
                continue
            places = places[:max_results]
            inner = st.progress(0, text=f"Détails… 0/{len(places)}")
            for i, place in enumerate(places):
                details = get_place_details(place["place_id"], GOOGLE_MAPS_API_KEY) if fetch_details else {}
                row = parse_result(place, details)
                row["Recherche"] = query
                all_rows.append(row)
                inner.progress((i + 1) / max(len(places), 1), text=f"Détails… {i+1}/{len(places)}")
            inner.empty()
            overall.progress((idx + 1) / total, text=f"{idx+1}/{total} recherches terminées")

        overall.empty()
        if all_rows:
            df_all = pd.DataFrame(all_rows)
            # Dédoublonnage sur Place ID
            before = len(df_all)
            df_all = df_all.drop_duplicates(subset=["Place ID"])
            after = len(df_all)
            if before != after:
                st.info(f"{before - after} doublons supprimés ({after} fiches uniques).")
            st.success(f"✅ {after} fiches extraites au total.")
            st.dataframe(df_all, use_container_width=True)
            col_csv2, col_xlsx2 = st.columns(2)
            with col_csv2:
                st.download_button("⬇️ Télécharger CSV", df_all.to_csv(index=False).encode("utf-8-sig"),
                                   "batch_gmaps.csv", "text/csv")
            with col_xlsx2:
                st.download_button("⬇️ Télécharger Excel", to_excel_bytes(df_all),
                                   "batch_gmaps.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.warning("Aucune fiche extraite.")
