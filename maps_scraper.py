import os
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")

import streamlit as st
import pandas as pd
import time
import io
import re
import urllib.parse
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout


# ── Scraping helpers ──────────────────────────────────────────────────────────

def _accept_cookies(page):
    for selector in [
        'button[aria-label*="Tout accepter"]',
        'button[aria-label*="Accept all"]',
        'form[action*="consent"] button',
        'button:has-text("Accepter tout")',
        'button:has-text("Accept all")',
    ]:
        try:
            page.click(selector, timeout=2500)
            return
        except Exception:
            pass


def _scroll_feed(page, max_results: int, status_cb=None):
    """Scroll the results feed until we have enough items or reach the end."""
    feed_sel = 'div[role="feed"]'
    try:
        page.wait_for_selector(feed_sel, timeout=12000)
    except PWTimeout:
        return

    prev = 0
    stale = 0
    while True:
        links = page.locator('a.hfpxzc').all()
        count = len(links)
        if status_cb:
            status_cb(count)
        if count >= max_results:
            break
        # Check "end of list" marker
        end_marker = page.locator('div[jsaction*="pane.resultSection.endOfList"]')
        if end_marker.count() > 0:
            break
        page.locator(feed_sel).evaluate("el => el.scrollBy(0, 2000)")
        time.sleep(1.2)
        if count == prev:
            stale += 1
            if stale >= 3:
                break
        else:
            stale = 0
        prev = count


def _extract_list_item(link) -> dict:
    """Extract lightweight data from a result card in the feed."""
    name = link.get_attribute("aria-label") or ""
    href = link.get_attribute("href") or ""
    # Rating & reviews sit in the parent wrapper
    try:
        wrapper = link.locator("xpath=../..")
        rating_el = wrapper.locator("span.MW4etd").first
        rating = rating_el.inner_text(timeout=500).strip() if rating_el.count() else ""
        reviews_el = wrapper.locator("span.UY7F9").first
        reviews_raw = reviews_el.inner_text(timeout=500).strip() if reviews_el.count() else ""
        reviews = re.sub(r"[^\d]", "", reviews_raw)
        # Category / address from aria-label on the container div
        info_el = wrapper.locator("div.W4Efsd").last
        info_text = info_el.inner_text(timeout=500).strip() if info_el.count() else ""
    except Exception:
        rating, reviews, info_text = "", "", ""
    return {"name": name, "href": href, "rating": rating, "reviews": reviews, "info_text": info_text}


def _extract_details(page, href: str) -> dict:
    """Navigate to a place page and pull phone, website, full address, category."""
    details: dict = {}
    try:
        page.goto(href, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        return details

    def _text(sel: str) -> str:
        try:
            el = page.locator(sel).first
            return el.inner_text(timeout=1500).strip() if el.count() else ""
        except Exception:
            return ""

    def _attr(sel: str, attr: str) -> str:
        try:
            el = page.locator(sel).first
            return (el.get_attribute(attr, timeout=1500) or "").strip() if el.count() else ""
        except Exception:
            return ""

    details["phone"] = _text('button[data-item-id^="phone:tel"] .fontBodyMedium')
    details["website"] = _attr('a[data-item-id="authority"]', "href")
    details["address"] = _text('button[data-item-id="address"] .fontBodyMedium')
    details["category"] = _text("button.DkEaL")

    # Latitude / longitude from the URL
    try:
        current_url = page.url
        m = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", current_url)
        if m:
            details["lat"] = m.group(1)
            details["lng"] = m.group(2)
    except Exception:
        pass

    return details


def scrape_maps(query: str, max_results: int, fetch_details: bool, progress_cb=None) -> list[dict]:
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx = browser.new_context(
            viewport={"width": 1366, "height": 900},
            locale="fr-FR",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        search_page = ctx.new_page()
        encoded = urllib.parse.quote_plus(query)
        search_page.goto(
            f"https://www.google.fr/maps/search/{encoded}/?hl=fr",
            wait_until="domcontentloaded",
            timeout=20000,
        )
        _accept_cookies(search_page)
        time.sleep(1)

        def _status(n):
            if progress_cb:
                progress_cb(f"Chargement des fiches… {n} trouvées")

        _scroll_feed(search_page, max_results, status_cb=_status)

        links = search_page.locator("a.hfpxzc").all()[:max_results]
        items = [_extract_list_item(lnk) for lnk in links]

        if fetch_details:
            detail_page = ctx.new_page()
            for i, item in enumerate(items):
                if progress_cb:
                    progress_cb(f"Détails {i+1}/{len(items)} — {item['name'][:40]}")
                details = _extract_details(detail_page, item["href"]) if item["href"] else {}
                rows.append(_build_row(item, details, query))
            detail_page.close()
        else:
            for item in items:
                rows.append(_build_row(item, {}, query))

        browser.close()
    return rows


def _build_row(item: dict, details: dict, query: str) -> dict:
    # Fallback: parse category/address from info_text when details not fetched
    info = item.get("info_text", "")
    parts = [p.strip() for p in re.split(r"[·•\n]", info) if p.strip()]
    fallback_cat = parts[0] if parts else ""
    fallback_addr = parts[-1] if len(parts) > 1 else ""

    return {
        "Recherche": query,
        "Nom": item.get("name", ""),
        "Catégorie": details.get("category") or fallback_cat,
        "Adresse": details.get("address") or fallback_addr,
        "Téléphone": details.get("phone", ""),
        "Site web": details.get("website", ""),
        "Note": item.get("rating", ""),
        "Nombre d'avis": item.get("reviews", ""),
        "Latitude": details.get("lat", ""),
        "Longitude": details.get("lng", ""),
        "URL Google Maps": item.get("href", ""),
    }


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Résultats")
        ws = writer.sheets["Résultats"]
        for col in ws.columns:
            width = max(len(str(c.value or "")) for c in col)
            ws.column_dimensions[col[0].column_letter].width = min(width + 4, 60)
    return buf.getvalue()


# ── UI ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Google Maps Scraper", page_icon="📍", layout="wide")
st.title("📍 Google Maps Scraper — Prospection locale")
st.caption("Extraction sans clé API via scraping Playwright (headless Chromium).")

with st.sidebar:
    st.header("⚙️ Paramètres")
    fetch_details = st.toggle(
        "Enrichir avec détails (téléphone, site web, adresse complète)",
        value=True,
        help="Ouvre chaque fiche individuellement. Plus lent mais données complètes.",
    )
    max_results = st.number_input(
        "Résultats max par recherche", min_value=1, max_value=120, value=20,
        help="Google Maps affiche env. 20 résultats par page, jusqu'à ~120 avec défilement."
    )
    st.info("Gratuit — aucune clé API requise.")

tab_single, tab_batch = st.tabs(["🔍 Recherche simple", "📋 Batch"])

# ── SINGLE ────────────────────────────────────────────────────────────────────
with tab_single:
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Mot-clé", placeholder="kinésiologue, plombier, dentiste…")
    with col2:
        location = st.text_input("Localisation", placeholder="Hérault, Montpellier, Paris…")

    if st.button("Lancer la recherche", type="primary", disabled=not (keyword and location)):
        query = f"{keyword} {location}"
        status_box = st.empty()
        status_box.info(f"Ouverture de Google Maps pour « {query} »…")

        def update_status(msg):
            status_box.info(msg)

        try:
            rows = scrape_maps(query, int(max_results), fetch_details, progress_cb=update_status)
        except Exception as e:
            st.error(f"Erreur Playwright : {e}")
            st.stop()

        status_box.empty()
        if not rows:
            st.warning("Aucun résultat extrait.")
        else:
            df = pd.DataFrame(rows)
            st.success(f"✅ {len(df)} fiches extraites.")
            st.dataframe(df, use_container_width=True)
            c1, c2 = st.columns(2)
            with c1:
                st.download_button("⬇️ CSV", df.to_csv(index=False).encode("utf-8-sig"),
                                   f"{keyword}_{location}.csv", "text/csv")
            with c2:
                st.download_button("⬇️ Excel", to_excel_bytes(df),
                                   f"{keyword}_{location}.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ── BATCH ─────────────────────────────────────────────────────────────────────
with tab_batch:
    st.markdown("Format : **`mot-clé | localisation`** — une ligne par recherche")
    batch_input = st.text_area(
        "Recherches",
        placeholder="kinésiologue | Hérault\nkinésiologue | Gard\nphysiothérapeute | Montpellier",
        height=160,
    )
    uploaded = st.file_uploader("ou importer un CSV (colonnes `keyword` et `location`)", type=["csv"])

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
        overall = st.progress(0, text="Démarrage…")
        status_box = st.empty()

        for idx, (kw, loc) in enumerate(searches):
            q = f"{kw} {loc}"
            st.write(f"🔎 `{q}`")

            def upd(msg, _q=q):
                status_box.info(f"[{_q}] {msg}")

            try:
                rows = scrape_maps(q, int(max_results), fetch_details, progress_cb=upd)
                all_rows.extend(rows)
            except Exception as e:
                st.warning(f"Erreur pour « {q} » : {e}")
            overall.progress((idx + 1) / len(searches), text=f"{idx+1}/{len(searches)} recherches")

        status_box.empty()
        overall.empty()

        if all_rows:
            df_all = pd.DataFrame(all_rows)
            before = len(df_all)
            df_all = df_all.drop_duplicates(subset=["URL Google Maps"])
            after = len(df_all)
            if before != after:
                st.info(f"{before - after} doublons supprimés — {after} fiches uniques.")
            st.success(f"✅ {after} fiches au total.")
            st.dataframe(df_all, use_container_width=True)
            c1, c2 = st.columns(2)
            with c1:
                st.download_button("⬇️ CSV", df_all.to_csv(index=False).encode("utf-8-sig"),
                                   "batch_gmaps.csv", "text/csv")
            with c2:
                st.download_button("⬇️ Excel", to_excel_bytes(df_all), "batch_gmaps.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.warning("Aucune fiche extraite.")
