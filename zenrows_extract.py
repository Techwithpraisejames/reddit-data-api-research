# pip install requests

import os
import json
import requests

API_KEY = os.environ["ZENROWS_API_KEY"]

url = ("https://www.reddit.com/r/Python/comments/1wr5g87/sunday_daily_thread_whats_everyone_working_on/")

params = {
    "url": url,
    "apikey": API_KEY,
    "mode": "auto",
    "extract": "auto",
}


response = requests.get(
    "https://api.zenrows.com/v1/",
    params=params,
    timeout=120,
)


response.raise_for_status()


data = response.json()
parsed = data.get("parsed", {})


with open("reddit_extracted.json", "w", encoding="utf-8") as file:
    json.dump(parsed, file, indent=2, ensure_ascii=False)


print("HTTP status:", response.status_code)
print("Extracted fields:", list(parsed.keys()))
print(json.dumps(parsed, indent=2, ensure_ascii=False)[:3000])
print("Saved to reddit_extracted.json")
