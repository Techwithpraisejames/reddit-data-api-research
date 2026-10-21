# pip install requests

import os
import requests

API_KEY = os.environ["ZENROWS_API_KEY"]

urls = {
    "post": "https://www.reddit.com/r/Python/comments/1wr5g87/sunday_daily_thread_whats_everyone_working_on/",
    "listing": "https://www.reddit.com/r/Python/",
}

for name, url in urls.items():
    params = {
        "url": url,
        "apikey": API_KEY,
        "mode": "auto",
        "response_type": "markdown",
    }

    response = requests.get(
        "https://api.zenrows.com/v1/",
        params=params,
        timeout=90,
    )

    response.raise_for_status()

    filename = f"reddit_{name}.md"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.text)

    print(f"{name.capitalize()} saved to {filename}")
