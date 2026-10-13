"""Data collection module for Bug-Report Triage Agent (Phase 4).

Fetches GitHub issues for kubernetes/kubernetes across 7 targeted SIG labels,
caches all raw HTTP responses to disk, filters for issues with exactly one sig/*
label to ensure clean classification labels, and saves them to data/raw/issues.jsonl.
"""

import email.utils
import json
import os
from pathlib import Path
import re
import sys
import time

from dotenv import load_dotenv
import httpx

# Load environment variables from .env
load_dotenv()

TARGET_LABELS = [
    "sig/node",
    "sig/network",
    "sig/api-machinery",
    "sig/scheduling",
    "sig/storage",
    "sig/cli",
    "sig/auth",
]

CACHE_DIR = Path("data/cache")
OUTPUT_FILE = Path("data/raw/issues.jsonl")


def get_cache_path(url: str) -> Path:
    """Generate a safe filesystem path for a cached URL."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    # Replace unsafe characters for Windows filesystem
    safe_filename = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", url)
    return CACHE_DIR / f"{safe_filename}.json"


def fetch_with_cache(url: str, headers: dict) -> dict:
    """Fetch JSON data from URL or local cache, handling GitHub rate limits safely."""
    cache_file = get_cache_path(url)

    # 1. Return immediately from cache if available
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to read cache {cache_file} ({e}), refetching...")

    # 2. Fetch from network with rate-limit backoff
    while True:
        try:
            with httpx.Client(headers=headers, timeout=30.0) as client:
                response = client.get(url)

            remaining = response.headers.get("x-ratelimit-remaining")
            reset_ts = response.headers.get("x-ratelimit-reset")
            server_date = response.headers.get("date")

            if server_date:
                try:
                    server_ts = email.utils.parsedate_to_datetime(server_date).timestamp()
                except Exception:
                    server_ts = time.time()
            else:
                server_ts = time.time()

            # Handle rate-limit status codes (403, 429) or exhausted remaining quota
            if response.status_code in (403, 429) or (
                remaining is not None and int(remaining) == 0 and response.status_code != 200
            ):
                if reset_ts:
                    wait_seconds = max(5, int(float(reset_ts) - server_ts) + 4)
                else:
                    wait_seconds = 60
                print(
                    f"\n[Rate Limit Warning] HTTP {response.status_code}. "
                    f"Quota exhausted. Waiting {wait_seconds}s for rate-limit reset...",
                    flush=True,
                )
                time.sleep(wait_seconds)
                continue

            response.raise_for_status()
            data = response.json()

            # Save successful response to disk cache
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Proactive pause if rate-limit window is almost empty
            if remaining is not None and int(remaining) <= 1 and reset_ts:
                wait_seconds = max(5, int(float(reset_ts) - server_ts) + 4)
                print(
                    f"\n[Rate Limit Notice] Search requests remaining: {remaining}. "
                    f"Proactively waiting {wait_seconds}s for reset window...",
                    flush=True,
                )
                time.sleep(wait_seconds)
            else:
                # Polite request spacing to prevent secondary rate-limits
                time.sleep(1.5)

            return data

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (403, 429):
                reset_ts = exc.response.headers.get("x-ratelimit-reset")
                wait_seconds = 60
                if reset_ts:
                    wait_seconds = max(5, int(float(reset_ts) - time.time()) + 4)
                print(
                    f"\n[Rate Limit Warning] HTTP {exc.response.status_code}. "
                    f"Waiting {wait_seconds}s for reset...",
                    flush=True,
                )
                time.sleep(wait_seconds)
                continue
            raise
        except (httpx.RequestError, httpx.TimeoutException) as exc:
            print(f"Network error ({exc}). Retrying in 5 seconds...", flush=True)
            time.sleep(5)


def count_sig_labels(issue: dict) -> list[str]:
    """Extract all sig/* label names attached to an issue."""
    sig_labels = []
    for lbl in issue.get("labels", []):
        name = lbl.get("name", "") if isinstance(lbl, dict) else str(lbl)
        if name.startswith("sig/"):
            sig_labels.append(name)
    return sig_labels


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token or token == "ghp_your_token_here":
        print("Warning: GITHUB_TOKEN not set in .env. API calls will be subject to strict unauthenticated rate limits.")

    headers = {
        "User-Agent": "Bug-Report-Triage-Agent/1.0",
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token.strip()}"

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Starting GitHub Data Collection (Phase 4)")
    print(f"Target Labels: {TARGET_LABELS}")
    print(f"Output File: {OUTPUT_FILE}")
    print("=" * 60)

    label_counts = {label: 0 for label in TARGET_LABELS}
    seen_issue_ids = set()
    total_saved = 0

    # Open issues.jsonl in 'w' mode at start to clear old runs
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
        for label_idx, label in enumerate(TARGET_LABELS, 1):
            print(f"\n[{label_idx}/{len(TARGET_LABELS)}] Fetching label: '{label}'...")

            for page in range(1, 7):
                url = (
                    f"https://api.github.com/search/issues"
                    f'?q=repo:kubernetes/kubernetes+is:issue+label:"{label}"'
                    f"&per_page=100&page={page}"
                )

                cached = get_cache_path(url).exists()
                source_tag = "[CACHE]" if cached else "[NET]"
                print(f"  Page {page}/6 {source_tag} fetching...", end=" ", flush=True)

                data = fetch_with_cache(url, headers)
                items = data.get("items", [])

                if not items:
                    print(f"No items returned on page {page}. Moving to next label.")
                    break

                page_kept = 0
                for issue in items:
                    issue_id = issue.get("id")
                    if issue_id in seen_issue_ids:
                        continue

                    # Filter: keep ONLY issues with exactly 1 sig/* label
                    sigs = count_sig_labels(issue)
                    if len(sigs) == 1:
                        seen_issue_ids.add(issue_id)
                        label_counts[label] += 1
                        page_kept += 1
                        total_saved += 1
                        out_file.write(json.dumps(issue, ensure_ascii=False) + "\n")

                out_file.flush()
                print(f"Items: {len(items)}, Kept (single-SIG): {page_kept} (Label total: {label_counts[label]})")

    print("\n" + "=" * 60)
    print("Data Collection Complete!")
    print("=" * 60)
    print("Final Counts of Valid Single-Label Issues Saved Per Label:")
    for label, count in label_counts.items():
        print(f"  - {label:<22}: {count:>4} issues")
    print("-" * 60)
    print(f"  Total Valid Issues Saved : {total_saved:>4} issues")
    print(f"  Output saved to          : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
