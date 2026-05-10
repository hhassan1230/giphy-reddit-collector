"""One-shot: collapse consecutive duplicate entries in data.json.

Walks entries in order. Drops any entry whose `data` payload hashes equal
to the previous kept entry's `data`. Preserves the first occurrence of
each distinct payload (i.e., the timestamp of the change, not of the
last-seen-unchanged reading).
"""
import hashlib
import json
import os


def payload_hash(payload):
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


def main():
    before_bytes = os.path.getsize('data.json')

    with open('data.json', 'r') as f:
        data = json.load(f)

    entries = data.get("entries", [])
    kept = []
    last_hash = None
    for entry in entries:
        h = payload_hash(entry.get("data"))
        if h != last_hash:
            kept.append(entry)
            last_hash = h

    data["entries"] = kept

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)

    after_bytes = os.path.getsize('data.json')
    removed = len(entries) - len(kept)

    print(f"Entries: {len(entries)} -> {len(kept)} (removed {removed})")
    print(f"Bytes:   {before_bytes:,} -> {after_bytes:,}")
    if before_bytes:
        pct = (1 - after_bytes / before_bytes) * 100
        print(f"Reduction: {pct:.1f}%")


if __name__ == "__main__":
    main()
