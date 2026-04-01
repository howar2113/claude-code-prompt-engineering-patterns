"""
Pattern 8: Prompt Caching Strategy
====================================

LLM API calls are expensive. Production systems split the
system prompt into static (cacheable) and dynamic (per-turn)
sections. A cache hit on the static prefix saves 90%+ of
input token costs.

KEY INSIGHT: A single misplaced dynamic value in the static
section multiplies cache variants by 2^N (where N = number
of dynamic bits). Production teams track this as a bug class.

Cost impact (real pricing):
- Cache WRITE: $3.75/M tokens (pay once)
- Cache READ:  $0.30/M tokens (pay every turn) ← 90% cheaper
- No cache:    $5.00/M tokens (pay every turn)
"""

from dataclasses import dataclass
from enum import Enum
import hashlib


class CacheScope(Enum):
    GLOBAL = "global"      # Same for ALL users → maximum cache hits
    SESSION = "session"    # Same within a session → good cache hits
    TURN = "turn"          # Changes every turn → no cache benefit


@dataclass
class PromptBlock:
    """A block of the system prompt with cache metadata."""
    name: str
    content: str
    scope: CacheScope

    @property
    def cache_key(self) -> str:
        return hashlib.blake2b(
            self.content.encode(), digest_size=16
        ).hexdigest()


BOUNDARY_MARKER = "__DYNAMIC_BOUNDARY__"


class PromptCacheManager:
    """
    Manages prompt caching by splitting into static and dynamic zones.

    Architecture:
    ┌─────────────────────────────────┐
    │  STATIC PREFIX (global cache)   │  ← Identical for all users
    │  - Identity section             │     Cache key = blake2b hash
    │  - Core rules                   │     Scope: GLOBAL
    │  - Tool instructions            │
    │  - Tone & style                 │
    ├─ ═══ BOUNDARY MARKER ═══ ──────┤
    │  DYNAMIC SUFFIX (per-session)   │  ← Changes per user/turn
    │  - Language preference          │     Scope: SESSION or TURN
    │  - Memory context               │
    │  - MCP server instructions      │
    │  - Feature-gated sections       │
    └─────────────────────────────────┘

    WARNING: Moving a dynamic value ABOVE the boundary breaks
    the cache for ALL users. This is tracked as a bug class
    in production (2^N cache variant multiplication).
    """

    def __init__(self):
        self._static_blocks: list[PromptBlock] = []
        self._dynamic_blocks: list[PromptBlock] = []
        self._cache: dict[str, str] = {}

    def add_static(self, name: str, content: str) -> None:
        self._static_blocks.append(
            PromptBlock(name, content, CacheScope.GLOBAL)
        )

    def add_dynamic(
        self, name: str, content: str, scope: CacheScope = CacheScope.SESSION,
    ) -> None:
        self._dynamic_blocks.append(
            PromptBlock(name, content, scope)
        )

    def build(self) -> dict:
        """
        Build the prompt with cache control markers.

        Returns a structure ready for the API:
        - static_prefix: cacheable, send with cache_control
        - dynamic_suffix: not cacheable, send normally
        """
        static_text = "\n\n".join(b.content for b in self._static_blocks)
        dynamic_text = "\n\n".join(b.content for b in self._dynamic_blocks)

        static_key = hashlib.blake2b(
            static_text.encode(), digest_size=16
        ).hexdigest()

        return {
            "system_prompt_blocks": [
                {
                    "type": "text",
                    "text": static_text,
                    "cache_control": {"type": "ephemeral"},
                    "cache_key": static_key,
                    "scope": "global",
                },
                {
                    "type": "text",
                    "text": BOUNDARY_MARKER,
                },
                {
                    "type": "text",
                    "text": dynamic_text,
                    "scope": "session",
                },
            ],
            "cache_stats": {
                "static_tokens_est": len(static_text) // 4,
                "dynamic_tokens_est": len(dynamic_text) // 4,
                "cache_key": static_key,
            },
        }

    def estimate_savings(self, turns: int = 20) -> dict:
        """
        Estimate cost savings from caching over a session.

        Pricing (per million tokens):
        - No cache:     $5.00 per turn
        - Cache write:  $3.75 (first turn only)
        - Cache read:   $0.30 (subsequent turns)
        """
        static_tokens = sum(len(b.content) // 4 for b in self._static_blocks)
        static_mtok = static_tokens / 1_000_000

        cost_no_cache = static_mtok * 5.00 * turns
        cost_with_cache = (static_mtok * 3.75) + (static_mtok * 0.30 * (turns - 1))
        savings = cost_no_cache - cost_with_cache
        pct = (savings / cost_no_cache * 100) if cost_no_cache > 0 else 0

        return {
            "static_tokens": static_tokens,
            "turns": turns,
            "cost_without_cache": round(cost_no_cache, 4),
            "cost_with_cache": round(cost_with_cache, 4),
            "savings_usd": round(savings, 4),
            "savings_pct": round(pct, 1),
        }


# ── Demo ──
if __name__ == "__main__":
    manager = PromptCacheManager()

    # Static sections (cacheable globally)
    manager.add_static("identity", "You are an AI coding assistant.")
    manager.add_static("rules", """# Rules
- Don't add features beyond what was asked
- Don't add error handling for impossible scenarios
- Read existing code before proposing changes
- Never introduce security vulnerabilities""")
    manager.add_static("tools", """# Tools
- Use Read instead of cat
- Use Edit instead of sed
- Use Grep instead of grep
- Use Bash only for system commands""")
    manager.add_static("tone", """# Tone
Be concise. Lead with the answer. No filler.""")

    # Dynamic sections (per-session)
    manager.add_dynamic("language", "# Language\nAlways respond in French.")
    manager.add_dynamic("memory", "# Memory\n- User is a data scientist")

    # Build
    result = manager.build()

    print("=" * 60)
    print("  PROMPT CACHE ARCHITECTURE")
    print("=" * 60)
    for block in result["system_prompt_blocks"]:
        if block.get("text") == BOUNDARY_MARKER:
            print(f"\n{'═'*60}")
            print("  CACHE BOUNDARY — Static above, Dynamic below")
            print(f"{'═'*60}\n")
        else:
            scope = block.get("scope", "boundary")
            cached = "CACHED" if "cache_control" in block else "NOT CACHED"
            print(f"[{scope:8s}] [{cached:10s}]")
            print(block["text"][:100] + "...")
            print()

    # Cost savings
    stats = manager.estimate_savings(turns=20)
    print(f"{'─'*60}")
    print(f"  COST SAVINGS (over {stats['turns']} turns)")
    print(f"{'─'*60}")
    print(f"  Static tokens:    {stats['static_tokens']:,}")
    print(f"  Without cache:    ${stats['cost_without_cache']}")
    print(f"  With cache:       ${stats['cost_with_cache']}")
    print(f"  Savings:          ${stats['savings_usd']} ({stats['savings_pct']}%)")
