# NicheScanner AI

NicheScanner AI is a small terminal-based Python application for testing print-on-demand niche ideas. It stores product ideas in SQLite, scores them with a simple trend score, analyzes title keywords, classifies product titles into Niche DNA, and exports CSV reports.

Current version: v0.9.1

## Features

- Import sample products.
- Scan a keyword with offline mock market data.
- Store products in `data/nichescanner.db`.
- Show a ranked product report in the terminal.
- Calculate a shared trend score from price and review count.
- Show keyword trends from product titles.
- Show Niche DNA with product type, main topic, subtopic, and detected keyword.
- Export a CSV report to `reports/nichescanner_report.csv`.

## Run

From the project root:

```powershell
python core\main.py
```

The app also resolves its database, report, and knowledge-base files from the project directory, so it can be launched from another working directory by passing the full path to `core\main.py`.

## Project Structure

```text
core/
  main.py                  CLI menu and application flow
  database.py              SQLite database helpers
  scoring.py               Shared trend score calculation
  market_scanner.py        Offline mock keyword scanner
  keyword_analyzer.py      Product title keyword analysis
  report_exporter.py       CSV report export
  config/                  Product category/topic configuration
  engine/                  Product type and topic detection
  knowledge/               JSON knowledge base for Niche DNA

data/
  nichescanner.db          SQLite database

reports/
  nichescanner_report.csv  Exported CSV report
```

## v0.9 Notes

- Added shared scoring in `core/scoring.py`.
- Updated the banner to `NICHE SCANNER AI v0.9`.
- Replaced corrupted terminal symbols with ASCII labels such as `[OK]`, `[ERROR]`, and `[SCAN]`.
- CSV export now includes Niche DNA columns.
- Mock keyword scanning now returns varied product types and platforms.

## v0.9.1 Notes

- Fixed database, report, and knowledge-base paths so the app works from the project root and other working directories.
- Added validation for empty keyword scans.
- Scan imports now report the real number of newly inserted products.
- Added scoring model documentation in `core/scoring.py`.

## Limitations

- The scanner uses mock data only.
- No live marketplace scraping or API integration is included.
- The database schema is unchanged in v0.9.1.
