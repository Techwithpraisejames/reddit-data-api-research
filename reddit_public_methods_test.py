"""Test whether public RSS, unauthenticated JSON, and Old Reddit return posts."""

import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup

SUBREDDIT = "Python"
URLS = {
    "RSS": f"https://www.reddit.com/r/{SUBREDDIT}/.rss",
    "JSON": f"https://www.reddit.com/r/{SUBREDDIT}/.json?limit=5",
    "Old Reddit": f"https://old.reddit.com/r/{SUBREDDIT}/",
}
HEADERS = {"User-Agent": "python:reddit-data-research:v1.0 (read-only research)"}


def rss_posts(response):
    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    posts = []
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", namespaces=ns)
        link = entry.find("atom:link", ns)
        if title and link is not None and link.get("href"):
            posts.append((title, link.get("href")))
    return posts


def json_posts(response):
    payload = response.json()
    if not isinstance(payload, dict):
        return []
    return [
        (item["data"]["title"], item["data"].get("permalink"))
        for item in payload.get("data", {}).get("children", [])
        if item.get("kind") == "t3" and item.get("data", {}).get("title")
    ]


def old_reddit_posts(response):
    soup = BeautifulSoup(response.text, "html.parser")
    return [
        (link.get_text(strip=True), link.get("href"))
        for item in soup.select("div.thing.link")
        if (link := item.select_one("a.title")) is not None
    ]


CHECKS = {"RSS": rss_posts, "JSON": json_posts, "Old Reddit": old_reddit_posts}
for method, url in URLS.items():
    print(f"\n--- {method} ---")
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        print("HTTP status:", response.status_code)
        print("Content type:", response.headers.get("Content-Type"))
        if response.status_code != 200:
            print("Useful post data: No")
            print("Reason:", f"HTTP {response.status_code}")
            continue
        posts = CHECKS[method](response)
        print("Useful post data:", "Yes" if posts else "No")
        print("Posts found:", len(posts))
        for title, link in posts[:3]:
            print(f"- {title} | {link}")
        if not posts:
            print("No posts extracted; inspect response before concluding endpoint unavailable.")
    except (requests.RequestException, ValueError, ET.ParseError) as exc:
        print("Test error:", exc)
