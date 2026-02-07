"""
Kategorisierer für AI Briefing Agent
Ordnet Artikel den definierten Kategorien zu
Fokus: KI in allen Bereichen inkl. Öffentlicher Sektor
"""
from typing import List, Dict, Tuple
import re


class Categorizer:
    """Kategorisiert Artikel nach KI-Themengebieten"""

    def __init__(self):
        # KI-Basis-Keywords die in allen Kategorien relevant sind
        self.ki_base_keywords = [
            'ki', 'ai', 'künstliche intelligenz', 'artificial intelligence',
            'machine learning', 'maschinelles lernen', 'deep learning',
            'llm', 'large language model', 'sprachmodell', 'chatbot',
            'gpt', 'claude', 'gemini', 'llama', 'mistral',
            'openai', 'anthropic', 'deepmind', 'neural', 'algorithmus',
            'automatisierung', 'copilot', 'agent', 'reasoning'
        ]

        self.categories = {
            'ki_global': {
                'emoji': '🤖',
                'name': 'KI Global',
                'keywords': [
                    'openai', 'anthropic', 'google ai', 'meta ai', 'microsoft ai',
                    'mistral', 'llm', 'gpt', 'claude', 'gemini', 'llama',
                    'training', 'benchmark', 'chatgpt', 'copilot', 'ai assistant',
                    'large language', 'neural network', 'deep learning',
                    'transformer', 'foundation model', 'multimodal',
                    'gpt-4', 'gpt-5', 'opus', 'sonnet', 'machine learning',
                    'ki-modell', 'sprachmodell', 'reasoning', 'inference',
                    'parameter', 'token', 'context window', 'fine-tuning',
                    'rlhf', 'alignment', 'safety', 'jailbreak'
                ],
                'priority': 1
            },
            'europa': {
                'emoji': '🇪🇺',
                'name': 'KI in Europa',
                'keywords': [
                    'eu', 'europa', 'brüssel', 'ai act', 'verordnung',
                    'richtlinie', 'european', 'commission', 'parlament',
                    'europäisch', 'eu-kommission', 'union', 'straßburg',
                    'ursula', 'von der leyen', 'breton', 'vestager',
                    'dsa', 'dma', 'digital services act', 'digital markets act',
                    'eu ai office', 'hochrisiko', 'sandbox'
                ],
                'priority': 2
            },
            'deutschland': {
                'emoji': '🇩🇪',
                'name': 'KI in Deutschland',
                'keywords': [
                    'bundesregierung', 'bmi', 'bitkom', 'deutschland',
                    'berlin', 'münchen', 'deutsche', 'bundestag',
                    'ministerium', 'bundesminister', 'bmbf', 'bmwk',
                    'dfki', 'fraunhofer', 'max-planck', 'helmholtz',
                    'bund', 'länder', 'landesregierung', 'ki-strategie',
                    'aleph alpha', 'deepl'
                ],
                'priority': 2
            },
            'verwaltung': {
                'emoji': '🏛️',
                'name': 'KI im Öffentlichen Sektor',
                'keywords': [
                    'behörde', 'verwaltung', 'kommune', 'kommunal',
                    'egov', 'e-government', 'bürger', 'amt', 'öffentlich',
                    'public sector', 'bürgerservice', 'onlinezugangsgesetz',
                    'ozg', 'smart city', 'bürgeramt', 'rathaus',
                    'fachverfahren', 'registermodernisierung',
                    'verwaltungsdigitalisierung', 'öffentlicher dienst',
                    'bundesbehörde', 'landesbehörde', 'staatlich',
                    'government', 'städte', 'gemeinde', 'landkreis',
                    'ministerien', 'ämter', 'jobcenter', 'finanzamt'
                ],
                'priority': 2  # Höhere Priorität für Verwaltung
            },
            'regulierung': {
                'emoji': '⚖️',
                'name': 'KI-Regulierung & Recht',
                'keywords': [
                    'gesetz', 'regulierung', 'compliance', 'audit',
                    'recht', 'verbot', 'vorschrift', 'copyright',
                    'urheberrecht', 'haftung', 'transparenz',
                    'algorithmen-regulierung', 'aufsicht', 'verordnung',
                    'rechtlich', 'gerichtshof', 'urteil', 'klage',
                    'ethik', 'bias', 'diskriminierung', 'fairness'
                ],
                'priority': 3
            },
            'wirtschaft': {
                'emoji': '💼',
                'name': 'KI in der Wirtschaft',
                'keywords': [
                    'startup', 'investment', 'funding', 'börse', 'übernahme',
                    'millionen', 'milliarden', 'finanzierung', 'valuation',
                    'series a', 'series b', 'ipo', 'unicorn', 'akquisition',
                    'merger', 'venture capital', 'vc', 'gründer',
                    'enterprise', 'b2b', 'saas'
                ],
                'priority': 4
            },
            'forschung': {
                'emoji': '🔬',
                'name': 'KI-Forschung',
                'keywords': [
                    'studie', 'paper', 'forschung', 'universität',
                    'wissenschaft', 'research', 'forscher', 'experiment',
                    'arxiv', 'peer-review', 'publication', 'journal',
                    'konferenz', 'neurips', 'icml', 'iclr', 'cvpr',
                    'benchmark', 'evaluation', 'sota', 'state of the art'
                ],
                'priority': 5
            }
        }

        # Priority-Keywords für Breaking News
        self.breaking_keywords = [
            'launch', 'release', 'ankündigung', 'announced', 'veröffentlicht',
            'neu', 'new', 'breaking', 'exklusiv', 'erstmals', 'revolutionär',
            'durchbruch', 'breakthrough', 'milestone', 'meilenstein',
            'gpt-5', 'claude 4', 'gemini 2', 'startet', 'einführung',
            'cyberangriff', 'datenleck', 'hack', 'sicherheitslücke',
            'billion', 'milliarden parameter'
        ]

        # Keywords für wichtige Nachrichten
        self.important_keywords = [
            'update', 'studie zeigt', 'analyse', 'report', 'bericht',
            'warnung', 'kritik', 'bedenken', 'herausforderung',
            'partnerschaft', 'kooperation', 'zusammenarbeit',
            'strategie', 'roadmap', 'reform', 'änderung',
            'compliance', 'regulierung', 'verordnung'
        ]

    def _has_ki_relevance(self, text: str) -> bool:
        """Prüft ob der Artikel KI-relevant ist"""
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.ki_base_keywords)

    def categorize(self, article: Dict) -> Dict:
        """
        Kategorisiert einen einzelnen Artikel
        Nur Artikel mit KI-Bezug werden kategorisiert
        """
        text = (article.get('title', '') + ' ' + article.get('description', '')).lower()

        # Prüfe KI-Relevanz
        if not self._has_ki_relevance(text):
            article['categories'] = []
            article['priority_level'] = '🟢'
            article['primary_category'] = 'ki_global'
            article['ki_relevant'] = False
            return article

        article['ki_relevant'] = True

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
            article['primary_category'] = 'ki_global'

        return article

    def _determine_priority(self, text: str) -> str:
        """Bestimmt die Prioritätsstufe eines Artikels"""
        text_lower = text.lower()

        for keyword in self.breaking_keywords:
            if keyword in text_lower:
                return '🔴'

        for keyword in self.important_keywords:
            if keyword in text_lower:
                return '🟡'

        return '🟢'

    def categorize_batch(self, articles: List[Dict]) -> List[Dict]:
        """Kategorisiert eine Liste von Artikeln"""
        categorized = [self.categorize(article) for article in articles]
        return [a for a in categorized if a.get('ki_relevant', True)]

    def group_by_category(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """Gruppiert Artikel nach ihrer primären Kategorie"""
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
