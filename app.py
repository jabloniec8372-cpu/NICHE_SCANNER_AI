import sys
from pathlib import Path
from html import escape

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent
CORE_DIR = ROOT_DIR / "core"
sys.path.append(str(CORE_DIR))

from database import create_database, add_product, get_products, clear_products
from market_scanner import scan_keyword
from scoring import calculate_score
from opportunity_finder import find_hidden_opportunities
from connectors.connector_manager import get_connector_status, get_trend_summary
from product_utils import product_to_dict


APP_VERSION = "v1.7.1"
PRODUCT_TYPES = [
    "T-Shirts",
    "Mugs",
    "Stickers",
    "Wall Art",
    "Hoodies",
    "Towels",
    "Posters",
    "Tote Bags",
    "Other",
]

PRODUCT_TYPE_KEYWORDS = {
    "T-Shirts": ["t-shirt", "tshirt", "shirt", "tee"],
    "Hoodies": ["hoodie", "sweatshirt"],
    "Mugs": ["mug", "cup"],
    "Stickers": ["sticker", "stickers", "decal", "vinyl decal"],
    "Posters": ["poster", "print"],
    "Wall Art": ["wall art", "canvas"],
    "Towels": ["towel", "towels"],
    "Tote Bags": ["tote", "tote bag", "bag"],
}

PRODUCT_TYPE_QUERY_TERMS = {
    "T-Shirts": "shirt",
    "Hoodies": "hoodie",
    "Mugs": "mug",
    "Stickers": "sticker",
    "Posters": "poster",
    "Wall Art": "wall art",
    "Towels": "towel",
    "Tote Bags": "tote bag",
}


st.set_page_config(
    page_title="NicheScanner AI",
    page_icon="NS",
    layout="wide"
)


def load_css():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1.4rem;
                padding-bottom: 2rem;
            }

            .top-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                padding: 1.25rem 1.5rem;
                margin-bottom: 1.25rem;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
                background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
                color: white;
            }

            .brand-wrap {
                display: flex;
                align-items: center;
                gap: 0.9rem;
            }

            .logo {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 46px;
                height: 46px;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.16);
                border: 1px solid rgba(255, 255, 255, 0.25);
                font-weight: 800;
                letter-spacing: 0;
            }

            .title {
                margin: 0;
                font-size: 1.65rem;
                line-height: 1.1;
                font-weight: 800;
            }

            .subtitle {
                margin-top: 0.25rem;
                color: #dbeafe;
                font-size: 0.95rem;
            }

            .version-pill {
                padding: 0.45rem 0.75rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.14);
                border: 1px solid rgba(255, 255, 255, 0.25);
                color: #eff6ff;
                font-weight: 700;
            }

            .kpi-card {
                min-height: 112px;
                padding: 1rem;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                background: white;
                box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
            }

            .kpi-products { border-top: 5px solid #2563eb; }
            .kpi-best { border-top: 5px solid #16a34a; }
            .kpi-average { border-top: 5px solid #f59e0b; }
            .kpi-opportunities { border-top: 5px solid #dc2626; }

            .kpi-label {
                color: #64748b;
                font-size: 0.85rem;
                font-weight: 700;
                text-transform: uppercase;
            }

            .kpi-value {
                margin-top: 0.35rem;
                color: #0f172a;
                font-size: 2rem;
                font-weight: 800;
            }

            .kpi-note {
                margin-top: 0.15rem;
                color: #64748b;
                font-size: 0.85rem;
            }

            .section-title {
                margin: 1.5rem 0 0.65rem;
                color: #0f172a;
                font-size: 1.15rem;
                font-weight: 800;
            }

            .opportunity-card {
                padding: 0.65rem 0;
            }

            .connector-status-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin: 0 0 0.85rem;
            }

            .connector-status-badge {
                display: inline-block;
                padding: 0.32rem 0.65rem;
                border: 1px solid #bbf7d0;
                border-radius: 999px;
                background: #f0fdf4;
                color: #166534;
                font-size: 0.85rem;
                font-weight: 700;
                white-space: nowrap;
            }

            .connector-status-badge-muted {
                border-color: #e5e7eb;
                background: #f8fafc;
                color: #64748b;
            }

            div[data-testid="stForm"][aria-label="search_form"] div[data-testid="stFormSubmitButton"]:nth-of-type(1) button {
                border-color: #1d4ed8;
                background: #1d4ed8;
                color: #ffffff;
                font-weight: 800;
            }

            div[data-testid="stForm"][aria-label="search_form"] div[data-testid="stFormSubmitButton"]:nth-of-type(1) button:hover {
                border-color: #1e40af;
                background: #1e40af;
                color: #ffffff;
            }

            div[data-testid="stForm"][aria-label="search_form"] div[data-testid="stFormSubmitButton"]:nth-of-type(2) button {
                border-color: #cbd5e1;
                background: #ffffff;
                color: #475569;
                font-weight: 700;
            }

            div[data-testid="stForm"][aria-label="search_form"] div[data-testid="stFormSubmitButton"]:nth-of-type(2) button:hover {
                border-color: #94a3b8;
                background: #f8fafc;
                color: #334155;
            }

        </style>
        """,
        unsafe_allow_html=True
    )


def build_product_rows(products, trend_score=0):
    rows = []

    for product in products:
        product_data = product_to_dict(product)
        title = product_data["title"]
        product_type = product_data.get("product_type") or normalize_product_type(title)
        platform = product_data["platform"]
        price = product_data["price"]
        reviews = product_data["reviews"]
        rating = product_data["rating"]
        score = calculate_score(price, reviews, rating, platform, trend_score)

        rows.append({
            "Image": product_data["image_url"],
            "Title": title,
            "Platform": platform,
            "Price": price,
            "Currency": product_data["currency"],
            "Rating": format_marketplace_metric(platform, rating),
            "Reviews": format_marketplace_metric(platform, reviews),
            "Product Link": product_data["product_url"],
            "Shop": product_data["shop_name"],
            "Shop Link": product_data["shop_url"],
            "Listing ID": product_data["listing_id"],
            "Product Type": product_type,
            "Score": score["overall_score"],
            "Score Badge": score["score_badge"],
            "Demand": score["demand_score"],
            "Competition Score": score["competition_score"],
            "Trend": score["trend_score"],
            "Price Score": score["price_score"],
            "Confidence": score["confidence"],
            "Competition": score["competition"],
            "Opportunity": score["opportunity"],
        })
    return rows


def format_marketplace_metric(platform, value):
    if str(platform).lower() == "ebay" and value == 0:
        return "N/A"

    return value


def get_kpi_values(products, rows, opportunities):
    if not rows:
        return {
            "products": len(products),
            "best_score": 0,
            "average_score": 0,
            "hidden_opportunities": len(opportunities),
            "best_product": "No products yet",
        }

    scores = [row["Score"] for row in rows]
    best_row = max(rows, key=lambda row: row["Score"])

    return {
        "products": len(products),
        "best_score": max(scores),
        "average_score": round(sum(scores) / len(scores), 1),
        "hidden_opportunities": len(opportunities),
        "best_product": best_row["Title"],
    }


def get_trends_keyword():
    return st.session_state.get("last_scan_keyword", "").strip()


def render_header():
    st.markdown(
        f"""
        <div class="top-header">
            <div class="brand-wrap">
                <div class="logo">NS</div>
                <div>
                    <h1 class="title">NicheScanner AI</h1>
                    <div class="subtitle">Modern niche research dashboard for product signals, scoring, and opportunities.</div>
                </div>
            </div>
            <div class="version-pill">{APP_VERSION}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_kpi_card(css_class, label, value, note):
    st.markdown(
        f"""
        <div class="kpi-card {css_class}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def competition_badge(value):
    colors = {
        "Low": "#16a34a",
        "Medium": "#f59e0b",
        "High": "#dc2626",
        "Very High": "#b91c1c",
    }
    color = colors.get(value, "#64748b")
    return f"color: white; background-color: {color}; font-weight: 700;"


def format_connector_label(connector_name):
    if connector_name == "ebay":
        return "eBay"

    return connector_name.replace("_", " ").title()


def get_selected_product_types():
    return [
        product_type
        for product_type in PRODUCT_TYPES
        if st.session_state.get(f"product_type_{product_type}", True)
    ]


def normalize_product_type(title):
    normalized_title = str(title).lower()
    for product_type in PRODUCT_TYPES:
        if product_type == "Other":
            continue

        if title_matches_product_type(normalized_title, product_type):
            return product_type

    return "Other"


def title_matches_product_type(title, product_type):
    normalized_title = str(title).lower()
    keywords = PRODUCT_TYPE_KEYWORDS.get(product_type, [])
    return any(keyword in normalized_title for keyword in keywords)


def build_scan_queries(keyword, selected_product_types):
    base_keyword = str(keyword).strip()

    if not selected_product_types:
        return [base_keyword]

    queries = []
    for product_type in selected_product_types:
        query_term = PRODUCT_TYPE_QUERY_TERMS.get(product_type)
        if query_term:
            queries.append(f"{base_keyword} {query_term}")

    return queries or [base_keyword]


def product_key(product):
    return (
        str(product.get("platform", "")).strip().lower(),
        str(product.get("title", "")).strip().lower(),
        str(product.get("product_url", "")).strip().lower(),
    )


def normalize_and_filter_products(products, selected_product_types):
    selected_types = set(selected_product_types)
    filtered_products = []
    seen_keys = set()

    for product in products:
        clean_product = product_to_dict(product)
        clean_product["product_type"] = normalize_product_type(clean_product["title"])

        if selected_types and clean_product["product_type"] not in selected_types:
            continue

        key = product_key(clean_product)
        if key in seen_keys:
            continue

        seen_keys.add(key)
        filtered_products.append(clean_product)

    return filtered_products


def build_scan_summary(products, selected_product_types):
    platform_counts = {}
    product_type_counts = {
        product_type: 0
        for product_type in (selected_product_types or PRODUCT_TYPES)
    }

    for product in products:
        platform = str(product.get("platform", "Unknown"))
        platform_counts[platform] = platform_counts.get(platform, 0) + 1

        product_type = product.get("product_type") or normalize_product_type(product.get("title", ""))
        product_type_counts[product_type] = product_type_counts.get(product_type, 0) + 1

    return {
        "platform_counts": platform_counts,
        "product_type_counts": product_type_counts,
    }


def render_count_summary(title, counts):
    if not counts:
        return

    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    columns = st.columns(max(1, min(len(counts), 4)))

    for index, (label, value) in enumerate(counts.items()):
        columns[index % len(columns)].metric(label, value)


def render_connector_status(connector_status):
    visible_connectors = ["etsy", "ebay"]
    status_items = []

    for connector_name in visible_connectors:
        connector = connector_status.get(connector_name, {"status": "Not configured"})
        label = format_connector_label(connector_name)
        status = str(connector["status"]).lower()
        is_connected = "configured" in status
        compact_status = "Connected" if is_connected else "Not connected"
        badge_class = "connector-status-badge" if is_connected else "connector-status-badge connector-status-badge-muted"
        status_items.append(
            f'<span class="{badge_class}">{label} {compact_status}</span>'
        )

    st.markdown(
        f"""
        <div class="connector-status-row">{"".join(status_items)}</div>
        """,
        unsafe_allow_html=True
    )


def render_scan_controls():
    st.markdown('<div class="section-title">Scan Platforms</div>', unsafe_allow_html=True)

    with st.form("search_form", enter_to_submit=True):
        platform_col1, platform_col2 = st.columns(2)
        with platform_col1:
            scan_ebay = st.checkbox("eBay", value=True)
        with platform_col2:
            scan_etsy = st.checkbox("Etsy", value=True)

        keyword_col, keyword_spacer = st.columns([0.58, 0.42])
        with keyword_col:
            keyword = st.text_input(
                "Keyword",
                placeholder="Enter keyword, e.g. beard, cat, fishing"
            )

        st.markdown("Product types")
        type_columns = st.columns(4)
        for index, product_type in enumerate(PRODUCT_TYPES):
            with type_columns[index % 4]:
                st.checkbox(
                    product_type,
                    value=True,
                    key=f"product_type_{product_type}"
                )

        action_col1, action_col2, action_spacer = st.columns([0.16, 0.22, 0.62])
        with action_col1:
            scan_requested = st.form_submit_button(
                "Scan",
                type="primary"
            )
        with action_col2:
            clear_requested = st.form_submit_button(
                "Clear database",
                type="secondary"
            )

    if clear_requested:
        clear_products()
        st.session_state.pop("last_scan_summary", None)
        st.session_state.pop("last_scan_product_titles", None)
        st.session_state.pop("selected_product_row_index", None)
        st.session_state.pop("selected_product_row_indices", None)
        st.rerun()

    if scan_requested:
        if not keyword.strip():
            st.warning("Please enter a keyword.")
        elif not scan_ebay and not scan_etsy:
            st.warning("Select at least one platform.")
        else:
            cleaned_keyword = keyword.strip()
            st.session_state["last_scan_keyword"] = cleaned_keyword
            selected_platforms = []
            if scan_ebay:
                selected_platforms.append("ebay")
            if scan_etsy:
                selected_platforms.append("etsy")

            selected_product_types = get_selected_product_types()
            scan_queries = build_scan_queries(cleaned_keyword, selected_product_types)

            with st.spinner("Scanning products..."):
                scanned_products = []
                for scan_query in scan_queries:
                    scanned_products.extend(
                        scan_keyword(scan_query, selected_platforms=selected_platforms)
                    )

                selected_platform_set = set(selected_platforms)
                platform_products = [
                    product_to_dict(product)
                    for product in scanned_products
                    if str(product.get("platform", "")).lower() in selected_platform_set
                ]
                products = normalize_and_filter_products(
                    platform_products,
                    selected_product_types
                )
                imported_count = 0

                for product in products:
                    was_inserted = add_product(
                        product["title"],
                        product["platform"],
                        product["price"],
                        product["reviews"],
                        product.get("rating", 0),
                        product.get("listing_id", ""),
                        product.get("product_url", ""),
                        product.get("image_url", ""),
                        product.get("shop_name", ""),
                        product.get("shop_url", ""),
                        product.get("currency", ""),
                    )

                    if was_inserted:
                        imported_count += 1

            st.session_state["last_scan_summary"] = build_scan_summary(
                products,
                selected_product_types
            )
            st.session_state["last_scan_product_titles"] = [
                product["title"] for product in products
            ]

            st.success(
                f"Imported {imported_count} new products for '{cleaned_keyword}'."
            )
            st.rerun()


def render_scan_summary():
    summary = st.session_state.get("last_scan_summary")
    if not summary:
        return

    render_count_summary("Scan Results By Platform", summary["platform_counts"])
    render_count_summary("Scan Results By Product Type", summary["product_type_counts"])


TABLE_SELECTION_MODE = "single-row"


def truncate_text(value, max_length=34):
    text = str(value)
    if len(text) <= max_length:
        return text

    return f"{text[:max_length - 3]}..."


def get_table_selected_indices(table_state, df):
    selected_rows = []

    if table_state is not None:
        if hasattr(table_state, "selection"):
            selected_rows = table_state.selection.rows
        elif isinstance(table_state, dict):
            selected_rows = table_state.get("selection", {}).get("rows", [])

    if selected_rows:
        selected_indices = [int(row) for row in selected_rows if int(row) in df.index]
        st.session_state["selected_product_row_indices"] = selected_indices
    else:
        selected_indices = st.session_state.get("selected_product_row_indices", [])

    selected_indices = [index for index in selected_indices if index in df.index]

    if not selected_indices:
        st.session_state.pop("selected_product_row_indices", None)
        return []

    return selected_indices


def get_primary_selected_index(table_state, df):
    selected_indices = get_table_selected_indices(table_state, df)

    if selected_indices:
        selected_index = selected_indices[0]
        st.session_state["selected_product_row_index"] = selected_index
    else:
        selected_index = st.session_state.get("selected_product_row_index")

    if selected_index is None or selected_index not in df.index:
        st.session_state.pop("selected_product_row_index", None)
        return None

    return selected_index


def render_product_table(df):
    selected_index = st.session_state.get("selected_product_row_index")
    display_df = df.copy()
    display_df["Full Title"] = display_df["Title"]
    display_df["Title"] = display_df["Title"].map(truncate_text)

    def highlight_selected_row(row):
        if row.name == selected_index:
            return ["background-color: #dbeafe; font-weight: 700;"] * len(row)

        return [""] * len(row)

    styled_df = (
        display_df.style
        .map(competition_badge, subset=["Competition"])
        .apply(highlight_selected_row, axis=1)
    )

    hidden_columns = {"Image", "Trend", "Platform", "Full Title"}
    visible_columns = [
        column for column in display_df.columns if column not in hidden_columns
    ]

    table_state = st.dataframe(
        styled_df,
        width="stretch",
        hide_index=True,
        column_order=visible_columns,
        key="product_research_table",
        on_select="rerun",
        selection_mode=TABLE_SELECTION_MODE,
        column_config={
            "Title": st.column_config.TextColumn(
                "Title",
                help="Select a row to view the full product title below."
            ),
            "Price": st.column_config.NumberColumn("Price", format="%.2f"),
            "Product Link": st.column_config.LinkColumn(
                "Source",
                display_text="Open product"
            ),
            "Shop Link": st.column_config.LinkColumn(
                "Shop Link",
                display_text="Open shop"
            ),
            "Score": st.column_config.ProgressColumn(
                "Overall Score",
                min_value=0,
                max_value=100,
                format="%d"
            ),
            "Demand": st.column_config.ProgressColumn("Demand", min_value=0, max_value=100, format="%d"),
            "Competition Score": st.column_config.ProgressColumn("Competition", min_value=0, max_value=100, format="%d"),
            "Price Score": st.column_config.ProgressColumn("Price Score", min_value=0, max_value=100, format="%d"),
        }
    )

    selected_index = get_primary_selected_index(table_state, df)
    if selected_index is None:
        return None

    return df.loc[selected_index]


def render_product_preview(product):
    if product is None:
        return

    image_url = str(product.get("Image", "") or "").strip()
    title = escape(str(product.get("Title", "")))
    platform = escape(str(product.get("Platform", "")))
    price = escape(format_price(float(product.get("Price", 0)), str(product.get("Currency", ""))))
    score = escape(str(product.get("Score", 0)))
    shop = escape(str(product.get("Shop", "") or "Unavailable"))

    st.markdown('<div class="section-title">Selected Product</div>', unsafe_allow_html=True)

    preview_col, detail_col = st.columns([1, 2.2], gap="large")
    with preview_col:
        if image_url:
            st.image(image_url, use_container_width=True)

    with detail_col:
        st.markdown(f"**{title}**")
        st.write(f"Platform: {platform}")
        st.write(f"Price: {price}")
        st.write(f"Shop/Seller: {shop}")
        st.write(f"Opportunity Score: {score}/100")
        if product.get("Product Link"):
            st.link_button("Open", product["Product Link"])
        if product.get("Shop Link"):
            st.link_button("Open shop", product["Shop Link"])


def render_hidden_opportunities(opportunities):
    st.markdown('<div class="section-title">Hidden Opportunities</div>', unsafe_allow_html=True)

    if not opportunities:
        st.info("No hidden opportunities found.")
        return

    for item in opportunities:
        title = item["title"]
        total_score = item["score"]["total_score"]

        with st.expander(f"{title} | Score {total_score}/100", expanded=False):
            st.markdown('<div class="opportunity-card">', unsafe_allow_html=True)

            if item.get("image_url"):
                st.image(item["image_url"], width=120)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Platform", item["platform"])
            col2.metric("Price", format_price(item["price"], item.get("currency", "")))
            col3.metric("Shop Reviews", format_marketplace_metric(item["platform"], item["reviews"]))
            col4.metric("Shop Rating", format_marketplace_metric(item["platform"], item["rating"]))

            if item.get("product_url"):
                st.link_button("Open product", item["product_url"])

            if item.get("shop_url"):
                shop_label = item.get("shop_name") or "Open shop"
                st.link_button(shop_label, item["shop_url"])

            st.write(f"**Competition:** {item['score']['competition']}")
            st.write(f"**Demand:** {item['score']['demand_score']}/100")
            st.write(f"**Competition Score:** {item['score']['competition_score']}/100")
            st.write(f"**Price:** {item['score']['price_score']}/100")
            st.write(f"**Confidence:** {item['score']['confidence']}")
            st.write("**Reasons:**")

            for reason in item["reasons"]:
                st.write(f"- {reason}")

            st.markdown("</div>", unsafe_allow_html=True)


def format_price(price, currency=""):
    if currency:
        return f"{currency} {price:.2f}"

    return f"${price:.2f}"


def get_current_result_products(products):
    last_scan_titles = st.session_state.get("last_scan_product_titles")

    if not last_scan_titles:
        return products

    title_filter = {
        str(title).strip().lower()
        for title in last_scan_titles
    }
    return [
        product
        for product in products
        if product_to_dict(product)["title"].strip().lower() in title_filter
    ]


create_database()
load_css()

stored_products = get_products()
products = get_current_result_products(stored_products)
trends_keyword = get_trends_keyword()
trend_summary = get_trend_summary(trends_keyword)
rows = build_product_rows(products, trend_summary["trend_score"])
opportunities = find_hidden_opportunities(products)
kpis = get_kpi_values(products, rows, opportunities)
connector_status = get_connector_status()

render_header()
render_connector_status(connector_status)
render_scan_controls()
render_scan_summary()

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    render_kpi_card("kpi-products", "Products", kpis["products"], "Current catalog")

with kpi_col2:
    render_kpi_card("kpi-best", "Best Score", kpis["best_score"], kpis["best_product"])

with kpi_col3:
    render_kpi_card("kpi-average", "Average Score", kpis["average_score"], "Across all products")

with kpi_col4:
    render_kpi_card("kpi-opportunities", "Hidden Opportunities", kpis["hidden_opportunities"], "Strong demand signals")

if rows:
    df = (
        pd.DataFrame(rows)
        .sort_values("Score", ascending=False)
        .reset_index(drop=True)
    )

    st.markdown('<div class="section-title">Product Research Table</div>', unsafe_allow_html=True)
    selected_product = render_product_table(df)
    render_product_preview(selected_product)
    render_hidden_opportunities(opportunities)
else:
    st.info("No products yet.")
