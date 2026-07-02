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

## Future Roadmap

### v1.5 - Better Trend And Competition Scoring

Focus: improve scoring quality while keeping the rules transparent.

- Review price, review-count, and rating thresholds.
- Improve competition scoring beyond simple review-count labels.
- Consider keyword frequency or product type as additional signals.
- Keep scoring logic reusable and easy to test.

### v2.0 - Optional AI-Assisted Niche Recommendations

Focus: optionally add AI-assisted suggestions after the core research workflow is stable.

- Generate niche ideas from existing product and keyword data.
- Explain why a niche might be promising.
- Keep AI features optional.
- Avoid replacing transparent scoring and keyword analysis with unexplained recommendations.