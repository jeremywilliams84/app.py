import os
import streamlit as st
import pandas as pd
import requests
import io

def _get_serpapi_key() -> str:
    # 1. Secrets Streamlit Cloud (format : SERPAPI_KEY = "...")
    try:
        key = st.secrets["SERPAPI_KEY"]
        if key:
            return key
    except Exception:
        pass
    # 2. Secrets imbriqués : [secrets] SERPAPI_KEY = "..."
    try:
        key = st.secrets["secrets"]["SERPAPI_KEY"]
        if key:
            return key
    except Exception:
        pass
    # 3. Variable d'environnement (local)
    return os.environ.get("SERPAPI_KEY", "")

SERPAPI_KEY = _get_serpapi_key()

SERPAPI_URL = "https://serpapi.com/search"


def search_maps(query: str, max_results: int) -> list[dict]:
    rows = []
    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "hl": "fr",
        "api_key": SERPAPI_KEY,
    }
    start = 0
    while len(rows) < max_results:
        params["start"] = start
        resp = requests.get(SERPAPI_URL, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        places = data.get("local_results", [])
        if not places:
            break
        for p in places:
            if len(rows) >= max_results:
                break
            rows.append(_parse(p, query))
        if not data.get("serpapi_pagination", {}).get("next"):
            break
        start += 20
    return rows


def _parse(p: dict, query: str) -> dict:
    gps = p.get("gps_coordinates", {})
    return {
        "Recherche": query,
        "Nom": p.get("title", ""),
        "Catégorie": p.get("type", ""),
        "Adresse": p.get("address", ""),
        "Téléphone": p.get("phone", ""),
        "Site web": p.get("website", ""),
        "Note": p.get("rating", ""),
        "Nombre d'avis": p.get("reviews", ""),
        "Statut": p.get("open_state", ""),
        "Latitude": gps.get("latitude", ""),
        "Longitude": gps.get("longitude", ""),
        "URL Google Maps": p.get("place_id_search", p.get("link", "")),
    }


def to_excel(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Résultats")
        ws = w.sheets["Résultats"]
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = min(
                max(len(str(c.value or "")) for c in col) + 4, 60
            )
    return buf.getvalue()


# ── UI ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Google Maps Scraper", page_icon="📍", layout="wide")
st.title("📍 Google Maps Scraper — Prospection locale")
st.caption("Extraction via SerpAPI — aucune installation de navigateur requise.")

if not SERPAPI_KEY:
    st.warning("Clé SerpAPI non configurée. Entrez-la ci-dessous pour continuer.")
    manual_key = st.text_input("Clé SerpAPI", type="password",
                               placeholder="Collez votre clé SerpAPI ici")
    if manual_key:
        SERPAPI_KEY = manual_key
    else:
        st.info("Créez un compte gratuit sur [serpapi.com](https://serpapi.com/) — 100 recherches/mois offertes.")
        st.stop()

with st.sidebar:
    st.header("⚙️ Paramètres")
    max_results = st.number_input(
        "Résultats max par recherche", min_value=1, max_value=100, value=20
    )
    st.markdown("**Crédit SerpAPI :** 100 recherches/mois gratuites")
    st.markdown("[Créer un compte SerpAPI](https://serpapi.com/)")

tab1, tab2 = st.tabs(["🔍 Recherche simple", "📋 Batch"])

# ── SINGLE ────────────────────────────────────────────────────────────────────
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        keyword = st.text_input("Mot-clé", placeholder="kinésiologue, plombier…")
    with c2:
        location = st.text_input("Localisation", placeholder="Hérault, Montpellier…")

    if st.button("Lancer", type="primary", disabled=not (keyword and location)):
        query = f"{keyword} {location}"
        with st.spinner(f"Recherche : « {query} »…"):
            try:
                rows = search_maps(query, int(max_results))
            except Exception as e:
                st.error(f"Erreur SerpAPI : {e}")
                st.stop()
        if not rows:
            st.warning("Aucun résultat.")
        else:
            df = pd.DataFrame(rows)
            st.success(f"✅ {len(df)} fiches extraites.")
            st.dataframe(df, use_container_width=True)
            c_a, c_b = st.columns(2)
            with c_a:
                st.download_button("⬇️ CSV", df.to_csv(index=False).encode("utf-8-sig"),
                                   f"{keyword}_{location}.csv", "text/csv")
            with c_b:
                st.download_button("⬇️ Excel", to_excel(df),
                                   f"{keyword}_{location}.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ── BATCH ─────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("Format : **`mot-clé | localisation`** — une ligne par recherche")
    batch_input = st.text_area(
        "Recherches",
        placeholder="kinésiologue | Hérault\nkinésiologue | Gard\nphysiothérapeute | Montpellier",
        height=150,
    )
    uploaded = st.file_uploader("ou importer CSV (colonnes `keyword` et `location`)", type=["csv"])

    searches = []
    if batch_input.strip():
        for line in batch_input.strip().splitlines():
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 2 and all(parts):
                searches.append((parts[0], parts[1]))
            else:
                st.warning(f"Ligne ignorée : `{line}`")
    if uploaded:
        try:
            bdf = pd.read_csv(uploaded)
            for _, row in bdf.iterrows():
                searches.append((str(row["keyword"]).strip(), str(row["location"]).strip()))
        except Exception as e:
            st.error(f"CSV invalide : {e}")

    if searches:
        st.info(f"{len(searches)} recherche(s) en file.")

    if st.button("Lancer le batch", type="primary", disabled=not searches):
        all_rows: list[dict] = []
        prog = st.progress(0)
        for i, (kw, loc) in enumerate(searches):
            q = f"{kw} {loc}"
            st.write(f"🔎 `{q}`")
            try:
                all_rows.extend(search_maps(q, int(max_results)))
            except Exception as e:
                st.warning(f"Erreur pour « {q} » : {e}")
            prog.progress((i + 1) / len(searches))

        if all_rows:
            df_all = pd.DataFrame(all_rows).drop_duplicates(subset=["URL Google Maps"])
            st.success(f"✅ {len(df_all)} fiches uniques.")
            st.dataframe(df_all, use_container_width=True)
            c_a, c_b = st.columns(2)
            with c_a:
                st.download_button("⬇️ CSV", df_all.to_csv(index=False).encode("utf-8-sig"),
                                   "batch_gmaps.csv", "text/csv")
            with c_b:
                st.download_button("⬇️ Excel", to_excel(df_all), "batch_gmaps.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.warning("Aucune fiche extraite.")
