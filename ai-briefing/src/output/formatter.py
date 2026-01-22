"""
Markdown Formatter für AI Briefing Agent
Erstellt das finale Briefing-Output
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
            'regulierung',
            'wirtschaft',
            'forschung'
        ]

        self.category_info = {
            'ki_global': {'emoji': '🤖', 'name': 'KI Global'},
            'europa': {'emoji': '🇪🇺', 'name': 'Europa'},
            'deutschland': {'emoji': '🇩🇪', 'name': 'Deutschland'},
            'verwaltung': {'emoji': '🏛️', 'name': 'Öffentliche Verwaltung'},
            'regulierung': {'emoji': '⚖️', 'name': 'Regulierung & Gesetze'},
            'wirtschaft': {'emoji': '💼', 'name': 'Wirtschaft & Startups'},
            'forschung': {'emoji': '🔬', 'name': 'Forschung'}
        }

    def format_briefing(self, grouped_articles: Dict[str, List[Dict]],
                        stats: Dict, failed_sources: List[Dict]) -> str:
        """
        Erstellt das komplette Briefing im Markdown-Format

        Args:
            grouped_articles: Nach Kategorien gruppierte Artikel
            stats: Statistiken (Quellen-Anzahl, Artikel-Anzahl)
            failed_sources: Liste fehlgeschlagener Quellen

        Returns:
            Formatiertes Markdown-Briefing
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
        output.append("# 🤖 KI & Tech Briefing")
        output.append(f"**{date_str}** | Quellen: {stats.get('sources_ok', 0)}/{stats.get('sources_total', 0)} | Artikel: {stats.get('articles_total', 0)}")
        output.append("")
        output.append("---")
        output.append("")

        # Executive Summary
        output.append("## 📌 Executive Summary")
        output.append("")
        output.append("> Die wichtigsten Entwicklungen heute:")
        output.append("")

        top_articles = self._get_top_articles(grouped_articles, 5)
        for i, article in enumerate(top_articles, 1):
            cat_emoji = article.get('categories', [{}])[0].get('emoji', '📰') if article.get('categories') else '📰'
            title = article.get('title', 'Unbekannt')
            # Kürze den Titel wenn nötig
            if len(title) > 80:
                title = title[:77] + '...'
            summary_short = self._get_short_context(article)
            output.append(f"{i}. **{title}** – {summary_short}")

        output.append("")
        output.append("---")
        output.append("")

        # Hauptkategorien
        # Kombiniere Europa und Deutschland
        combined_sections = [
            (['ki_global'], '🤖 KI Global'),
            (['europa', 'deutschland'], '🇪🇺 Europa & 🇩🇪 Deutschland'),
            (['verwaltung'], '🏛️ Öffentliche Verwaltung'),
            (['regulierung'], '⚖️ Regulierung & Gesetze'),
        ]

        for cat_ids, section_title in combined_sections:
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

                # Zeige maximal 5 Artikel pro Sektion
                for article in section_articles[:5]:
                    output.append(self._format_article(article))
                    output.append("")

            output.append("---")
            output.append("")

        # Weitere lesenswerte Artikel (Wirtschaft & Forschung)
        other_articles = []
        for cat_id in ['wirtschaft', 'forschung']:
            other_articles.extend(grouped_articles.get(cat_id, []))

        if other_articles:
            output.append("## 📚 Weitere lesenswerte Artikel")
            output.append("")
            output.append("| Titel | Quelle | Kategorie |")
            output.append("|-------|--------|-----------|")

            for article in other_articles[:10]:
                title = article.get('title', 'Unbekannt')
                if len(title) > 60:
                    title = title[:57] + '...'
                link = article.get('link', '#')
                source = article.get('source', 'Unbekannt')
                cat_emoji = article.get('categories', [{}])[0].get('emoji', '📰') if article.get('categories') else '📰'
                output.append(f"| [{title}]({link}) | {source} | {cat_emoji} |")

            output.append("")
            output.append("---")
            output.append("")

        # Fehlgeschlagene Quellen
        if failed_sources:
            output.append("## ⚠️ Hinweise")
            output.append("")
            output.append("Folgende Quellen konnten nicht abgerufen werden:")
            output.append("")
            for source in failed_sources:
                output.append(f"- **{source.get('source', 'Unbekannt')}**: {source.get('message', 'Unbekannter Fehler')}")
            output.append("")
            output.append("---")
            output.append("")

        # Footer
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        output.append(f"*Generiert: {timestamp} | AI Briefing Agent v1.0*")

        return "\n".join(output)

    def _format_article(self, article: Dict) -> str:
        """Formatiert einen einzelnen Artikel"""
        title = article.get('title', 'Unbekannt')
        source = article.get('source', 'Unbekannt')
        priority = article.get('priority_level', '🟢')
        link = article.get('link', '#')
        summary = article.get('summary', article.get('description', ''))

        # Kürze Summary wenn nötig
        if len(summary) > 300:
            summary = summary[:297] + '...'

        lines = []
        lines.append(f"### {title}")
        lines.append(f"**Quelle:** {source} | **Priorität:** {priority}")
        lines.append("")
        if summary:
            lines.append(summary)
            lines.append("")
        lines.append(f"🔗 [Zum Artikel]({link})")

        return "\n".join(lines)

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

        if not summary:
            return article.get('source', 'Aktuelle Meldung')

        # Nimm den ersten Satz oder die ersten 100 Zeichen
        first_sentence = summary.split('.')[0]
        if len(first_sentence) > 100:
            first_sentence = first_sentence[:97] + '...'

        return first_sentence
