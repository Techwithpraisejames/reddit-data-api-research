# Reddit data access research

Read-only Python experiments for a technical article comparing Reddit retrieval methods.

## Scripts

- `reddit_public_methods_test.py`: Tests public RSS, unauthenticated JSON, and Old Reddit by attempting to extract actual posts rather than interpreting HTTP 200 as proof of usable data.
- `zenrows_fetch.py`: Uses Zenrows Fetch to save a public r/Python discussion and subreddit listing as Markdown. Requires `ZENROWS_API_KEY`.
- `zenrows_extract.py`: Uses Zenrows Extract (`extract=auto`) to save structured JSON for the same r/Python discussion. Requires `ZENROWS_API_KEY`.

## Setup

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
python reddit_public_methods_test.py
```

The Reddit OAuth test was removed because the access request was not approved. The public-method checks require no API keys. For upcoming Zenrows experiments, copy `.env.example` to `.env` and supply your own `ZENROWS_API_KEY`. Do not commit `.env`.

To run the Zenrows Fetch script, set `ZENROWS_API_KEY` in your shell, then execute:

```bash
python zenrows_fetch.py
```

This creates `reddit_post.md` and `reddit_listing.md` in your current directory.

To run the Extract script with the same API key:

```bash
python zenrows_extract.py
```

This creates `reddit_extracted.json` in your current directory.

## Recorded results

- [`results/public_methods.txt`](results/public_methods.txt): Raw terminal output from October 21, 2026, for RSS, unauthenticated JSON, and Old Reddit checks against r/Python.
- [`results/reddit_post.md`](results/reddit_post.md): Markdown returned by Zenrows Fetch for the r/Python Sunday Daily Thread.
- [`results/reddit_listing.md`](results/reddit_listing.md): Markdown returned by Zenrows Fetch for the r/Python subreddit listing.
- [`results/reddit_extracted.json`](results/reddit_extracted.json): Structured JSON from Zenrows Extract for the r/Python Sunday Daily Thread. Includes nine comment records; the post metadata reports 11 comments. Some reply metadata is missing or inconsistent.

To reproduce the test with the script's default `SUBREDDIT = "Python"` setting:

```bash
python reddit_public_methods_test.py
```

## Notes

A 403 does not establish permanent shutdown; it only describes the tested request. An HTTP 200 may still return a login or other non-post page. The Old Reddit parser targets the legacy HTML layout; markup changes can cause zero matches. These scripts are small-scale research tools, not scraping infrastructure or a guarantee of Reddit's future availability.
