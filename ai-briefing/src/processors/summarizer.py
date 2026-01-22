"""
Zusammenfasser für AI Briefing Agent
Erstellt kurze Zusammenfassungen der Artikel
"""
from typing import List, Dict
import re
import hashlib


class Summarizer:
    """Erstellt Zusammenfassungen für Artikel"""

    def __init__(self):
        # Füllwörter und irrelevante Phrasen
        self.remove_phrases = [
            'weiterlesen', 'mehr lesen', 'read more', 'click here',
            'jetzt lesen', 'zum artikel', 'hier klicken', 'subscribe',
            'newsletter', 'anmelden', 'registrieren'
        ]

    def summarize(self, article: Dict) -> Dict:
        """
        Erstellt eine Zusammenfassung für einen Artikel

        Da wir keinen externen LLM-API-Zugriff haben, erstellen wir
        eine intelligente Extraktion aus Titel und Beschreibung.

        Args:
            article: Artikel-Dictionary

        Returns:
            Artikel mit summary-Feld
        """
        title = article.get('title', '')
        description = article.get('description', '')

        # Beschreibung bereinigen
        clean_desc = self._clean_description(description)

        # Zusammenfassung erstellen
        if clean_desc and len(clean_desc) > 50:
            # Wenn Beschreibung vorhanden, nutze sie
            summary = self._create_summary_from_description(clean_desc, title)
        else:
            # Ansonsten erweitere den Titel
            summary = self._expand_title(title)

        article['summary'] = summary
        return article

    def _clean_description(self, text: str) -> str:
        """Bereinigt die Beschreibung von Fülltext"""
        if not text:
            return ''

        # Entferne bekannte Phrasen
        clean = text.lower()
        for phrase in self.remove_phrases:
            clean = clean.replace(phrase, '')

        # Original-Case zurück
        clean = text

        # Entferne mehrfache Leerzeichen und Zeilenumbrüche
        clean = re.sub(r'\s+', ' ', clean)

        # Entferne URLs
        clean = re.sub(r'https?://\S+', '', clean)

        # Entferne E-Mail-Adressen
        clean = re.sub(r'\S+@\S+\.\S+', '', clean)

        return clean.strip()

    def _create_summary_from_description(self, description: str, title: str) -> str:
        """Erstellt Zusammenfassung aus der Beschreibung"""
        # Teile in Sätze
        sentences = re.split(r'[.!?]+', description)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        if not sentences:
            return description[:200] + '...' if len(description) > 200 else description

        # Nimm die ersten 2-3 Sätze, max 300 Zeichen
        summary_parts = []
        char_count = 0

        for sentence in sentences[:3]:
            if char_count + len(sentence) > 300:
                break
            summary_parts.append(sentence)
            char_count += len(sentence)

        summary = '. '.join(summary_parts)
        if summary and not summary.endswith('.'):
            summary += '.'

        return summary

    def _expand_title(self, title: str) -> str:
        """Erweitert einen Titel zu einer kurzen Beschreibung"""
        if not title:
            return 'Keine Zusammenfassung verfügbar.'

        # Wenn der Titel schon lang genug ist
        if len(title) > 80:
            return title

        # Füge kontextuelle Information hinzu basierend auf Keywords
        title_lower = title.lower()

        context_additions = {
            'announced': 'wurde angekündigt',
            'launch': 'startet',
            'release': 'wird veröffentlicht',
            'update': 'erhält ein Update',
            'new': 'präsentiert Neuerungen',
            'study': 'laut einer aktuellen Studie',
            'report': 'wie ein neuer Bericht zeigt',
        }

        return title

    def summarize_batch(self, articles: List[Dict]) -> List[Dict]:
        """Erstellt Zusammenfassungen für eine Liste von Artikeln"""
        return [self.summarize(article) for article in articles]

    def deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """
        Entfernt Duplikate basierend auf Titel-Ähnlichkeit

        Returns:
            Deduplizierte Artikel-Liste
        """
        seen_titles = {}
        unique_articles = []

        for article in articles:
            # Normalisiere Titel für Vergleich
            title = article.get('title', '')
            normalized = self._normalize_title(title)

            # Kurzer Hash für Vergleich
            title_hash = hashlib.md5(normalized.encode()).hexdigest()[:8]

            if title_hash not in seen_titles:
                seen_titles[title_hash] = title
                unique_articles.append(article)
            else:
                # Prüfe ob es wirklich ein Duplikat ist (Levenshtein wäre besser)
                existing = seen_titles[title_hash]
                if self._similarity_ratio(normalized, self._normalize_title(existing)) < 0.8:
                    unique_articles.append(article)

        return unique_articles

    def _normalize_title(self, title: str) -> str:
        """Normalisiert einen Titel für Duplikat-Erkennung"""
        # Kleinschreibung
        norm = title.lower()
        # Entferne Sonderzeichen
        norm = re.sub(r'[^\w\s]', '', norm)
        # Entferne mehrfache Leerzeichen
        norm = re.sub(r'\s+', ' ', norm)
        return norm.strip()

    def _similarity_ratio(self, s1: str, s2: str) -> float:
        """Berechnet einfache Ähnlichkeit zwischen zwei Strings"""
        if not s1 or not s2:
            return 0.0

        words1 = set(s1.split())
        words2 = set(s2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)
