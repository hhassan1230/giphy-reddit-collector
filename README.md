# Giphy Reddit GIF Data Collector

Builds and serves a growing catalog of unique GIF posts from
[r/gifs](https://www.reddit.com/r/gifs). Sourced directly from Reddit's
public JSON endpoint and updated daily via GitHub Actions.

## Overview

- Daily run at 04:00 UTC fetches the current top of `r/gifs` from
  `https://www.reddit.com/r/gifs.json?limit=75`.
- Posts whose `data.id` is already in the catalog are skipped; only
  new posts are appended.
- If the Reddit fetch fails (network error, rate limit, malformed
  response), the run exits cleanly without modifying any files.
- The catalog grows forever (no cap).

## Files

- `data.json`: the full catalog, formatted with indentation (human-readable).
- `latest.json`: byte-equivalent payload, unindented — this is the file
  consumers should fetch from raw.githubusercontent.com.
- `fetch_data.py`: daily collection script.
- `compact_data.py`: legacy one-shot from the old archive-format era;
  kept for reference but no longer applicable to the current schema.
- `.github/workflows/main.yml`: GitHub Actions schedule and commit step.

## Schema

Both `data.json` and `latest.json` mirror Reddit's standard listing
envelope so that consumers handle the same shape they'd get from the
upstream endpoint:

```json
{
  "kind": "Listing",
  "data": {
    "modhash": "",
    "geo_filter": "",
    "after": null,
    "before": null,
    "dist": 176,
    "children": [
      { "kind": "t3", "data": { "id": "abc123", "title": "...", "url": "...", "...": "..." } }
    ]
  }
}
```

`dist` is kept in sync with `len(children)` on every write.

## Consumer URL

```
https://raw.githubusercontent.com/hhassan1230/giphy-reddit-collector/main/latest.json
```

CORS-open. Cache-Control: 5 minutes.

## Setup

No configuration needed — the workflow runs on schedule. Manual runs
can be triggered from the Actions tab via `workflow_dispatch`.

## Author

Created by @hhassan1230
