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


APP_VERSION = "v1.7"
EBAY_REVIEW_NOTE = "Product review data is unavailable from the eBay Browse API."


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

            .small-muted {
                color: #64748b;
                font-size: 0.9rem;
            }

            .product-preview {
                margin-top: 0.85rem;
                padding: 1rem;
                border: 1px solid #bfdbfe;
                border-radius: 8px;
                background: #f8fbff;
            }

            .product-preview-grid {
                display: grid;
                grid-template-columns: minmax(180px, 320px) minmax(0, 1fr);
                gap: 1rem;
                align-items: center;
            }

            .product-preview-image-wrap {
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 180px;
                max-height: 320px;
                overflow: hidden;
                border: 1px solid #dbeafe;
                border-radius: 8px;
                background: #ffffff;
            }

            .product-preview-image {
                display: block;
                max-width: 100%;
                max-height: 300px;
                width: auto;
                height: auto;
                object-fit: contain;
            }

            .product-preview-empty {
                color: #64748b;
                font-size: 0.95rem;
                font-weight: 700;
            }

            .product-preview-title {
                margin: 0 0 0.75rem;
                color: #0f172a;
                font-size: 1.05rem;
                line-height: 1.35;
                font-weight: 800;
            }

            .product-preview-meta {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.75rem;
            }

            .product-preview-label {
                color: #64748b;
                font-size: 0.78rem;
                font-weight: 800;
                text-transform: uppercase;
            }

            .product-preview-value {
                margin-top: 0.2rem;
                color: #0f172a;
                font-size: 1rem;
                font-weight: 700;
            }

            @media (max-width: 760px) {
                .product-preview-grid {
                    grid-template-columns: 1fr;
                }

                .product-preview-meta {
                    grid-template-columns: 1fr;
                }
            }
            div[data-testid="stSidebar"] {
                background: #f8fafc;
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


def has_unavailable_ebay_product_data(rows):
    return any(
        str(row["Platform"]).lower() == "ebay"
        and (row["Reviews"] == "N/A" or row["Rating"] == "N/A")
        for row in rows
    )


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

def render_sidebar(products, rows, opportunities, connector_status):
    st.sidebar.markdown("## NicheScanner AI")
    st.sidebar.caption(f"Project version: {APP_VERSION}")

    st.sidebar.markdown("### Database statistics")
    st.sidebar.metric("Stored products", len(products))
    st.sidebar.metric("Platforms", len({row["Platform"] for row in rows}))
    st.sidebar.metric("Hidden opportunities", len(opportunities))

    st.sidebar.markdown("### Connectors")
    for connector_name, connector in connector_status.items():
        label = format_connector_label(connector_name)
        st.sidebar.caption(f"{label}: {connector['status']}")

    st.sidebar.markdown("### Quick actions")
    if st.sidebar.button("Clear database", width="stretch"):
        clear_products()
        st.rerun()

    st.sidebar.caption("Use the scan form to import mock marketplace results.")


def render_google_trends_card(summary):
    st.markdown('<div class="section-title">Google Trends Insight</div>', unsafe_allow_html=True)

    if summary["available"]:
        st.success(summary["message"])
    else:
        st.info(summary["message"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Keyword", summary["keyword"] or "No keyword selected")
    col2.metric("Trend Score", summary["trend_score"])
    col3.metric("Direction", summary["trend_direction"])


def render_scan_form():
    with st.form("search_form", enter_to_submit=True):
        keyword = st.text_input(
            "Scan keyword",
            placeholder="example: nurse, camping, cat"
        )

        submitted = st.form_submit_button(
            "Scan keyword",
            width="stretch"
        )

    if submitted:
        if not keyword.strip():
            st.warning("Please enter a keyword.")
        else:
            cleaned_keyword = keyword.strip()
            st.session_state["last_scan_keyword"] = cleaned_keyword

            with st.spinner("Scanning products..."):
                print("SCAN EXECUTED")
                products = scan_keyword(cleaned_keyword)
                print("SCAN FINISHED")
                imported_count = 0
                inserted_ebay_count = 0

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
                        if str(product.get("platform", "")).lower() == "ebay":
                            inserted_ebay_count += 1

                print(f"[DB] inserted ebay products count: {inserted_ebay_count}")

            st.success(
                f"Imported {imported_count} new products for '{cleaned_keyword}'."
            )
            st.rerun()


def get_selected_product_row(df):
    table_state = st.session_state.get("product_research_table")
    selected_rows = []

    if table_state is not None:
        if hasattr(table_state, "selection"):
            selected_rows = table_state.selection.rows
        elif isinstance(table_state, dict):
            selection = table_state.get("selection", {})
            selected_rows = selection.get("rows", [])

    if selected_rows:
        selected_index = int(selected_rows[0])
        st.session_state["selected_product_row_index"] = selected_index
    else:
        selected_index = st.session_state.get("selected_product_row_index")

    if selected_index is None or selected_index not in df.index:
        st.session_state.pop("selected_product_row_index", None)
        return None, None

    return selected_index, df.loc[selected_index]


def render_product_table(df):
    selected_index, selected_product = get_selected_product_row(df)

    def highlight_selected_row(row):
        if row.name == selected_index:
            return ["background-color: #e0f2fe"] * len(row)

        return [""] * len(row)

    styled_df = (
        df.style
        .map(competition_badge, subset=["Competition"])
        .apply(highlight_selected_row, axis=1)
    )

    visible_columns = [column for column in df.columns if column != "Image"]

    table_state = st.dataframe(
        styled_df,
        width="stretch",
        hide_index=True,
        column_order=visible_columns,
        key="product_research_table",
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "Price": st.column_config.NumberColumn("Price", format="%.2f"),
            "Product Link": st.column_config.LinkColumn(
                "Product",
                display_text="Open"
            ),
            "Shop Link": st.column_config.LinkColumn(
                "Shop URL",
                display_text="Open"
            ),
            "Score": st.column_config.ProgressColumn(
                "Overall Score",
                min_value=0,
                max_value=100,
                format="%d"
            ),
            "Demand": st.column_config.ProgressColumn("Demand", min_value=0, max_value=100, format="%d"),
            "Competition Score": st.column_config.ProgressColumn("Competition", min_value=0, max_value=100, format="%d"),
            "Trend": st.column_config.ProgressColumn("Trend", min_value=0, max_value=100, format="%d"),
            "Price Score": st.column_config.ProgressColumn("Price", min_value=0, max_value=100, format="%d"),
        }
    )

    if table_state.selection.rows:
        selected_index = int(table_state.selection.rows[0])
        st.session_state["selected_product_row_index"] = selected_index
        return df.loc[selected_index]

    return selected_product


def render_product_preview(product):
    if product is None:
        st.caption("Select a product row to preview details.")
        return

    image_url = str(product.get("Image", "") or "").strip()
    title = escape(str(product.get("Title", "Untitled product")))
    platform = escape(str(product.get("Platform", "Unavailable")))
    price = format_price(float(product.get("Price", 0)), str(product.get("Currency", "")))
    score = escape(str(product.get("Score", 0)))
    reviews = escape(str(product.get("Reviews", "N/A")))
    rating = escape(str(product.get("Rating", "N/A")))

    if image_url:
        image_markup = (
            f'<img class="product-preview-image" src="{escape(image_url, quote=True)}" '
            f'alt="{title}">'
        )
    else:
        image_markup = '<div class="product-preview-empty">No image available.</div>'

    st.markdown(
        f"""
        <div class="product-preview">
            <div class="product-preview-grid">
                <div class="product-preview-image-wrap">{image_markup}</div>
                <div>
                    <div class="product-preview-title">{title}</div>
                    <div class="product-preview-meta">
                        <div>
                            <div class="product-preview-label">Platform</div>
                            <div class="product-preview-value">{platform}</div>
                        </div>
                        <div>
                            <div class="product-preview-label">Price</div>
                            <div class="product-preview-value">{escape(price)}</div>
                        </div>
                        <div>
                            <div class="product-preview-label">Opportunity Score</div>
                            <div class="product-preview-value">{score}/100</div>
                        </div>
                        <div>
                            <div class="product-preview-label">Shop Reviews</div>
                            <div class="product-preview-value">{reviews}</div>
                        </div>
                        <div>
                            <div class="product-preview-label">Shop Rating</div>
                            <div class="product-preview-value">{rating}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_charts(df):
    chart_col1, chart_col2 = st.columns([1.45, 1], gap="large")

    with chart_col1:
        st.markdown('<div class="section-title">Top 10 Products by Score</div>', unsafe_allow_html=True)
        top_products = (
            df.sort_values("Score", ascending=False)
            .head(10)[["Title", "Score"]]
            .reset_index(drop=True)
        )

        st.vega_lite_chart(
            top_products,
            {
                "height": 320,
                "autosize": {"type": "fit", "contains": "padding"},
                "mark": {"type": "bar", "cornerRadiusEnd": 4, "tooltip": True},
                "encoding": {
                    "y": {
                        "field": "Title",
                        "type": "nominal",
                        "sort": "-x",
                        "axis": {
                            "title": None,
                            "labelLimit": 260,
                            "labelFontSize": 12
                        }
                    },
                    "x": {
                        "field": "Score",
                        "type": "quantitative",
                        "scale": {"domain": [0, 100]},
                        "axis": {"title": "Score", "grid": True}
                    },
                    "color": {
                        "field": "Score",
                        "type": "quantitative",
                        "scale": {"scheme": "blues"},
                        "legend": None
                    },
                    "tooltip": [
                        {"field": "Title", "type": "nominal"},
                        {"field": "Score", "type": "quantitative"}
                    ]
                },
                "config": {
                    "view": {"stroke": None},
                    "axis": {"labelColor": "#334155", "titleColor": "#64748b"}
                }
            },
            width="stretch"
        )

    with chart_col2:
        st.markdown('<div class="section-title">Platform Distribution</div>', unsafe_allow_html=True)
        platform_df = (
            df["Platform"]
            .value_counts()
            .reset_index()
        )
        platform_df.columns = ["Platform", "Products"]

        st.vega_lite_chart(
            platform_df,
            {
                "height": 320,
                "autosize": {"type": "fit", "contains": "padding"},
                "mark": {"type": "arc", "innerRadius": 52, "tooltip": True},
                "encoding": {
                    "theta": {"field": "Products", "type": "quantitative"},
                    "color": {
                        "field": "Platform",
                        "type": "nominal",
                        "legend": {"orient": "bottom", "title": None}
                    },
                    "tooltip": [
                        {"field": "Platform", "type": "nominal"},
                        {"field": "Products", "type": "quantitative"}
                    ]
                },
                "config": {"view": {"stroke": None}}
            },
            width="stretch"
        )


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

            if str(item["platform"]).lower() == "ebay":
                st.caption(EBAY_REVIEW_NOTE)

            if item.get("product_url"):
                st.link_button("Open product", item["product_url"])

            if item.get("shop_url"):
                shop_label = item.get("shop_name") or "Open shop"
                st.link_button(shop_label, item["shop_url"])

            st.write(f"**Competition:** {item['score']['competition']}")
            st.write(f"**Demand:** {item['score']['demand_score']}/100")
            st.write(f"**Competition Score:** {item['score']['competition_score']}/100")
            st.write(f"**Trend:** {item['score']['trend_score']}/100")
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


create_database()
load_css()

products = get_products()
trends_keyword = get_trends_keyword()
trend_summary = get_trend_summary(trends_keyword)
rows = build_product_rows(products, trend_summary["trend_score"])
opportunities = find_hidden_opportunities(products)
kpis = get_kpi_values(products, rows, opportunities)
connector_status = get_connector_status()

render_header()
render_sidebar(products, rows, opportunities, connector_status)

scan_col, note_col = st.columns([1.2, 1])

with scan_col:
    render_scan_form()

with note_col:
    st.markdown("### Research workflow")
    st.markdown(
        '<div class="small-muted">Scan a keyword, review scoring signals, compare platform distribution, and inspect hidden opportunities.</div>',
        unsafe_allow_html=True
    )

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    render_kpi_card("kpi-products", "Products", kpis["products"], "Stored in SQLite")

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

    render_google_trends_card(trend_summary)
    render_charts(df)

    st.markdown('<div class="section-title">Product Research Table</div>', unsafe_allow_html=True)
    if has_unavailable_ebay_product_data(rows):
        st.caption(EBAY_REVIEW_NOTE)
    selected_product = render_product_table(df)
    render_product_preview(selected_product)
    render_hidden_opportunities(opportunities)
else:
    render_google_trends_card(trend_summary)
    st.info("Scan a keyword to begin.")
