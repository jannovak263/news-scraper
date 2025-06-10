import feedparser
import sqlite3
from datetime import datetime

FEEDS = [
    ('https://www.euro.cz/rss', 'euro.cz'),
    ('https://www.tydenikeuro.cz/feed', 'tydenikeuro.cz'),
]

def fetch_articles():
    articles = []
    for url, source in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published = entry.get('published', datetime.now().isoformat())
            articles.append((title, link, source, published))
    return articles

def save_to_db(articles):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT UNIQUE,
            source TEXT,
            date_scraped TEXT
        )
    """)
    for article in articles:
        try:
            c.execute('INSERT INTO articles (title, url, source, date_scraped) VALUES (?, ?, ?, ?)', article)
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()

if __name__ == '__main__':
    articles = fetch_articles()
    save_to_db(articles)
