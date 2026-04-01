"""
Pattern 7: Feature Flag Gating in Prompts
==========================================

Production AI agents use feature flags to control which
prompt sections are active. This enables:
- Gradual rollout of new behaviors
- A/B testing of prompt variations
- Instant rollback if a behavior causes issues
- Internal-only features before public launch

KEY INSIGHT: In production, 30+ features were found behind
flags, including autonomous agent mode, dream/imagination
capabilities, coordinator mode, and verification agents.
"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class FeatureFlag:
    """A feature flag that controls a prompt section."""
    name: str
    description: str
    enabled: bool = False
    internal_only: bool = False


class FeatureFlagRegistry:
    """
    Registry of feature flags that control prompt behavior.

    In production, these are evaluated at build time via
    dead code elimination — disabled features are stripped
    from the final bundle entirely.
    """

    def __init__(self):
        self._flags: dict[str, FeatureFlag] = {}

    def register(self, flag: FeatureFlag) -> None:
        self._flags[flag.name] = flag

    def is_enabled(self, name: str) -> bool:
        flag = self._flags.get(name)
        return flag.enabled if flag else False

    def get_all(self) -> list[FeatureFlag]:
        return list(self._flags.values())

    def get_enabled(self) -> list[FeatureFlag]:
        return [f for f in self._flags.values() if f.enabled]


# ── Production feature flags (identified in leaked source) ──

def create_production_registry() -> FeatureFlagRegistry:
    """
    Feature flags found in a major AI coding tool.
    These control which prompt sections and behaviors are active.
    """
    registry = FeatureFlagRegistry()

    # ── Agent modes ──
    registry.register(FeatureFlag(
        "COORDINATOR_MODE",
        "Top-level orchestrator that delegates to worker agents",
        internal_only=True,
    ))
    registry.register(FeatureFlag(
        "VERIFICATION_AGENT",
        "Adversarial agent that independently verifies implementation",
        internal_only=True,
    ))

    # ── Autonomous / Proactive ──
    registry.register(FeatureFlag(
        "KAIROS",
        "Autonomous agent mode — acts without being asked",
        internal_only=True,
    ))
    registry.register(FeatureFlag(
        "KAIROS_DREAM",
        "Dream skill — agent imagines/generates proactively",
        internal_only=True,
    ))
    registry.register(FeatureFlag(
        "KAIROS_BRIEF",
        "Proactive summaries and briefings",
        internal_only=True,
    ))
    registry.register(FeatureFlag(
        "PROACTIVE",
        "Agent anticipates user needs",
        internal_only=True,
    ))

    # ── Context management ──
    registry.register(FeatureFlag(
        "CONTEXT_COLLAPSE",
        "Intelligent context compression when approaching limits",
    ))
    registry.register(FeatureFlag(
        "HISTORY_SNIP",
        "Smart history trimming to save context space",
    ))
    registry.register(FeatureFlag(
        "CACHED_MICROCOMPACT",
        "Cache-friendly message compaction",
    ))
    registry.register(FeatureFlag(
        "TOKEN_BUDGET",
        "User-specified token targets (+500K, spend 2M tokens)",
    ))

    # ── Security ──
    registry.register(FeatureFlag(
        "BASH_CLASSIFIER",
        "ML classifier for bash command safety",
        internal_only=True,
    ))
    registry.register(FeatureFlag(
        "TRANSCRIPT_CLASSIFIER",
        "Classifies conversation transcripts",
        internal_only=True,
    ))

    # ── Infrastructure ──
    registry.register(FeatureFlag(
        "BG_SESSIONS",
        "Background sessions that persist",
    ))
    registry.register(FeatureFlag(
        "BRIDGE_MODE",
        "Bridge mode for remote connections",
    ))
    registry.register(FeatureFlag(
        "CHICAGO_MCP",
        "New MCP server integration system",
        internal_only=True,
    ))
    registry.register(FeatureFlag(
        "MONITOR_TOOL",
        "Real-time monitoring tool",
        internal_only=True,
    ))
    registry.register(FeatureFlag(
        "WORKFLOW_SCRIPTS",
        "Automated workflow script execution",
        internal_only=True,
    ))

    # ── Skills ──
    registry.register(FeatureFlag(
        "EXPERIMENTAL_SKILL_SEARCH",
        "Automatic skill discovery and suggestion",
    ))
    registry.register(FeatureFlag(
        "AGENT_TRIGGERS",
        "Automatic agent triggers based on events",
        internal_only=True,
    ))

    return registry


def gated_prompt_section(
    registry: FeatureFlagRegistry,
    flag_name: str,
    compute: Callable[[], str],
) -> str | None:
    """
    Return a prompt section only if its feature flag is enabled.

    In production, the build system does this at compile time
    via dead code elimination. At runtime, disabled flags
    produce zero overhead.
    """
    if registry.is_enabled(flag_name):
        return compute()
    return None


# ── Demo ──
if __name__ == "__main__":
    registry = create_production_registry()

    print("=" * 60)
    print("  FEATURE FLAGS IN PRODUCTION AI AGENTS")
    print("=" * 60)

    all_flags = registry.get_all()
    internal = [f for f in all_flags if f.internal_only]
    public = [f for f in all_flags if not f.internal_only]

    print(f"\nTotal flags: {len(all_flags)}")
    print(f"Internal-only: {len(internal)}")
    print(f"Public: {len(public)}")

    print(f"\n{'─'*60}")
    print("  INTERNAL-ONLY FLAGS (not available to public users)")
    print(f"{'─'*60}")
    for f in internal:
        status = "ON" if f.enabled else "OFF"
        print(f"  [{status:3s}] {f.name:30s} {f.description}")

    print(f"\n{'─'*60}")
    print("  PUBLIC FLAGS")
    print(f"{'─'*60}")
    for f in public:
        status = "ON" if f.enabled else "OFF"
        print(f"  [{status:3s}] {f.name:30s} {f.description}")
