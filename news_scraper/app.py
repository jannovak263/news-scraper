from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_articles(source=None):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if source:
        c.execute('SELECT title, url, source, date_scraped FROM articles WHERE source=? ORDER BY date_scraped DESC', (source,))
    else:
        c.execute('SELECT title, url, source, date_scraped FROM articles ORDER BY date_scraped DESC')
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/articles')
def api_articles():
    source = request.args.get('source')
    articles = get_articles(source)
    return jsonify([
        {'title': r[0], 'url': r[1], 'source': r[2], 'date': r[3]} for r in articles
    ])

if __name__ == '__main__':
    app.run(debug=True)
