# How to Scrape Reddit Data After the RSS and API Shutdown

This repository contains the Python scripts and saved results for **How to Scrape Reddit Data After the RSS and API Shutdown**, a Zenrows article examining how Reddit's public retrieval methods behave and demonstrating how to retrieve publicly accessible Reddit pages with Zenrows Fetch and Extract.

Tests were conducted on **October 21, 2026**, using the **r/Python** subreddit. The repository preserves the resulting files so readers can inspect the retrieved content and reproduce the requests.

## Features

- Tests subreddit RSS, unauthenticated `.json`, and Old Reddit requests.
- Records HTTP status codes, content types, and the number of posts extracted from public-method responses.
- Retrieves a subreddit listing and an individual discussion with Zenrows Fetch using `mode=auto`.
- Saves Fetch responses as Markdown.
- Uses Zenrows Extract with `extract=auto` to retrieve structured information about a discussion, its comments, and the subreddit.
- Includes the original test outputs for inspection.

## Prerequisites

- Python 3.10 or later
- A Zenrows API key for the Fetch and Extract scripts ([create a free account](https://app.zenrows.com/register))

The public-method script does **not** require a Zenrows key or Reddit Data API credentials.

## Installation

Clone the repository:

```bash
git clone https://github.com/Techwithpraisejames/reddit-data-api-research.git
cd reddit-data-api-research
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

The Zenrows scripts read the `ZENROWS_API_KEY` environment variable. The `.env.example` file documents the variable name, but **these scripts do not automatically load a `.env` file**.

Set the key in your terminal before running them:

**Windows Command Prompt**

```bat
set ZENROWS_API_KEY=your_zenrows_api_key
```

**Windows PowerShell**

```powershell
$env:ZENROWS_API_KEY="your_zenrows_api_key"
```

**macOS / Linux**

```bash
export ZENROWS_API_KEY="your_zenrows_api_key"
```

Keep your real API key out of Git and shared terminal output. The repository's `.gitignore` excludes `.env` files.

## Project structure

```text
.
├── results/
│   ├── public_methods.txt
│   ├── reddit_extracted.json
│   ├── reddit_listing.md
│   └── reddit_post.md
├── .env.example
├── .gitignore
├── README.md
├── reddit_public_methods_test.py
├── requirements.txt
├── zenrows_extract.py
└── zenrows_fetch.py
```

- `reddit_public_methods_test.py` checks the RSS feed, unauthenticated JSON endpoint, and Old Reddit listing for r/Python.
- `zenrows_fetch.py` retrieves an r/Python discussion and subreddit listing as Markdown.
- `zenrows_extract.py` requests structured JSON for the same discussion.
- `results/` contains the captured output from the tests; scripts write new files to the directory in which you run them.

## How it works

### 1. Test public Reddit retrieval methods

```bash
python reddit_public_methods_test.py
```

The script checks three URLs for **r/Python**:

| Method | Target |
| --- | --- |
| RSS | `https://www.reddit.com/r/Python/.rss` |
| Unauthenticated JSON | `https://www.reddit.com/r/Python/.json?limit=5` |
| Old Reddit | `https://old.reddit.com/r/Python/` |

For each request, it prints the HTTP status and content type. If the request returns HTTP 200, the script also attempts to extract posts from the response. A successful HTTP status alone does not establish that usable posts were returned.

**Recorded October 21, 2026 results:**

| Method | HTTP status | Extracted posts |
| --- | --- | --- |
| RSS | 200 | 25 |
| Unauthenticated JSON | 403 | None; request rejected |
| Old Reddit | 403 | None; request rejected |

See the [complete terminal output](results/public_methods.txt). These are observations from the tested requests, not a claim that all unauthenticated Reddit requests always fail.

The official Reddit Data API was not tested because the access application was not approved.

### 2. Retrieve Reddit content with Zenrows Fetch

```bash
python zenrows_fetch.py
```

The script requests an [r/Python Sunday Daily Thread](https://www.reddit.com/r/Python/comments/1wr5g87/sunday_daily_thread_whats_everyone_working_on/) and the [r/Python subreddit listing](https://www.reddit.com/r/Python/), using:

- `mode=auto` for automatic retrieval configuration.
- `response_type=markdown` to return Markdown.

It writes `reddit_post.md` and `reddit_listing.md` to your current working directory.

**Saved results:**

- [Discussion Markdown](results/reddit_post.md), including the post and visible comments.
- [Subreddit listing Markdown](results/reddit_listing.md), including post links and other page content.

The discussion output includes a **More replies** link, so it does not establish that every nested reply was retrieved. The subreddit listing also includes navigation, advertisements, and some interface text in Hindi.

### 3. Extract structured Reddit data

```bash
python zenrows_extract.py
```

The script requests the same discussion using `mode=auto` and `extract=auto`. It saves the `parsed` response as `reddit_extracted.json` in your current working directory.

The [saved JSON output](results/reddit_extracted.json) contains three top-level fields: `comments`, `post`, and `subreddit`. It contains **nine comment records**, while the post metadata reports **11 comments**. Some comment depth and parent fields are missing or inconsistent, so do not treat the output as a complete or fully reconstructed comment tree.

## Recorded outputs

| File | Contents |
| --- | --- |
| [`results/public_methods.txt`](results/public_methods.txt) | RSS, unauthenticated JSON, and Old Reddit terminal results |
| [`results/reddit_post.md`](results/reddit_post.md) | Zenrows Fetch output for the discussion |
| [`results/reddit_listing.md`](results/reddit_listing.md) | Zenrows Fetch output for the subreddit listing |
| [`results/reddit_extracted.json`](results/reddit_extracted.json) | Zenrows Extract structured data |

These outputs document the October 21 test. Live Reddit pages and API responses may differ when you rerun the scripts.

## Technologies

- Python
- Requests
- Beautiful Soup
- Python's built-in XML and JSON modules
- Zenrows Fetch and Extract APIs

## Usage and limitations

This repository documents small, read-only tests. It does not provide Reddit OAuth access, guarantee complete comment retrieval, or establish permission to collect or reuse Reddit content. Review Reddit's applicable terms and obtain any required authorization for your intended use.

## Related article

**[How to Scrape Reddit Data After the RSS and API Shutdown](https://www.zenrows.com/blog/how-to-scrape-reddit-data-after-rss-and-api-shutdown)**

*Forthcoming on the Zenrows blog. The URL above is a proposed slug and may change when the article is published.*
