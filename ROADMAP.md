# NicheScanner AI Roadmap

This roadmap describes the planned direction for NicheScanner AI. It does not mean every item is already implemented.

## v0.9 - GitHub Polish

Focus: make the project clear, beginner-friendly, and presentable on GitHub.

- Improve README documentation.
- Explain current features and limitations.
- Add project structure documentation.
- Add Windows installation and run instructions.
- Add a clear roadmap.
- Keep the app offline and dependency-free.

## v1.0 - Real Marketplace Data Research

Focus: move beyond mock data while keeping the app safe and maintainable.

- Research options for real marketplace data sources.
- Prefer official APIs or approved data sources where possible.
- Add clear configuration for any required credentials.
- Preserve the existing mock scanner for local testing.
- Avoid scraping unless explicitly approved and legally appropriate.

## v1.1 - Scoring System

Focus: improve the trend score so it gives more useful product research signals.

- Review the current price and review-count thresholds.
- Add clearer scoring explanations.
- Consider additional signals such as competition level, keyword frequency, or product type.
- Keep scoring logic reusable and easy to test.

## v1.2 - Dashboard And Export Improvements

Focus: improve how users review and export research results.

- Improve CSV export formatting and file naming.
- Consider adding summary statistics.
- Explore a simple dashboard or report view.
- Make exported reports easier to use in spreadsheets.

## v2.0 - Optional AI-Assisted Niche Recommendations

Focus: optionally add AI-assisted suggestions after the core research workflow is stable.

- Generate niche ideas from existing product and keyword data.
- Explain why a niche might be promising.
- Keep AI features optional.
- Avoid replacing transparent scoring and keyword analysis with unexplained recommendations.
