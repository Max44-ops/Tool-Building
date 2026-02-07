"""
Web Scraper für AI Briefing Agent
Fallback für Seiten ohne RSS-Feed
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
import hashlib
from urllib.parse import urljoin, urlparse


class WebScraper:
    """Scraper für Webseiten ohne RSS-Feed"""

    def __init__(self, max_age_hours: int = 48):
        self.max_age_hours = max_age_hours
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8'
        }
        self.timeout = 30

    def fetch_articles(self, source: Dict) -> List[Dict]:
        """
        Holt Artikel von einer Webseite

        Args:
            source: Quellen-Konfiguration mit url, name

        Returns:
            Liste von Artikel-Dictionaries
        """
        url = source.get('url', '')
        source_name = source.get('name', 'Unknown')
        source_type = source.get('type', 'web')

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # Je nach Quelle unterschiedliche Parser verwenden
            if 'substack' in url.lower():
                articles = self._parse_substack(soup, url, source_name)
            elif 'anthropic' in url.lower():
                articles = self._parse_anthropic(soup, url, source_name)
            elif 'superhuman.ai' in url.lower():
                articles = self._parse_superhuman(soup, url, source_name)
            elif 'deeplearning.ai' in url.lower():
                articles = self._parse_deeplearning(soup, url, source_name)
            elif 'zeit.de' in url.lower():
                articles = self._parse_zeit(soup, url, source_name)
            elif 'sueddeutsche' in url.lower():
                articles = self._parse_sueddeutsche(soup, url, source_name)
            elif 'egovernment-computing' in url.lower():
                articles = self._parse_generic(soup, url, source_name)
            elif 'digital-strategy.ec.europa.eu' in url.lower():
                articles = self._parse_eu_digital(soup, url, source_name)
            else:
                articles = self._parse_generic(soup, url, source_name)

            return articles

        except requests.exceptions.Timeout:
            return [{
                'error': True,
                'source': source_name,
                'message': 'Timeout beim Abrufen'
            }]
        except requests.exceptions.RequestException as e:
            return [{
                'error': True,
                'source': source_name,
                'message': f'Netzwerkfehler: {str(e)[:100]}'
            }]
        except Exception as e:
            return [{
                'error': True,
                'source': source_name,
                'message': f'Parsing-Fehler: {str(e)[:100]}'
            }]

    def _parse_substack(self, soup: BeautifulSoup, base_url: str, source_name: str) -> List[Dict]:
        """Parser für Substack-Newsletter"""
        articles = []

        # Substack-Artikel finden
        for item in soup.select('div.post-preview, article.post, div.post-preview-content')[:10]:
            title_elem = item.select_one('a.post-preview-title, h2 a, h3 a')
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            link = urljoin(base_url, title_elem.get('href', ''))

            desc_elem = item.select_one('div.post-preview-description, p.subtitle')
            description = desc_elem.get_text(strip=True) if desc_elem else ''

            articles.append(self._create_article(title, link, description, source_name))

        return articles

    def _parse_anthropic(self, soup: BeautifulSoup, base_url: str, source_name: str) -> List[Dict]:
        """Parser für Anthropic News"""
        articles = []

        for item in soup.select('article, div[class*="post"], div[class*="news-item"], a[href*="/news/"]')[:15]:
            if item.name == 'a':
                title = item.get_text(strip=True)
                link = urljoin(base_url, item.get('href', ''))
                description = ''
            else:
                title_elem = item.select_one('h2, h3, h4, a')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link_elem = item.select_one('a[href]')
                link = urljoin(base_url, link_elem.get('href', '')) if link_elem else base_url

                desc_elem = item.select_one('p, div.description')
                description = desc_elem.get_text(strip=True) if desc_elem else ''

            if title and len(title) > 10:
                articles.append(self._create_article(title, link, description, source_name))

        return articles

    def _parse_superhuman(self, soup: BeautifulSoup, base_url: str, source_name: str) -> List[Dict]:
        """Parser für Superhuman AI Newsletter"""
        articles = []

        for item in soup.select('article, div.post, div[class*="newsletter"]')[:10]:
            title_elem = item.select_one('h1, h2, h3, a.title')
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            link_elem = item.select_one('a[href]')
            link = urljoin(base_url, link_elem.get('href', '')) if link_elem else base_url

            desc_elem = item.select_one('p, div.excerpt, div.summary')
            description = desc_elem.get_text(strip=True) if desc_elem else ''

            articles.append(self._create_article(title, link, description, source_name))

        return articles

    def _parse_deeplearning(self, soup: BeautifulSoup, base_url: str, source_name: str) -> List[Dict]:
        """Parser für DeepLearning.AI The Batch"""
        articles = []

        for item in soup.select('article, div.batch-item, div[class*="post"]')[:10]:
            title_elem = item.select_one('h2, h3, a.title')
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            link_elem = item.select_one('a[href]')
            link = urljoin(base_url, link_elem.get('href', '')) if link_elem else base_url

            desc_elem = item.select_one('p, div.summary')
            description = desc_elem.get_text(strip=True) if desc_elem else ''

            articles.append(self._create_article(title, link, description, source_name))

        return articles

    def _parse_zeit(self, soup: BeautifulSoup, base_url: str, source_name: str) -> List[Dict]:
        """Parser für Zeit Online"""
        articles = []

        for item in soup.select('article, div.teaser, div[class*="zon-teaser"]')[:15]:
            title_elem = item.select_one('h2, h3, span.teaser-headline, a.teaser-link')
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            link_elem = item.select_one('a[href]')
            link = urljoin(base_url, link_elem.get('href', '')) if link_elem else ''

            desc_elem = item.select_one('p.teaser-text, p.summary')
            description = desc_elem.get_text(strip=True) if desc_elem else ''

            if title and link:
                articles.append(self._create_article(title, link, description, source_name))

        return articles

    def _parse_sueddeutsche(self, soup: BeautifulSoup, base_url: str, source_name: str) -> List[Dict]:
        """Parser für Süddeutsche Zeitung"""
        articles = []

        for item in soup.select('article, div.teaser, div[class*="entrylist"]')[:15]:
            title_elem = item.select_one('h2, h3, em.entry-title, a.entry-title')
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            link_elem = item.select_one('a[href]')
            link = urljoin(base_url, link_elem.get('href', '')) if link_elem else ''

            desc_elem = item.select_one('p.entry-summary, p.teaser')
            description = desc_elem.get_text(strip=True) if desc_elem else ''

            if title and link:
                articles.append(self._create_article(title, link, description, source_name))

        return articles

    def _parse_eu_digital(self, soup: BeautifulSoup, base_url: str, source_name: str) -> List[Dict]:
        """Parser für EU Digital Strategy"""
        articles = []

        for item in soup.select('article, div.node, div[class*="news"]')[:10]:
            title_elem = item.select_one('h2, h3, h4, a.title')
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            link_elem = item.select_one('a[href]')
            link = urljoin(base_url, link_elem.get('href', '')) if link_elem else ''

            desc_elem = item.select_one('p, div.field-body')
            description = desc_elem.get_text(strip=True) if desc_elem else ''

            if title and len(title) > 5:
                articles.append(self._create_article(title, link, description, source_name))

        return articles

    def _parse_generic(self, soup: BeautifulSoup, base_url: str, source_name: str) -> List[Dict]:
        """Generischer Parser für unbekannte Seiten"""
        articles = []

        # Versuche verschiedene Selektoren
        selectors = [
            'article',
            'div.post',
            'div.article',
            'div.entry',
            'div[class*="teaser"]',
            'li.post-item',
        ]

        for selector in selectors:
            items = soup.select(selector)[:10]
            if items:
                for item in items:
                    title_elem = item.select_one('h1, h2, h3, h4, a.title, a[class*="title"]')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    if len(title) < 10:
                        continue

                    link_elem = item.select_one('a[href]')
                    link = urljoin(base_url, link_elem.get('href', '')) if link_elem else ''

                    desc_elem = item.select_one('p, div.excerpt, div.summary, div.description')
                    description = desc_elem.get_text(strip=True) if desc_elem else ''

                    if title and link:
                        articles.append(self._create_article(title, link, description, source_name))

                if articles:
                    break

        return articles

    def _create_article(self, title: str, link: str, description: str, source_name: str) -> Dict:
        """Erstellt ein standardisiertes Artikel-Dictionary"""
        article_id = hashlib.md5((link + title).encode()).hexdigest()[:12]

        return {
            'id': article_id,
            'title': title.strip(),
            'link': link,
            'description': description[:500] if description else '',
            'source': source_name,
            'published': None,  # Web-Scraping hat oft kein genaues Datum
            'scraped_at': datetime.now().isoformat()
        }
