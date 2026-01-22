"""
Kategorisierer für AI Briefing Agent
Ordnet Artikel den definierten Kategorien zu
Fokus: KI UND Digitalisierung
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
                    'openai', 'anthropic', 'google ai', 'meta ai', 'microsoft ai',
                    'mistral', 'llm', 'gpt', 'claude', 'gemini', 'llama',
                    'training', 'benchmark', 'chatgpt', 'copilot', 'ai assistant',
                    'large language', 'neural network', 'deep learning',
                    'transformer', 'foundation model', 'multimodal',
                    'gpt-4', 'gpt-5', 'opus', 'sonnet', 'machine learning',
                    'ki-modell', 'sprachmodell', 'reasoning'
                ],
                'priority': 1
            },
            'digitalisierung': {
                'emoji': '💻',
                'name': 'Digitalisierung',
                'keywords': [
                    'digitalisierung', 'digital transformation', 'digitale transformation',
                    'modernisierung', 'automatisierung', 'workflow', 'prozesse',
                    'software', 'saas', 'cloud computing', 'plattform', 'api',
                    'schnittstelle', 'integration', 'legacy', 'migration',
                    'digital first', 'paperless', 'low-code', 'no-code'
                ],
                'priority': 2
            },
            'europa': {
                'emoji': '🇪🇺',
                'name': 'Europa',
                'keywords': [
                    'eu', 'europa', 'brüssel', 'ai act', 'verordnung',
                    'richtlinie', 'european', 'commission', 'parlament',
                    'europäisch', 'eu-kommission', 'union', 'straßburg',
                    'ursula', 'von der leyen', 'breton', 'vestager',
                    'dsa', 'dma', 'digital services act', 'digital markets act'
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
                    'dfki', 'fraunhofer', 'max-planck', 'helmholtz',
                    'bund', 'länder', 'landesregierung'
                ],
                'priority': 2
            },
            'verwaltung': {
                'emoji': '🏛️',
                'name': 'Öffentliche Verwaltung',
                'keywords': [
                    'behörde', 'verwaltung', 'kommune', 'kommunal',
                    'egov', 'e-government', 'bürger', 'amt', 'öffentlich',
                    'public sector', 'bürgerservice', 'onlinezugangsgesetz',
                    'ozg', 'smart city', 'bürgeramt', 'rathaus',
                    'fachverfahren', 'registermodernisierung', 'bund online',
                    'verwaltungsdigitalisierung', 'öffentlicher dienst'
                ],
                'priority': 3
            },
            'cybersecurity': {
                'emoji': '🔒',
                'name': 'IT-Sicherheit & Datenschutz',
                'keywords': [
                    'cybersecurity', 'it-sicherheit', 'sicherheit', 'hack',
                    'angriff', 'cyberangriff', 'ransomware', 'malware',
                    'datenschutz', 'dsgvo', 'gdpr', 'datenleck', 'breach',
                    'bsi', 'kritis', 'verschlüsselung', 'phishing',
                    'vulnerability', 'zero-day', 'firewall', 'authentifizierung'
                ],
                'priority': 3
            },
            'regulierung': {
                'emoji': '⚖️',
                'name': 'Regulierung & Recht',
                'keywords': [
                    'gesetz', 'regulierung', 'compliance', 'audit',
                    'recht', 'verbot', 'vorschrift', 'copyright',
                    'urheberrecht', 'haftung', 'transparenz',
                    'algorithmen-regulierung', 'aufsicht', 'verordnung',
                    'rechtlich', 'gerichtshof', 'urteil', 'klage'
                ],
                'priority': 3
            },
            'infrastruktur': {
                'emoji': '🌐',
                'name': 'Digitale Infrastruktur',
                'keywords': [
                    'cloud', 'rechenzentrum', 'datacenter', 'netz',
                    'breitband', 'glasfaser', '5g', 'infrastruktur',
                    'server', 'hosting', 'aws', 'azure', 'gaia-x',
                    'backbone', 'bandbreite', 'latenz', 'edge computing'
                ],
                'priority': 4
            },
            'wirtschaft': {
                'emoji': '💼',
                'name': 'Wirtschaft & Startups',
                'keywords': [
                    'startup', 'investment', 'funding', 'börse', 'übernahme',
                    'millionen', 'milliarden', 'finanzierung', 'valuation',
                    'series a', 'series b', 'ipo', 'unicorn', 'akquisition',
                    'merger', 'venture capital', 'vc', 'gründer'
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
                'priority': 5
            }
        }

        # Priority-Keywords für Breaking News
        self.breaking_keywords = [
            'launch', 'release', 'ankündigung', 'announced', 'veröffentlicht',
            'neu', 'new', 'breaking', 'exklusiv', 'erstmals', 'revolutionär',
            'durchbruch', 'breakthrough', 'milestone', 'meilenstein',
            'gpt-5', 'claude 4', 'gemini 2', 'startet', 'einführung',
            'cyberangriff', 'datenleck', 'hack', 'sicherheitslücke'
        ]

        # Keywords für wichtige Nachrichten
        self.important_keywords = [
            'update', 'studie zeigt', 'analyse', 'report', 'bericht',
            'warnung', 'kritik', 'bedenken', 'herausforderung',
            'partnerschaft', 'kooperation', 'zusammenarbeit',
            'strategie', 'roadmap', 'reform', 'änderung'
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
            article['primary_category'] = 'digitalisierung'  # Default für allgemeine Tech-News

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
            primary_cat = article.get('primary_category', 'digitalisierung')
            if primary_cat in grouped:
                grouped[primary_cat].append(article)

        # Sortiere jede Gruppe nach Priorität
        priority_order = {'🔴': 0, '🟡': 1, '🟢': 2}
        for cat_id in grouped:
            grouped[cat_id].sort(key=lambda x: priority_order.get(x.get('priority_level', '🟢'), 2))

        return grouped
