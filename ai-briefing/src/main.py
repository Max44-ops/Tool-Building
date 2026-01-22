#!/usr/bin/env python3
"""
AI Briefing Agent - Main Entry Point
Sammelt, kategorisiert und formatiert KI/Tech-News
"""
import sys
import os
import yaml
import json
from datetime import datetime
from typing import List, Dict, Tuple

# Füge src zum Path hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers.rss_scraper import RSSscraper
from scrapers.web_scraper import WebScraper
from processors.categorizer import Categorizer
from processors.summarizer import Summarizer
from output.formatter import BriefingFormatter


class AIBriefingAgent:
    """Hauptklasse für den AI Briefing Agent"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), '..', 'config', 'sources.yaml'
        )
        self.rss_scraper = RSSscraper(max_age_hours=168)  # 7 Tage
        self.web_scraper = WebScraper(max_age_hours=168)  # 7 Tage
        self.categorizer = Categorizer()
        self.summarizer = Summarizer()
        self.formatter = BriefingFormatter()

        self.articles = []
        self.failed_sources = []
        self.successful_sources = []

    def load_config(self) -> Dict:
        """Lädt die Quellen-Konfiguration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Fehler beim Laden der Konfiguration: {e}")
            return {'primary_sources': [], 'additional_sources': []}

    def fetch_all_sources(self) -> Tuple[List[Dict], List[Dict]]:
        """
        Ruft alle konfigurierten Quellen ab

        Returns:
            Tuple aus (Artikel-Liste, Fehlgeschlagene-Quellen-Liste)
        """
        config = self.load_config()
        all_sources = config.get('primary_sources', []) + config.get('additional_sources', [])

        articles = []
        failed = []
        successful = []

        print(f"\n📡 Starte Abruf von {len(all_sources)} Quellen...\n")

        for i, source in enumerate(all_sources, 1):
            source_name = source.get('name', 'Unbekannt')
            source_type = source.get('type', 'rss')

            print(f"  [{i}/{len(all_sources)}] {source_name}...", end=" ")

            try:
                if source_type == 'rss' or source.get('rss_url'):
                    result = self.rss_scraper.fetch_feed(source)
                else:
                    result = self.web_scraper.fetch_articles(source)

                # Prüfe auf Fehler
                if result and isinstance(result, list):
                    if result and result[0].get('error'):
                        failed.append(result[0])
                        print(f"❌ {result[0].get('message', 'Fehler')[:50]}")
                    else:
                        valid_articles = [a for a in result if not a.get('error')]
                        articles.extend(valid_articles)
                        successful.append(source_name)
                        print(f"✅ {len(valid_articles)} Artikel")
                else:
                    print("⚠️ Keine Artikel")

            except Exception as e:
                error_info = {
                    'error': True,
                    'source': source_name,
                    'message': str(e)[:100]
                }
                failed.append(error_info)
                print(f"❌ {str(e)[:50]}")

        self.articles = articles
        self.failed_sources = failed
        self.successful_sources = successful

        return articles, failed

    def process_articles(self) -> List[Dict]:
        """Verarbeitet die gesammelten Artikel"""
        if not self.articles:
            return []

        print(f"\n🔄 Verarbeite {len(self.articles)} Artikel...")

        # Deduplizieren
        self.articles = self.summarizer.deduplicate(self.articles)
        print(f"  → Nach Deduplizierung: {len(self.articles)} Artikel")

        # Kategorisieren
        self.articles = self.categorizer.categorize_batch(self.articles)
        print("  → Kategorisierung abgeschlossen")

        # Zusammenfassen
        self.articles = self.summarizer.summarize_batch(self.articles)
        print("  → Zusammenfassungen erstellt")

        return self.articles

    def generate_briefing(self) -> str:
        """Generiert das finale Briefing"""
        print("\n📝 Generiere Briefing...")

        # Artikel nach Kategorien gruppieren
        grouped = self.categorizer.group_by_category(self.articles)

        # Statistiken
        stats = {
            'sources_total': len(self.successful_sources) + len(self.failed_sources),
            'sources_ok': len(self.successful_sources),
            'articles_total': len(self.articles)
        }

        # Formatieren
        briefing = self.formatter.format_briefing(grouped, stats, self.failed_sources)

        return briefing

    def run(self) -> str:
        """Führt den kompletten Briefing-Prozess aus"""
        print("=" * 60)
        print("🤖 DAILY KI-BRIEFING AGENT v1.3")
        print("=" * 60)

        # 1. Quellen abrufen
        articles, failed = self.fetch_all_sources()

        # 2. Verarbeiten
        self.process_articles()

        # 3. Briefing generieren
        briefing = self.generate_briefing()

        # 4. Status ausgeben
        print("\n" + "=" * 60)
        print("📊 ZUSAMMENFASSUNG")
        print("=" * 60)
        print(f"  ✅ Erfolgreiche Quellen: {len(self.successful_sources)}")
        print(f"  ❌ Fehlgeschlagene Quellen: {len(self.failed_sources)}")
        print(f"  📰 Gesammelte Artikel: {len(self.articles)}")
        print("=" * 60)

        return briefing


def main():
    """Hauptfunktion"""
    agent = AIBriefingAgent()
    briefing = agent.run()

    print("\n")
    print("=" * 60)
    print("📰 BRIEFING OUTPUT")
    print("=" * 60)
    print("\n")
    print(briefing)

    return briefing


if __name__ == "__main__":
    main()
