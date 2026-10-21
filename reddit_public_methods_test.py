import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

SUBREDDIT = "Python"

urls = {
    "RSS": f"https://www.reddit.com/r/{SUBREDDIT}/.rss",
    "JSON": f"https://www.reddit.com/r/{SUBREDDIT}/.json?limit=5",
    "Old Reddit": f"https://old.reddit.com/r/{SUBREDDIT}/",
}

headers = {
    "User-Agent": "python:reddit-data-research:v1.0 (read-only testing)"
}


def check_rss(response):
    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)

    posts = []

    for entry in entries:
        title = entry.findtext("atom:title", namespaces=ns)
        link = entry.find("atom:link", ns)
        url = link.get("href") if link is not None else None

        if title and url:
            posts.append({"title": title, "url": url})

    return posts


def check_json(response):
    data = response.json()

    children = data.get("data", {}).get("children", [])

    return [
        {
            "title": item["data"].get("title"),
            "url": item["data"].get("permalink"),
        }
        for item in children
        if item.get("kind") == "t3"
        and item.get("data", {}).get("title")
    ]


def check_old_reddit(response):
    soup = BeautifulSoup(response.text, "html.parser")

    posts = []

    for item in soup.select("div.thing.link"):
        title = item.select_one("a.title")

        if title:
            posts.append({
                "title": title.get_text(strip=True),
                "url": title.get("href"),
            })

    return posts


checks = {
    "RSS": check_rss,
    "JSON": check_json,
    "Old Reddit": check_old_reddit,
}


for method, url in urls.items():
    print(f"\n--- {method} ---")

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20,
        )

        print("HTTP status:", response.status_code)
        print("Content type:", response.headers.get("Content-Type"))

        if response.status_code != 200:
            print("Useful post data: No")
            print("Reason:", f"HTTP {response.status_code}")
            continue

        posts = checks[method](response)

        print("Useful post data:", "Yes" if posts else "No")
        print("Posts found:", len(posts))

        for post in posts[:3]:
            print("Title:", post["title"])
            print("URL:", post["url"])
            print()

    except (
        requests.RequestException,
        ValueError,
        ET.ParseError,
    ) as error:
        print("Test failed:", error)
