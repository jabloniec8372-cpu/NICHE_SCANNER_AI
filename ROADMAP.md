# NicheScanner AI Roadmap

This roadmap describes the planned direction for NicheScanner AI. Completed sections describe what is already in the project. Future sections describe possible next work and should stay small, safe, and beginner-friendly.

## Completed Releases

### v0.9 - GitHub Polish - Completed

Focus: make the project clear, beginner-friendly, and presentable on GitHub.

- Improved README documentation.
- Explained current features and limitations.
- Added project structure documentation.
- Added Windows installation and run instructions.
- Added a clear roadmap.
- Kept the app offline and dependency-free.

### v0.9.1 - Stability Polish - Completed

Focus: make the existing terminal app easier to run from different working directories.

- Fixed project-root path handling for database, reports, and knowledge files.
- Added validation for empty keyword scans.
- Improved import feedback for newly inserted products.
- Added clearer scoring documentation.

### v1.2 - Rating, Competition, And Opportunities - Completed

Focus: improve how users evaluate stored product research.

- Added product rating support.
- Added safe SQLite migration for older databases that do not have the `rating` column.
- Added rating score to the scoring model.
- Added competition labels based on review count.
- Added opportunity labels to scoring output.
- Added Top Niches menu flow.
- Added Hidden Opportunities workflow.
- Expanded CSV export with rating, rating score, competition, and opportunity fields.

### v1.2.1 - GitHub Polish And Documentation - Completed

Focus: document the current v1.2 codebase accurately before future feature work.

- Updated README to describe current features and menu behavior.
- Updated project structure documentation.
- Updated roadmap so future work starts from v1.3.
- Expanded development rules in `AGENTS.md`.
- Kept this release documentation-only.

### v1.3 - CSV Import For Product Research Files - Completed

Focus: let users import their own product research data.

- Added CSV import for product files.
- Added validation for required columns: `title`, `price`, `reviews`, and `rating`.
- Added conversion for price, reviews, and rating values.
- Added safe skipping for invalid CSV rows.
- Added CLI menu support for CSV import.
- Kept compatibility with the current SQLite database.
- Avoided external dependencies.

### v1.4 - Static HTML Dashboard - Completed

Focus: make stored product research easier to review in a browser.

- Added static HTML dashboard generation.
- Added summary cards for total products, average score, best product, and hidden opportunities.
- Added a sortable product table.
- Included score, competition, opportunity, product type, main topic, and subtopic fields.
- Used inline HTML, CSS, and simple JavaScript.
- Kept the feature dependency-free and compatible with the existing SQLite workflow.

### v1.5 - Rich Etsy Product Data - Completed

Focus: improve the optional Etsy integration while keeping mock fallback and older databases working.

- Inspected the live Etsy listing, image, and shop response shapes.
- Stored optional Etsy fields with safe SQLite migrations.
- Imported listing ID, product URL, image URL, shop name, shop URL, currency, and price when available.
- Displayed clickable product links and thumbnails in the Streamlit dashboard.
- Kept CLI, CSV import, mock fallback, and older product rows compatible.

### v1.6.2 - eBay OAuth Credential Priority - Completed

Focus: use fresh production OAuth application tokens from eBay client credentials when they are available.

- Preferred `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET` over the older `EBAY_APPLICATION_TOKEN` value.
- Kept `EBAY_APPLICATION_TOKEN` only as a fallback when OAuth credentials are missing.
- Verified production OAuth and Browse API calls end-to-end through CLI, SQLite, and dashboard export.

### v1.7.1 - Product Type Scan Filter Fix - Completed

Focus: make dashboard Product Types control search queries and current scan results.

- Expanded selected product types into focused dashboard scan queries.
- Scanned only the selected dashboard marketplace platforms.
- Normalized result product types from product titles.
- Filtered current dashboard scan results by selected product type.
- Kept the SQLite schema unchanged.

### v1.6.1 - eBay End-to-End Debug Verification - Completed

Focus: make it easy to prove that eBay Browse API results flow through the CLI, SQLite database, and dashboard output.

- Added eBay connector debug output for connector calls, search URL, status code, raw item count, and mapped product count.
- Added SQLite insert debug output for newly inserted eBay products after keyword scans.
- Added dashboard export debug output for stored eBay product count.
- Kept the existing database schema and marketplace behavior compatible.

### v1.6 - eBay Marketplace Integration - Completed

Focus: add eBay as the next marketplace while keeping the connector system clean and reusable.

- Integrated the official eBay Browse API.
- Added keyword product search for eBay.
- Added temporary `EBAY_APPLICATION_TOKEN` support for application-token testing.
- Kept the existing OAuth client credentials flow for `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET`.
- Normalized Etsy and eBay product models for scanner results.
- Updated the Connector Manager to aggregate Etsy and eBay products.
- Kept mock fallback only when both Etsy and eBay return no products.
- Preserved scoring, dashboard behavior, and database schema compatibility.

## Future Roadmap

### v1.7 - Multi Marketplace Intelligence

Focus: compare marketplaces and identify stronger cross-platform opportunities.

- Cross-platform comparison.
- Compare Etsy vs eBay opportunities.
- Detect products available on multiple marketplaces.
- Unified Opportunity Score.
- Marketplace statistics.
- Platform comparison dashboard.

### v1.8 - Advanced Scoring Engine

Focus: improve scoring quality while keeping the rules transparent and understandable.

- Improved demand scoring.
- Better competition analysis.
- Trend scoring.
- Seasonality detection.
- Sales confidence score.
- Opportunity Score 2.0.

### v2.0 - AI Niche Intelligence

Focus: add optional AI-assisted market intelligence after multi-marketplace support is stable.

- AI-powered niche recommendations.
- AI market summaries.
- AI keyword clustering.
- AI product explanations.
- AI opportunity forecasting.
