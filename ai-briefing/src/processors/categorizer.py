"""
Kategorisierer für AI Briefing Agent
Ordnet Artikel den definierten Kategorien zu
"""
from typing import List, Dict, Tuple
import re


class Categorizer:
    """Kategorisiert Artikel nach Themengebieten"""

    def __init__(self):
        self.categories = {
            'ki_global': {
                'emoji': '🤖',
                'name': 'KI Global',
                'keywords': [
                    'openai', 'anthropic', 'google', 'meta', 'microsoft',
                    'model', 'llm', 'gpt', 'claude', 'gemini', 'mistral',
                    'training', 'benchmark', 'chatgpt', 'copilot', 'ai assistant',
                    'large language', 'neural network', 'deep learning',
                    'transformer', 'foundation model', 'multimodal',
                    'gpt-4', 'gpt-5', 'opus', 'sonnet', 'llama'
                ],
                'priority': 1
            },
            'europa': {
                'emoji': '🇪🇺',
                'name': 'Europa',
                'keywords': [
                    'eu', 'europa', 'brüssel', 'ai act', 'verordnung',
                    'richtlinie', 'european', 'commission', 'parlament',
                    'europäisch', 'eu-kommission', 'union', 'straßburg',
                    'ursula', 'von der leyen', 'breton', 'vestager'
                ],
                'priority': 2
            },
            'deutschland': {
                'emoji': '🇩🇪',
                'name': 'Deutschland',
                'keywords': [
                    'bundesregierung', 'bmi', 'bitkom', 'deutschland',
                    'berlin', 'münchen', 'deutsche', 'bundestag',
                    'ministerium', 'bundesminister', 'bmbf', 'bmwk',
                    'dfki', 'fraunhofer', 'max-planck', 'helmholtz'
                ],
                'priority': 2
            },
            'verwaltung': {
                'emoji': '🏛️',
                'name': 'Öffentliche Verwaltung',
                'keywords': [
                    'behörde', 'verwaltung', 'kommune', 'digitalisierung',
                    'egov', 'bürger', 'amt', 'öffentlich', 'public sector',
                    'bürgerservice', 'onlinezugangsgesetz', 'ozg',
                    'e-government', 'smart city', 'bürgeramt'
                ],
                'priority': 3
            },
            'regulierung': {
                'emoji': '⚖️',
                'name': 'Regulierung & Recht',
                'keywords': [
                    'gesetz', 'regulierung', 'datenschutz', 'dsgvo',
                    'compliance', 'audit', 'recht', 'verbot', 'vorschrift',
                    'gdpr', 'copyright', 'urheberrecht', 'haftung',
                    'transparenz', 'algorithmen-regulierung', 'aufsicht'
                ],
                'priority': 3
            },
            'wirtschaft': {
                'emoji': '💼',
                'name': 'Wirtschaft & Startups',
                'keywords': [
                    'startup', 'investment', 'funding', 'börse', 'übernahme',
                    'millionen', 'milliarden', 'finanzierung', 'valuation',
                    'series a', 'series b', 'ipo', 'unicorn', 'akquisition',
                    'merger', 'venture capital', 'vc'
                ],
                'priority': 4
            },
            'forschung': {
                'emoji': '🔬',
                'name': 'Forschung',
                'keywords': [
                    'studie', 'paper', 'forschung', 'universität',
                    'wissenschaft', 'research', 'forscher', 'experiment',
                    'arxiv', 'peer-review', 'publication', 'journal',
                    'konferenz', 'neurips', 'icml', 'iclr', 'cvpr'
                ],
                'priority': 4
            }
        }

        # Priority-Keywords für Breaking News
        self.breaking_keywords = [
            'launch', 'release', 'ankündigung', 'announced', 'veröffentlicht',
            'neu', 'new', 'breaking', 'exklusiv', 'erstmals', 'revolutionär',
            'durchbruch', 'breakthrough', 'milestone', 'meilenstein',
            'gpt-5', 'claude 4', 'gemini 2'
        ]

        # Keywords für wichtige Nachrichten
        self.important_keywords = [
            'update', 'studie zeigt', 'analyse', 'report', 'bericht',
            'warnung', 'kritik', 'bedenken', 'herausforderung',
            'partnerschaft', 'kooperation', 'zusammenarbeit'
        ]

    def categorize(self, article: Dict) -> Dict:
        """
        Kategorisiert einen einzelnen Artikel

        Args:
            article: Artikel-Dictionary mit title, description

        Returns:
            Artikel mit zusätzlichen Feldern: categories, priority_level
        """
        text = (article.get('title', '') + ' ' + article.get('description', '')).lower()

        # Kategorien finden
        matched_categories = []
        for cat_id, cat_info in self.categories.items():
            for keyword in cat_info['keywords']:
                if keyword.lower() in text:
                    matched_categories.append({
                        'id': cat_id,
                        'emoji': cat_info['emoji'],
                        'name': cat_info['name'],
                        'priority': cat_info['priority']
                    })
                    break

        # Deduplizieren und nach Priorität sortieren
        seen = set()
        unique_categories = []
        for cat in sorted(matched_categories, key=lambda x: x['priority']):
            if cat['id'] not in seen:
                seen.add(cat['id'])
                unique_categories.append(cat)

        # Maximal 2 Kategorien
        article['categories'] = unique_categories[:2]

        # Prioritätslevel bestimmen
        article['priority_level'] = self._determine_priority(text)

        # Primäre Kategorie für Sortierung
        if unique_categories:
            article['primary_category'] = unique_categories[0]['id']
        else:
            article['primary_category'] = 'ki_global'  # Default

        return article

    def _determine_priority(self, text: str) -> str:
        """
        Bestimmt die Prioritätsstufe eines Artikels

        Returns:
            '🔴' für Breaking, '🟡' für Wichtig, '🟢' für Lesenswert
        """
        text_lower = text.lower()

        # Breaking News Check
        for keyword in self.breaking_keywords:
            if keyword in text_lower:
                return '🔴'

        # Wichtige Nachrichten Check
        for keyword in self.important_keywords:
            if keyword in text_lower:
                return '🟡'

        return '🟢'

    def categorize_batch(self, articles: List[Dict]) -> List[Dict]:
        """Kategorisiert eine Liste von Artikeln"""
        return [self.categorize(article) for article in articles]

    def group_by_category(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Gruppiert Artikel nach ihrer primären Kategorie

        Returns:
            Dictionary mit Kategorie-IDs als Keys und Artikel-Listen als Values
        """
        grouped = {cat_id: [] for cat_id in self.categories.keys()}

        for article in articles:
            primary_cat = article.get('primary_category', 'ki_global')
            if primary_cat in grouped:
                grouped[primary_cat].append(article)

        # Sortiere jede Gruppe nach Priorität
        priority_order = {'🔴': 0, '🟡': 1, '🟢': 2}
        for cat_id in grouped:
            grouped[cat_id].sort(key=lambda x: priority_order.get(x.get('priority_level', '🟢'), 2))

        return grouped
