import json
import os

import requests

REDDIT_URL = "https://www.reddit.com/r/gifs.json?limit=75"
USER_AGENT = "giphy-reddit-collector/1.0 (+https://github.com/hhassan1230/giphy-reddit-collector)"
DATA_FILE = "data.json"
LATEST_FILE = "latest.json"


def new_catalog():
    return {
        "kind": "Listing",
        "data": {
            "modhash": "",
            "geo_filter": "",
            "after": None,
            "before": None,
            "dist": 0,
            "children": [],
        },
    }


def load_catalog():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return new_catalog()
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Could not load existing catalog ({e}); starting fresh.")
        return new_catalog()


def fetch_new_data():
    try:
        response = requests.get(
            REDDIT_URL,
            headers={"User-Agent": USER_AGENT},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching data: {e}")
        return None


def is_valid_payload(payload):
    if not isinstance(payload, dict):
        return False
    inner = payload.get("data")
    if not isinstance(inner, dict):
        return False
    children = inner.get("children")
    return isinstance(children, list) and len(children) > 0


def child_id(child):
    if not isinstance(child, dict):
        return None
    inner = child.get("data")
    if not isinstance(inner, dict):
        return None
    return inner.get("id")


def main():
    new_data = fetch_new_data()
    if not is_valid_payload(new_data):
        print("Upstream returned no data or unrecognized shape; "
              "leaving existing files untouched.")
        return

    catalog = load_catalog()
    existing_ids = {child_id(c) for c in catalog["data"]["children"]}

    new_children = [
        child for child in new_data["data"]["children"]
        if (cid := child_id(child)) is not None and cid not in existing_ids
    ]

    if not new_children:
        print("No new gifs since last run; skipping write.")
        return

    catalog["data"]["children"].extend(new_children)
    catalog["data"]["dist"] = len(catalog["data"]["children"])

    with open(DATA_FILE, "w") as f:
        json.dump(catalog, f, indent=2)
    with open(LATEST_FILE, "w") as f:
        json.dump(catalog, f)

    print(f"Added {len(new_children)} new gifs "
          f"(catalog now {catalog['data']['dist']}).")


if __name__ == "__main__":
    main()
