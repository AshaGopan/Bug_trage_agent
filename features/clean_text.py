"""Text cleaning utilities for Bug-Report Triage Agent (Phase 5).

Cleans raw issue text by stripping out GitHub issue template boilerplate,
such as HTML comments and markdown section headers, while preserving
meaningful technical descriptions and issue cross-references.
"""

import re
from typing import Optional

# Regex pattern for HTML comments (single-line and multi-line)
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)

# Regex pattern for Markdown headers (e.g., #, ##, ### What happened?, ### Environment)
MARKDOWN_HEADER_PATTERN = re.compile(r"^\s*#{1,6}\s+.*$", re.MULTILINE)

# Pattern for reducing 3+ consecutive newlines to 2
EXCESS_NEWLINES_PATTERN = re.compile(r"\n{3,}")


def clean_issue_body(raw_text: Optional[str]) -> str:
    """Clean the raw body of an issue report.

    Args:
        raw_text: The raw markdown/plain-text body from GitHub API.

    Returns:
        The cleaned text with HTML comments and markdown headers removed,
        trimmed of leading/trailing whitespace.
    """
    if not raw_text:
        return ""

    # 1. Remove HTML comments (<!-- ... -->)
    text = HTML_COMMENT_PATTERN.sub("", raw_text)

    # 2. Remove Markdown headers (e.g., ### What happened?, ### Environment)
    text = MARKDOWN_HEADER_PATTERN.sub("", text)

    # 3. Collapse multiple empty lines and strip surrounding whitespace
    text = EXCESS_NEWLINES_PATTERN.sub("\n\n", text)
    return text.strip()


if __name__ == "__main__":
    sample = (
        "<!-- Template comment -->\n"
        "### What happened?\n"
        "Pod failed to start after kubelet upgrade.\n"
        "### Environment\n"
        "- Kubernetes version: v1.30.0\n"
        "<!-- End of template -->"
    )
    print("Original:\n", sample)
    print("\nCleaned:\n", clean_issue_body(sample))
