"""Verify candidate repository labels for Bug-Report Triage Agent (Phase 1).

This script queries the GitHub Search API using only Python's standard library
to verify that candidate repositories have enough labeled issues (>= 300 per class)
to support training our leakage-free hybrid Text + Graph classification model.
"""

import email.utils
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Threshold required to ensure each class has sufficient training/validation/test samples
MIN_REQUIRED_ISSUES = 300

# Repositories and candidate area/component labels under evaluation
CANDIDATE_REPOS = {
    "kubernetes/kubernetes": [
        "sig/node",
        "sig/network",
        "sig/api-machinery",
        "sig/scheduling",
        "sig/storage",
        "sig/cli",
        "sig/auth",
    ],
    "rust-lang/rust": [
        "A-diagnostics",
        "A-borrow-checker",
        "A-MIR",
        "A-LLVM",
        "A-traits",
        "A-resolve",
        "A-const-eval",
    ],
}


def build_request(repo: str, label: str, token: str | None) -> urllib.request.Request:
    """Construct an HTTP Request object for the GitHub Search API."""
    query = f'repo:{repo} is:issue label:"{label}"'
    params = urllib.parse.urlencode({"q": query, "per_page": 1})
    url = f"https://api.github.com/search/issues?{params}"

    headers = {
        "User-Agent": "Bug-Report-Triage-Agent/1.0 (academic-research)",
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token.strip()}"

    return urllib.request.Request(url, headers=headers)


def get_server_timestamp(headers) -> float:
    """Extract server timestamp from HTTP Date header to prevent local clock skew."""
    date_header = headers.get("Date") if headers else None
    if date_header:
        try:
            return email.utils.parsedate_to_datetime(date_header).timestamp()
        except Exception:
            pass
    return time.time()


def fetch_label_count(
    repo: str, label: str, token: str | None = None, max_retries: int = 2
) -> tuple[int | None, str | None]:
    """Fetch the total count of issues for a given repo and label.

    Returns:
        (count, None) on success
        (None, error_message) on failure
    """
    for attempt in range(max_retries + 1):
        req = build_request(repo, label, token)
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                remaining_hdr = response.headers.get("x-ratelimit-remaining")
                reset_hdr = response.headers.get("x-ratelimit-reset")
                server_ts = get_server_timestamp(response.headers)

                body = response.read().decode("utf-8")
                data = json.loads(body)
                count = data.get("total_count", 0)

                # If rate limit is nearly exhausted, proactively pause so the next call succeeds
                if remaining_hdr is not None and int(remaining_hdr) <= 1 and reset_hdr:
                    wait_seconds = max(5, int(reset_hdr) - int(server_ts) + 4)
                    if wait_seconds <= 65:
                        print(
                            f"\n  [Rate Limit Notice] Search requests remaining: {remaining_hdr}. "
                            f"Proactively waiting {wait_seconds}s for 60s window reset...",
                            flush=True,
                        )
                        time.sleep(wait_seconds)

                return count, None

        except urllib.error.HTTPError as exc:
            server_ts = get_server_timestamp(exc.headers)
            reset_ts = exc.headers.get("x-ratelimit-reset") if exc.headers else None
            remaining = exc.headers.get("x-ratelimit-remaining") if exc.headers else None
            retry_after = exc.headers.get("Retry-After") if exc.headers else None

            # Handle GitHub rate limit (HTTP 403 or 429)
            if exc.code in (403, 429):
                err_body = ""
                try:
                    err_body = exc.read().decode("utf-8")
                except Exception:
                    pass

                is_rate_limit = (
                    remaining == "0"
                    or "rate limit" in err_body.lower()
                    or "secondary rate limit" in err_body.lower()
                    or exc.code == 429
                )

                if is_rate_limit and attempt < max_retries:
                    if retry_after:
                        wait_seconds = int(retry_after) + 3
                    elif reset_ts:
                        wait_seconds = max(5, int(reset_ts) - int(server_ts) + 4)
                    else:
                        wait_seconds = 15

                    if wait_seconds <= 70:
                        print(
                            f"\n  [Rate Limit HTTP {exc.code}] Pausing {wait_seconds}s before retrying '{label}'... "
                            f"(Tip: Set GITHUB_TOKEN environment variable for higher limit)",
                            flush=True,
                        )
                        time.sleep(wait_seconds)
                        continue

                msg = (
                    f"HTTP {exc.code} Rate Limit: GitHub search API limit reached. "
                    f"Set GITHUB_TOKEN environment variable to increase limit."
                )
                return None, msg

            return None, f"HTTP Error {exc.code}: {exc.reason}"

        except urllib.error.URLError as exc:
            return None, f"Network connection error: {exc.reason}"
        except json.JSONDecodeError:
            return None, "Invalid JSON response received from GitHub API."
        except Exception as exc:
            return None, f"Unexpected error: {str(exc)}"

    return None, "Exceeded retry attempts due to rate limiting."


def verify_repo_labels(
    repo: str, labels: list[str], token: str | None = None
) -> list[dict]:
    """Verify issue counts for all candidate labels in a repository."""
    results = []
    print(f"\nScanning repository: {repo} ({len(labels)} candidate labels)...")

    for idx, label in enumerate(labels, 1):
        print(f"  [{idx}/{len(labels)}] Checking label: '{label}'... ", end="", flush=True)
        count, err = fetch_label_count(repo, label, token=token)

        if count is not None:
            passed = count >= MIN_REQUIRED_ISSUES
            status = "PASSED" if passed else "FAILED"
            print(f"{count:,} issues ({status})", flush=True)
            results.append({
                "label": label,
                "count": count,
                "passed": passed,
                "error": None,
            })
        else:
            print(f"FAILED ({err})", flush=True)
            results.append({
                "label": label,
                "count": None,
                "passed": False,
                "error": err,
            })

        # Polite delay between calls to respect GitHub search rate limits
        time.sleep(1.2)

    return results


def print_summary_table(repo: str, results: list[dict], min_threshold: int) -> None:
    """Print an aligned ASCII summary table for the repository verification results."""
    print("\n" + "=" * 80)
    print(f"VERIFICATION SUMMARY: {repo}")
    print("=" * 80)
    print(f"{'Label':<28} | {'Total Count':>12} | {'Requirement':>12} | {'Status':<10}")
    print("-" * 28 + "-+-" + "-" * 12 + "-+-" + "-" * 12 + "-+-" + "-" * 10)

    passed_count = 0
    total_valid = 0

    for item in results:
        label = item["label"]
        count = item["count"]
        passed = item["passed"]
        error = item["error"]

        if error is not None:
            count_str = "ERROR"
            req_str = f">= {min_threshold}"
            status_str = "ERR / 403"
        else:
            count_str = f"{count:,}"
            req_str = f">= {min_threshold}"
            status_str = "PASSED [OK]" if passed else "LOW COUNT"
            total_valid += 1
            if passed:
                passed_count += 1

        print(f"{label:<28} | {count_str:>12} | {req_str:>12} | {status_str:<10}")

    print("-" * 80)
    pass_pct = (passed_count / len(results) * 100) if results else 0
    print(
        f"Result: {passed_count}/{len(results)} labels qualified "
        f"({pass_pct:.1f}% met requirement >= {min_threshold} issues)"
    )
    print("=" * 80)


def main() -> int:
    token = os.getenv("GITHUB_TOKEN")
    print("=" * 80)
    print("Bug-Report Triage Agent — Phase 1: Repository Label Verification")
    print("=" * 80)
    if token:
        masked = token[:4] + "..." + token[-4:] if len(token) > 8 else "***"
        print(f"Authentication: GITHUB_TOKEN detected ({masked}). Limit is 30 req/min.")
    else:
        print("Authentication: None (Public search, limit is 10 req/min).")
        print("Hint: To query faster without rate limits, set GITHUB_TOKEN environment variable.")

    all_results = {}
    for repo, labels in CANDIDATE_REPOS.items():
        results = verify_repo_labels(repo, labels, token=token)
        all_results[repo] = results

    # Print summary tables
    for repo, results in all_results.items():
        print_summary_table(repo, results, MIN_REQUIRED_ISSUES)

    # Final overall check
    print("\n" + "=" * 80)
    print("FINAL COMPARISON & VERDICT")
    print("=" * 80)
    for repo, results in all_results.items():
        valid_items = [r for r in results if r["passed"]]
        total_issues = sum(r["count"] for r in valid_items if r["count"] is not None)
        print(
            f"  * {repo:<25}: {len(valid_items)}/{len(results)} labels pass threshold. "
            f"Total issues across candidate labels: {total_issues:,}"
        )
    print("=" * 80)
    print("Phase 1 verification script completed successfully.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
