#!/usr/bin/env python3
"""
KI-Briefing Web App
Flask-basierte Landing Page für tägliche KI-Briefings
"""
import os
import sys
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request

# Parent-Verzeichnis für imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.main import AIBriefingAgent

app = Flask(__name__)

# Pfad für gespeicherte Briefings
BRIEFINGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'briefings')


def get_briefing_path(date_str):
    """Gibt den Pfad für ein Briefing eines bestimmten Datums zurück"""
    return os.path.join(BRIEFINGS_DIR, f'briefing_{date_str}.json')


def load_briefing(date_str):
    """Lädt ein gespeichertes Briefing"""
    path = get_briefing_path(date_str)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_briefing(date_str, data):
    """Speichert ein Briefing"""
    os.makedirs(BRIEFINGS_DIR, exist_ok=True)
    path = get_briefing_path(date_str)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_available_briefings():
    """Gibt eine Liste aller verfügbaren Briefings zurück"""
    if not os.path.exists(BRIEFINGS_DIR):
        return []

    briefings = []
    for filename in sorted(os.listdir(BRIEFINGS_DIR), reverse=True):
        if filename.startswith('briefing_') and filename.endswith('.json'):
            date_str = filename.replace('briefing_', '').replace('.json', '')
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                briefings.append({
                    'date': date_str,
                    'display_date': date_obj.strftime('%d. %B %Y').replace(
                        'January', 'Januar').replace('February', 'Februar').replace(
                        'March', 'März').replace('May', 'Mai').replace(
                        'June', 'Juni').replace('July', 'Juli').replace(
                        'October', 'Oktober').replace('December', 'Dezember')
                })
            except:
                pass
    return briefings


@app.route('/')
def index():
    """Landing Page"""
    today = datetime.now().strftime('%Y-%m-%d')
    briefings = get_available_briefings()
    current_briefing = load_briefing(today)

    return render_template('index.html',
                         briefings=briefings,
                         current_briefing=current_briefing,
                         today=today)


@app.route('/briefing/<date_str>')
def view_briefing(date_str):
    """Einzelnes Briefing anzeigen"""
    briefing = load_briefing(date_str)
    if not briefing:
        return render_template('error.html', message='Briefing nicht gefunden'), 404

    return render_template('briefing.html', briefing=briefing, date=date_str)


@app.route('/api/generate', methods=['POST'])
def generate_briefing():
    """Generiert ein neues Briefing"""
    try:
        agent = AIBriefingAgent()

        # Briefing generieren
        agent.fetch_all_sources()
        agent.process_articles()

        # Artikel nach Kategorien gruppieren
        grouped = agent.categorizer.group_by_category(agent.articles)

        # Briefing-Daten strukturieren
        today = datetime.now().strftime('%Y-%m-%d')
        briefing_data = {
            'date': today,
            'generated_at': datetime.now().isoformat(),
            'stats': {
                'sources_total': len(agent.successful_sources) + len(agent.failed_sources),
                'sources_ok': len(agent.successful_sources),
                'articles_total': len(agent.articles)
            },
            'failed_sources': agent.failed_sources,
            'categories': {}
        }

        # Kategorien mit Artikeln
        category_names = {
            'ki_global': {'emoji': '🤖', 'name': 'KI Global'},
            'europa': {'emoji': '🇪🇺', 'name': 'KI in Europa'},
            'deutschland': {'emoji': '🇩🇪', 'name': 'KI in Deutschland'},
            'verwaltung': {'emoji': '🏛️', 'name': 'KI im Öffentlichen Sektor'},
            'regulierung': {'emoji': '⚖️', 'name': 'KI-Regulierung & Recht'},
            'wirtschaft': {'emoji': '💼', 'name': 'KI in der Wirtschaft'},
            'forschung': {'emoji': '🔬', 'name': 'KI-Forschung'}
        }

        for cat_id, articles in grouped.items():
            if cat_id in category_names:
                briefing_data['categories'][cat_id] = {
                    'info': category_names[cat_id],
                    'articles': articles[:10]  # Max 10 pro Kategorie
                }

        # Top 5 für Executive Summary
        all_articles = []
        for articles in grouped.values():
            all_articles.extend(articles)

        priority_order = {'🔴': 0, '🟡': 1, '🟢': 2}
        all_articles.sort(key=lambda x: priority_order.get(x.get('priority_level', '🟢'), 2))
        briefing_data['top_articles'] = all_articles[:5]

        # Speichern
        save_briefing(today, briefing_data)

        return jsonify({'success': True, 'date': today})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/briefing/<date_str>')
def api_get_briefing(date_str):
    """API: Briefing als JSON"""
    briefing = load_briefing(date_str)
    if not briefing:
        return jsonify({'error': 'Briefing nicht gefunden'}), 404
    return jsonify(briefing)


@app.route('/api/briefings')
def api_list_briefings():
    """API: Liste aller Briefings"""
    return jsonify(get_available_briefings())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
