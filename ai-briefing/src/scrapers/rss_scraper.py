"""
RSS Feed Scraper für AI Briefing Agent
Verwendet xml.etree für RSS/Atom-Parsing
"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
import hashlib


class RSSscraper:
    """Scraper für RSS/Atom Feeds"""

    def __init__(self, max_age_hours: int = 48):
        self.max_age_hours = max_age_hours
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AIBriefingBot/1.0)'
        }
        self.timeout = 30

        # Namespace-Definitionen für Atom und andere Formate
        self.namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'dc': 'http://purl.org/dc/elements/1.1/',
        }

    def fetch_feed(self, source: Dict) -> List[Dict]:
        """
        Holt Artikel aus einem RSS/Atom Feed

        Args:
            source: Quellen-Konfiguration mit rss_url, name, optional filter

        Returns:
            Liste von Artikel-Dictionaries
        """
        rss_url = source.get('rss_url', source.get('url'))
        source_name = source.get('name', 'Unknown')
        filter_pattern = source.get('filter', '')

        articles = []

        try:
            # Feed abrufen
            response = requests.get(
                rss_url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            # Feed parsen
            content = response.content
            articles = self._parse_feed(content, source_name, filter_pattern)

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
        except ET.ParseError as e:
            return [{
                'error': True,
                'source': source_name,
                'message': f'XML-Parsing-Fehler: {str(e)[:100]}'
            }]
        except Exception as e:
            return [{
                'error': True,
                'source': source_name,
                'message': f'Unbekannter Fehler: {str(e)[:100]}'
            }]

        return articles

    def _parse_feed(self, content: bytes, source_name: str, filter_pattern: str) -> List[Dict]:
        """Parst den Feed-Content"""
        try:
            root = ET.fromstring(content)
        except ET.ParseError:
            # Versuche mit encoding-Deklaration
            content_str = content.decode('utf-8', errors='ignore')
            content_str = re.sub(r'<\?xml[^>]*\?>', '', content_str)
            root = ET.fromstring(content_str.encode('utf-8'))

        articles = []

        # Bestimme Feed-Typ und parse entsprechend
        if root.tag == '{http://www.w3.org/2005/Atom}feed' or root.tag == 'feed':
            articles = self._parse_atom(root, source_name, filter_pattern)
        elif root.tag == 'rss' or root.find('channel') is not None:
            articles = self._parse_rss(root, source_name, filter_pattern)
        else:
            # Versuche generisches Parsing
            articles = self._parse_generic(root, source_name, filter_pattern)

        return articles

    def _parse_rss(self, root: ET.Element, source_name: str, filter_pattern: str) -> List[Dict]:
        """Parst RSS 2.0 Feed"""
        articles = []
        channel = root.find('channel')
        if channel is None:
            return articles

        cutoff = datetime.now() - timedelta(hours=self.max_age_hours)

        for item in channel.findall('item')[:30]:  # Max 30 Artikel
            article = self._parse_rss_item(item, source_name, cutoff, filter_pattern)
            if article:
                articles.append(article)

        return articles

    def _parse_rss_item(self, item: ET.Element, source_name: str, cutoff: datetime,
                        filter_pattern: str) -> Optional[Dict]:
        """Parst ein einzelnes RSS-Item"""
        # Titel
        title_elem = item.find('title')
        title = title_elem.text.strip() if title_elem is not None and title_elem.text else ''
        if not title:
            return None

        # Link
        link_elem = item.find('link')
        link = link_elem.text.strip() if link_elem is not None and link_elem.text else ''
        if not link:
            return None

        # Beschreibung
        description = ''
        for desc_tag in ['description', '{http://purl.org/rss/1.0/modules/content/}encoded']:
            desc_elem = item.find(desc_tag)
            if desc_elem is not None and desc_elem.text:
                description = self._clean_html(desc_elem.text)
                break

        # Datum
        published = None
        for date_tag in ['pubDate', 'dc:date', '{http://purl.org/dc/elements/1.1/}date']:
            date_elem = item.find(date_tag)
            if date_elem is not None and date_elem.text:
                published = self._parse_date(date_elem.text)
                break

        # Filter anwenden
        if filter_pattern:
            search_text = (title + ' ' + description).lower()
            patterns = filter_pattern.lower().split('|')
            if not any(p.strip() in search_text for p in patterns):
                return None

        # ID generieren
        article_id = hashlib.md5((link + title).encode()).hexdigest()[:12]

        return {
            'id': article_id,
            'title': title,
            'link': link,
            'description': description[:500] if description else '',
            'source': source_name,
            'published': published.isoformat() if published else None,
            'scraped_at': datetime.now().isoformat()
        }

    def _parse_atom(self, root: ET.Element, source_name: str, filter_pattern: str) -> List[Dict]:
        """Parst Atom Feed"""
        articles = []
        cutoff = datetime.now() - timedelta(hours=self.max_age_hours)

        # Finde alle entry-Elemente
        entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        if not entries:
            entries = root.findall('entry')

        for entry in entries[:30]:
            article = self._parse_atom_entry(entry, source_name, cutoff, filter_pattern)
            if article:
                articles.append(article)

        return articles

    def _parse_atom_entry(self, entry: ET.Element, source_name: str, cutoff: datetime,
                          filter_pattern: str) -> Optional[Dict]:
        """Parst einen Atom-Entry"""
        ns = '{http://www.w3.org/2005/Atom}'

        # Titel
        title_elem = entry.find(f'{ns}title') or entry.find('title')
        title = title_elem.text.strip() if title_elem is not None and title_elem.text else ''
        if not title:
            return None

        # Link
        link = ''
        link_elem = entry.find(f'{ns}link[@rel="alternate"]') or entry.find(f'{ns}link') or entry.find('link')
        if link_elem is not None:
            link = link_elem.get('href', '')

        if not link:
            return None

        # Beschreibung
        description = ''
        for tag in [f'{ns}summary', f'{ns}content', 'summary', 'content']:
            desc_elem = entry.find(tag)
            if desc_elem is not None and desc_elem.text:
                description = self._clean_html(desc_elem.text)
                break

        # Datum
        published = None
        for tag in [f'{ns}published', f'{ns}updated', 'published', 'updated']:
            date_elem = entry.find(tag)
            if date_elem is not None and date_elem.text:
                published = self._parse_date(date_elem.text)
                break

        # Filter anwenden
        if filter_pattern:
            search_text = (title + ' ' + description).lower()
            patterns = filter_pattern.lower().split('|')
            if not any(p.strip() in search_text for p in patterns):
                return None

        # ID
        article_id = hashlib.md5((link + title).encode()).hexdigest()[:12]

        return {
            'id': article_id,
            'title': title,
            'link': link,
            'description': description[:500] if description else '',
            'source': source_name,
            'published': published.isoformat() if published else None,
            'scraped_at': datetime.now().isoformat()
        }

    def _parse_generic(self, root: ET.Element, source_name: str, filter_pattern: str) -> List[Dict]:
        """Generisches Parsing für unbekannte Feed-Formate"""
        articles = []
        cutoff = datetime.now() - timedelta(hours=self.max_age_hours)

        # Suche nach item oder entry Elementen
        for tag in ['item', 'entry', 'article']:
            items = root.findall('.//' + tag)
            if items:
                for item in items[:30]:
                    article = self._parse_generic_item(item, source_name, filter_pattern)
                    if article:
                        articles.append(article)
                break

        return articles

    def _parse_generic_item(self, item: ET.Element, source_name: str, filter_pattern: str) -> Optional[Dict]:
        """Generisches Item-Parsing"""
        title = ''
        link = ''
        description = ''

        for child in item:
            tag = child.tag.split('}')[-1].lower()  # Entferne Namespace
            text = child.text.strip() if child.text else ''

            if tag == 'title' and not title:
                title = text
            elif tag == 'link':
                link = child.get('href', text)
            elif tag in ['description', 'summary', 'content'] and not description:
                description = self._clean_html(text)

        if not title or not link:
            return None

        if filter_pattern:
            search_text = (title + ' ' + description).lower()
            patterns = filter_pattern.lower().split('|')
            if not any(p.strip() in search_text for p in patterns):
                return None

        article_id = hashlib.md5((link + title).encode()).hexdigest()[:12]

        return {
            'id': article_id,
            'title': title,
            'link': link,
            'description': description[:500] if description else '',
            'source': source_name,
            'published': None,
            'scraped_at': datetime.now().isoformat()
        }

    def _clean_html(self, text: str) -> str:
        """Entfernt HTML-Tags aus Text"""
        if not text:
            return ''
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = re.sub(r'\s+', ' ', clean)
        # Entferne CDATA
        clean = re.sub(r'<!\[CDATA\[|\]\]>', '', clean)
        return clean.strip()

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parst verschiedene Datums-Formate"""
        if not date_str:
            return None

        date_formats = [
            '%a, %d %b %Y %H:%M:%S %z',  # RFC 822
            '%a, %d %b %Y %H:%M:%S %Z',
            '%Y-%m-%dT%H:%M:%S%z',       # ISO 8601
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%f%z',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
        ]

        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                if dt.tzinfo:
                    dt = dt.replace(tzinfo=None)
                return dt
            except ValueError:
                continue

        return None
