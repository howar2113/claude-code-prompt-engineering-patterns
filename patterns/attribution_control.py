"""
Pattern 6: Attribution Control (Undercover Mode)
==================================================

Production AI agents need to control WHEN and HOW they reveal
their AI nature. In some contexts (internal repos), full attribution
is fine. In others (public/open-source), the AI must operate
"undercover" to avoid leaking internal information.

KEY INSIGHT: This isn't about deception — it's about information
security. Internal codenames, unreleased model versions, and
project names are confidential. The AI must strip all traces
of internal information from public-facing outputs.

The pattern:
- AUTO mode: Detect repo type (internal vs public) automatically
- FORCED mode: Environment variable override
- NO FORCE-OFF: Safety default is always undercover (conservative)
"""

from dataclasses import dataclass
from enum import Enum


class RepoClass(Enum):
    INTERNAL = "internal"    # Company's own repos
    EXTERNAL = "external"    # Public/open-source repos
    UNKNOWN = "unknown"      # Can't determine → treat as external


class AttributionMode(Enum):
    FULL = "full"            # Include AI attribution
    UNDERCOVER = "undercover"  # Strip all AI traces


# Internal repos where full attribution is safe
INTERNAL_REPO_PATTERNS = [
    "github.com/your-company/",
    "gitlab.internal.company.com/",
]


def classify_repo(remote_url: str | None) -> RepoClass:
    """Classify a git repo as internal or external."""
    if not remote_url:
        return RepoClass.UNKNOWN

    for pattern in INTERNAL_REPO_PATTERNS:
        if pattern in remote_url:
            return RepoClass.INTERNAL

    return RepoClass.EXTERNAL


def get_attribution_mode(
    repo_url: str | None,
    force_undercover: bool = False,
    user_type: str = "external",
) -> AttributionMode:
    """
    Determine attribution mode.

    Logic:
    1. If force_undercover env var is set → UNDERCOVER (always)
    2. If user is internal AND repo is confirmed internal → FULL
    3. Everything else → UNDERCOVER (safe default)

    IMPORTANT: There is NO force-OFF for undercover mode.
    If we're not confident we're in an internal repo, we stay undercover.
    This guards against accidentally leaking internal info.
    """
    if force_undercover:
        return AttributionMode.UNDERCOVER

    if user_type != "internal":
        return AttributionMode.FULL  # External users always get normal attribution

    # For internal users, check repo classification
    repo_class = classify_repo(repo_url)
    if repo_class == RepoClass.INTERNAL:
        return AttributionMode.FULL

    # Unknown or external repo → undercover
    return AttributionMode.UNDERCOVER


# ── Commit message templates ──

NORMAL_COMMIT_SUFFIX = """
Co-Authored-By: AI Assistant <noreply@company.com>"""

UNDERCOVER_INSTRUCTIONS = """## UNDERCOVER MODE — CRITICAL

You are operating in a PUBLIC/OPEN-SOURCE repository.
Your commit messages and PR descriptions MUST NOT contain
ANY internal information. Do not blow your cover.

NEVER include in commits or PRs:
- Internal model codenames (animal names, project names)
- Unreleased model version numbers
- Internal repo or project names
- Internal tooling, Slack channels, or short links
- Any mention that you are an AI
- Any hint of what model or version you are
- Co-Authored-By lines or any attribution

Write commit messages as a human developer would —
describe only what the code change does.

GOOD:
- "Fix race condition in file watcher initialization"
- "Add support for custom key bindings"

BAD (never write these):
- "Fix bug found while testing with Model-X"
- "Generated with AI Assistant"
- "Co-Authored-By: AI <...>"
"""


@dataclass
class CommitConfig:
    """Configuration for commit message generation."""
    mode: AttributionMode
    suffix: str
    extra_instructions: str


def get_commit_config(
    repo_url: str | None,
    force_undercover: bool = False,
    user_type: str = "external",
) -> CommitConfig:
    """Get commit configuration based on attribution mode."""
    mode = get_attribution_mode(repo_url, force_undercover, user_type)

    if mode == AttributionMode.UNDERCOVER:
        return CommitConfig(
            mode=mode,
            suffix="",  # No attribution
            extra_instructions=UNDERCOVER_INSTRUCTIONS,
        )

    return CommitConfig(
        mode=mode,
        suffix=NORMAL_COMMIT_SUFFIX,
        extra_instructions="",
    )


# ── Demo ──
if __name__ == "__main__":
    scenarios = [
        ("Internal user, internal repo", "github.com/your-company/app", "internal"),
        ("Internal user, public repo", "github.com/opensource/project", "internal"),
        ("Internal user, unknown repo", None, "internal"),
        ("External user, any repo", "github.com/user/repo", "external"),
    ]

    for label, repo_url, user_type in scenarios:
        config = get_commit_config(repo_url, user_type=user_type)
        print(f"\n{'─'*50}")
        print(f"Scenario: {label}")
        print(f"Mode: {config.mode.value}")
        print(f"Attribution suffix: {repr(config.suffix.strip()) or '(none)'}")
        if config.extra_instructions:
            print(f"Extra instructions: YES (undercover)")
