# AI Briefing Agent

Automatisierter Daily Briefing Agent für KI- und Technologie-News.

## Features

- RSS-Feed Parsing und Web-Scraping
- Automatische Kategorisierung nach Themengebieten
- Deduplizierung ähnlicher Artikel
- Priorisierung (Breaking / Wichtig / Lesenswert)
- Markdown-formatierte Ausgabe

## Projektstruktur

```
ai-briefing/
├── src/
│   ├── main.py              # Entry Point
│   ├── scrapers/
│   │   ├── rss_scraper.py   # RSS-Feed Parser
│   │   └── web_scraper.py   # Web-Scraper
│   ├── processors/
│   │   ├── categorizer.py   # Kategorisierung
│   │   └── summarizer.py    # Zusammenfassungen
│   └── output/
│       └── formatter.py     # Markdown-Output
├── config/
│   └── sources.yaml         # Quellen-Konfiguration
├── data/
│   └── cache.json           # Artikel-Cache
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Verwendung

```bash
python src/main.py
```

## Kategorien

| Emoji | Kategorie |
|-------|-----------|
| 🤖 | KI Global |
| 🇪🇺 | Europa |
| 🇩🇪 | Deutschland |
| 🏛️ | Öffentliche Verwaltung |
| ⚖️ | Regulierung & Recht |
| 💼 | Wirtschaft & Startups |
| 🔬 | Forschung |

## Quellen

### Primär
- Superhuman AI
- DeepLearning.AI - The Batch
- EU AI Act Newsletter
- The Decoder
- T3n
- Heise KI
- Zeit - KI
- Süddeutsche - KI

### Zusätzlich
- Netzpolitik.org
- Golem.de
- eGovernment Computing
- EU Digital Strategy
- TechCrunch AI
- The Verge AI
- Anthropic News

## Version

v1.0 - Januar 2026
