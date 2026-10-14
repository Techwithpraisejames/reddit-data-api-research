"""Read-only test of an approved Reddit OAuth application's comment endpoint."""

import json
import os
import requests

POST_ID = "1wvo3my"
TOKEN = os.getenv("REDDIT_ACCESS_TOKEN")

if not TOKEN:
    raise SystemExit("Set REDDIT_ACCESS_TOKEN to an approved OAuth access token.")


def parse_children(children, comments, more_ids):
    for item in children:
        kind = item.get("kind")
        data = item.get("data", {})
        if kind == "more":
            more_ids.extend(data.get("children", []))
        elif kind == "t1":
            comments.append({
                "id": data.get("id"),
                "author": data.get("author"),
                "body": data.get("body"),
                "parent_id": data.get("parent_id"),
            })
            replies = data.get("replies")
            if isinstance(replies, dict):
                parse_children(replies.get("data", {}).get("children", []), comments, more_ids)


response = requests.get(
    f"https://oauth.reddit.com/r/SQL/comments/{POST_ID}",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "python:reddit-data-research:v1.0 (read-only research)",
    },
    params={"limit": 100, "depth": 10, "raw_json": 1},
    timeout=30,
)
print("Status:", response.status_code)
response.raise_for_status()
payload = response.json()
post = payload[0]["data"]["children"][0]["data"]
comments, more_ids = [], []
parse_children(payload[1]["data"]["children"], comments, more_ids)

result = {
    "post_id": POST_ID,
    "title": post.get("title"),
    "reported_comment_count": post.get("num_comments"),
    "retrieved_comment_count": len(comments),
    "unexpanded_comment_ids": more_ids,
    "comments": comments,
}
with open("reddit_api_output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print("Post:", result["title"])
print("Comments retrieved:", len(comments))
print("Unexpanded IDs:", len(more_ids))
print("Saved reddit_api_output.json")
