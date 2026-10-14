# Reddit data access research

Read-only Python experiments for a technical article comparing Reddit retrieval methods.

## Scripts

- `reddit_api_test.py`: Tests Reddit's official OAuth Data API using an **approved** access token against one public r/SQL discussion. Saves extracted comments and records unexpanded reply IDs. It does **not** automatically expand `more` placeholders.
- `reddit_public_methods_test.py`: Tests public RSS, unauthenticated JSON, and Old Reddit by attempting to extract actual posts rather than interpreting HTTP 200 as proof of usable data.

## Setup

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
python reddit_public_methods_test.py
```

To test the authorized API, obtain access from Reddit and set the environment variable `REDDIT_ACCESS_TOKEN` in your shell (never commit the token):

```bash
python reddit_api_test.py
```

## Notes

A 403 does not establish permanent shutdown; it only describes the tested request. An HTTP 200 may still return a login or other non-post page. The Old Reddit parser targets the legacy HTML layout; markup changes can cause zero matches. These scripts are small-scale research tools, not scraping infrastructure or a guarantee of Reddit's future availability.
