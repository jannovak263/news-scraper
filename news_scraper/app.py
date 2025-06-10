from flask import Flask, render_template
from db import get_all_articles
import feedparser

app = Flask(__name__)

RSS_FEEDS = {
    "euro": "https://www.euro.cz/rss",
    "tydenik": "https://www.tydenikeuro.cz/rss"
}

def get_articles_from_rss():
    euro_feed = feedparser.parse(RSS_FEEDS["euro"])
    tydenik_feed = feedparser.parse(RSS_FEEDS["tydenik"])
    articles = euro_feed.entries[:5] + tydenik_feed.entries[:5]
    return articles

@app.route("/")
def index():
    articles = get_all_articles()

    if not articles:
        # fallback na RSS
        articles = get_articles_from_rss()

    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)
