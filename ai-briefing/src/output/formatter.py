"""
Markdown Formatter für AI Briefing Agent
Erstellt das finale Briefing-Output mit Zusammenfassungen und Links
Fokus: KI in allen Bereichen
"""
from typing import List, Dict
from datetime import datetime


class BriefingFormatter:
    """Formatiert das Briefing als Markdown"""

    def __init__(self):
        self.category_order = [
            'ki_global',
            'europa',
            'deutschland',
            'verwaltung',
            'cybersecurity',
            'regulierung',
            'wirtschaft',
            'forschung'
        ]

        self.category_info = {
            'ki_global': {'emoji': '🤖', 'name': 'KI Global'},
            'europa': {'emoji': '🇪🇺', 'name': 'KI in Europa'},
            'deutschland': {'emoji': '🇩🇪', 'name': 'KI in Deutschland'},
            'verwaltung': {'emoji': '🏛️', 'name': 'KI in der Verwaltung'},
            'cybersecurity': {'emoji': '🔒', 'name': 'KI & Sicherheit'},
            'regulierung': {'emoji': '⚖️', 'name': 'KI-Regulierung & Recht'},
            'wirtschaft': {'emoji': '💼', 'name': 'KI in der Wirtschaft'},
            'forschung': {'emoji': '🔬', 'name': 'KI-Forschung'}
        }

    def format_briefing(self, grouped_articles: Dict[str, List[Dict]],
                        stats: Dict, failed_sources: List[Dict]) -> str:
        """
        Erstellt das komplette Briefing im Markdown-Format
        """
        now = datetime.now()
        date_str = now.strftime("%d. %B %Y").replace(
            'January', 'Januar').replace('February', 'Februar').replace(
            'March', 'März').replace('April', 'April').replace(
            'May', 'Mai').replace('June', 'Juni').replace(
            'July', 'Juli').replace('August', 'August').replace(
            'September', 'September').replace('October', 'Oktober').replace(
            'November', 'November').replace('December', 'Dezember')

        # Header
        output = []
        output.append("# 🤖 Daily KI-Briefing")
        output.append(f"**{date_str}** | Quellen: {stats.get('sources_ok', 0)}/{stats.get('sources_total', 0)} | Artikel: {stats.get('articles_total', 0)}")
        output.append("")
        output.append("---")
        output.append("")

        # Executive Summary
        output.append("## 📌 Executive Summary")
        output.append("")
        output.append("> Die wichtigsten KI-Entwicklungen heute:")
        output.append("")

        top_articles = self._get_top_articles(grouped_articles, 5)
        for i, article in enumerate(top_articles, 1):
            title = article.get('title', 'Unbekannt')
            if len(title) > 70:
                title = title[:67] + '...'
            link = article.get('link', '#')
            summary_short = self._get_short_context(article)
            output.append(f"{i}. **[{title}]({link})** – {summary_short}")

        output.append("")
        output.append("---")
        output.append("")

        # Hauptkategorien
        main_sections = [
            (['ki_global'], '🤖 KI Global'),
            (['europa', 'deutschland'], '🇪🇺 KI in Europa & Deutschland'),
            (['verwaltung'], '🏛️ KI im Öffentlichen Sektor'),
            (['regulierung'], '⚖️ KI-Regulierung & Recht'),
        ]

        for cat_ids, section_title in main_sections:
            section_articles = []
            for cat_id in cat_ids:
                section_articles.extend(grouped_articles.get(cat_id, []))

            output.append(f"## {section_title}")
            output.append("")

            if not section_articles:
                output.append("*Heute keine relevanten Meldungen in dieser Kategorie.*")
            else:
                # Sortiere nach Priorität
                priority_order = {'🔴': 0, '🟡': 1, '🟢': 2}
                section_articles.sort(key=lambda x: priority_order.get(x.get('priority_level', '🟢'), 2))

                # Zeige maximal 5 Artikel pro Sektion mit vollständiger Formatierung
                for article in section_articles[:5]:
                    output.append(self._format_article_full(article))
                    output.append("")

            output.append("---")
            output.append("")

        # Weitere lesenswerte Artikel (Wirtschaft & Forschung)
        other_articles = []
        for cat_id in ['wirtschaft', 'forschung']:
            other_articles.extend(grouped_articles.get(cat_id, []))

        if other_articles:
            output.append("## 📚 Weitere KI-News: Wirtschaft & Forschung")
            output.append("")

            for article in other_articles[:8]:
                output.append(self._format_article_compact(article))
                output.append("")

            output.append("---")
            output.append("")

        # Fehlgeschlagene Quellen
        if failed_sources:
            output.append("## ⚠️ Nicht erreichbare Quellen")
            output.append("")
            for source in failed_sources:
                msg = source.get('message', 'Unbekannter Fehler')
                # Kürze die Fehlermeldung
                if len(msg) > 60:
                    msg = msg[:57] + '...'
                output.append(f"- **{source.get('source', 'Unbekannt')}**: {msg}")
            output.append("")
            output.append("---")
            output.append("")

        # Footer
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        output.append(f"*Generiert: {timestamp} | Daily KI-Briefing Agent v1.2*")

        return "\n".join(output)

    def _format_article_full(self, article: Dict) -> str:
        """Formatiert einen Artikel mit vollständiger Zusammenfassung und Link"""
        title = article.get('title', 'Unbekannt')
        source = article.get('source', 'Unbekannt')
        priority = article.get('priority_level', '🟢')
        link = article.get('link', '#')
        summary = article.get('summary', article.get('description', ''))

        # Bereinige und kürze Summary
        summary = self._clean_summary(summary)
        if len(summary) > 350:
            summary = summary[:347] + '...'

        lines = []
        lines.append(f"### {priority} {title}")
        lines.append("")
        if summary:
            lines.append(f"> {summary}")
            lines.append("")
        lines.append(f"**Quelle:** [{source}]({link})")

        return "\n".join(lines)

    def _format_article_compact(self, article: Dict) -> str:
        """Kompakte Formatierung für weitere Artikel"""
        title = article.get('title', 'Unbekannt')
        if len(title) > 70:
            title = title[:67] + '...'
        source = article.get('source', 'Unbekannt')
        priority = article.get('priority_level', '🟢')
        link = article.get('link', '#')
        summary = article.get('summary', article.get('description', ''))

        # Kurze Zusammenfassung
        summary = self._clean_summary(summary)
        if len(summary) > 150:
            summary = summary[:147] + '...'

        lines = []
        lines.append(f"**{priority} [{title}]({link})** ({source})")
        if summary:
            lines.append(f"> {summary}")

        return "\n".join(lines)

    def _clean_summary(self, text: str) -> str:
        """Bereinigt die Zusammenfassung"""
        if not text:
            return ''

        # Entferne HTML-Entities
        text = text.replace('&#8217;', "'").replace('&#8211;', "–")
        text = text.replace('&amp;', '&').replace('&quot;', '"')

        # Entferne "Der Artikel ... erschien zuerst auf ..."
        if 'erschien zuerst auf' in text:
            text = text.split('Der Artikel')[0].strip()

        # Entferne doppelte Leerzeichen
        import re
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _get_top_articles(self, grouped_articles: Dict[str, List[Dict]], count: int) -> List[Dict]:
        """Holt die Top-Artikel für die Executive Summary"""
        all_articles = []
        for cat_id, articles in grouped_articles.items():
            all_articles.extend(articles)

        # Sortiere nach Priorität
        priority_order = {'🔴': 0, '🟡': 1, '🟢': 2}
        all_articles.sort(key=lambda x: priority_order.get(x.get('priority_level', '🟢'), 2))

        # Dedupliziere nach Titel
        seen_titles = set()
        unique = []
        for article in all_articles:
            title_normalized = article.get('title', '').lower()[:50]
            if title_normalized not in seen_titles:
                seen_titles.add(title_normalized)
                unique.append(article)

        return unique[:count]

    def _get_short_context(self, article: Dict) -> str:
        """Erstellt einen kurzen Kontext-Satz für die Executive Summary"""
        summary = article.get('summary', article.get('description', ''))
        summary = self._clean_summary(summary)

        if not summary:
            return article.get('source', 'Aktuelle Meldung')

        # Nimm den ersten Satz oder die ersten 100 Zeichen
        first_sentence = summary.split('.')[0]
        if len(first_sentence) > 100:
            first_sentence = first_sentence[:97] + '...'

        return first_sentence
