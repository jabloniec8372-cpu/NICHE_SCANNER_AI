import sys
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent
CORE_DIR = ROOT_DIR / "core"
sys.path.append(str(CORE_DIR))

from database import create_database, add_product, get_products, clear_products
from market_scanner import scan_keyword
from scoring import calculate_score
from opportunity_finder import find_hidden_opportunities
from connectors.google_trends import get_google_trend_summary


APP_VERSION = "v1.4"


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

            div[data-testid="stSidebar"] {
                background: #f8fafc;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def build_product_rows(products):
    rows = []

    for product in products:
        title, platform, price, reviews, rating = product
        score = calculate_score(price, reviews, rating)

        rows.append({
            "Title": title,
            "Platform": platform,
            "Price": price,
            "Rating": rating,
            "Reviews": reviews,
            "Score": score["total_score"],
            "Competition": score["competition"],
            "Opportunity": score["opportunity"],
        })

    return rows


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


def get_trends_keyword(rows):
    if not rows:
        return ""

    best_row = max(rows, key=lambda row: row["Score"])
    title_words = str(best_row["Title"]).split()

    if len(title_words) >= 2:
        return " ".join(title_words[:2])

    return best_row["Title"]


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


def render_sidebar(products, rows, opportunities):
    st.sidebar.markdown("## NicheScanner AI")
    st.sidebar.caption(f"Project version: {APP_VERSION}")

    st.sidebar.markdown("### Database statistics")
    st.sidebar.metric("Stored products", len(products))
    st.sidebar.metric("Platforms", len({row["Platform"] for row in rows}))
    st.sidebar.metric("Hidden opportunities", len(opportunities))

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
    col1.metric("Keyword", summary["keyword"] or "No keyword yet")
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
            with st.spinner("Scanning products..."):
                products = scan_keyword(keyword.strip())
                imported_count = 0

                for product in products:
                    was_inserted = add_product(
                        product["title"],
                        product["platform"],
                        product["price"],
                        product["reviews"],
                        product.get("rating", 0),
                    )

                    if was_inserted:
                        imported_count += 1

            st.success(
                f"Imported {imported_count} new products for '{keyword}'."
            )
            st.rerun()


def render_product_table(df):
    styled_df = df.style.map(
        competition_badge,
        subset=["Competition"]
    )

    st.dataframe(
        styled_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Price": st.column_config.NumberColumn("Price", format="$%.2f"),
            "Rating": st.column_config.NumberColumn("Rating", format="%.1f"),
            "Score": st.column_config.ProgressColumn(
                "Score",
                min_value=0,
                max_value=100,
                format="%d"
            ),
        }
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

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Platform", item["platform"])
            col2.metric("Price", f"${item['price']:.2f}")
            col3.metric("Reviews", item["reviews"])
            col4.metric("Rating", item["rating"])

            st.write(f"**Competition:** {item['score']['competition']}")
            st.write("**Reasons:**")

            for reason in item["reasons"]:
                st.write(f"- {reason}")

            st.markdown("</div>", unsafe_allow_html=True)


create_database()
load_css()

products = get_products()
rows = build_product_rows(products)
opportunities = find_hidden_opportunities(products)
kpis = get_kpi_values(products, rows, opportunities)
trends_keyword = get_trends_keyword(rows)
trend_summary = get_google_trend_summary(trends_keyword)

render_header()
render_sidebar(products, rows, opportunities)

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
    render_product_table(df)
    render_hidden_opportunities(opportunities)
else:
    render_google_trends_card(trend_summary)
    st.info("Scan a keyword to begin.")
