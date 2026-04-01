"""
Pattern 2: Conditional Behavior (User-Type Gating)
===================================================

Production AI agents serve DIFFERENT instructions to different
user types. Internal employees get stricter anti-hallucination
rules, verbose communication guidelines, and internal tooling.
External users get concise responses optimized for token cost.

KEY INSIGHT: The same AI model receives fundamentally different
system prompts depending on who is using it. This means the
"personality" you experience is engineered, not inherent.

This pattern is used in production where:
- Internal users (type='internal') get enhanced instructions
- External users (type='external') get cost-optimized instructions
- The build system eliminates unreachable code paths (dead code elimination)
"""

from enum import Enum
from dataclasses import dataclass


class UserType(Enum):
    INTERNAL = "internal"  # Company employees
    EXTERNAL = "external"  # Public users


@dataclass
class ConditionalRule:
    """A rule that only applies to specific user types."""
    text: str
    user_type: UserType | None = None  # None = applies to everyone
    reason: str = ""  # Why this rule exists


def build_conditional_prompt(
    rules: list[ConditionalRule],
    current_user: UserType,
) -> str:
    """
    Build a prompt with user-type-gated sections.

    Rules with user_type=None apply to everyone.
    Rules with a specific user_type only apply to that type.
    """
    applicable = []
    for rule in rules:
        if rule.user_type is None or rule.user_type == current_user:
            applicable.append(rule.text)
    return "\n".join(f"- {r}" for r in applicable)


# ── Production rules identified in AI coding agents ──

CODING_RULES = [
    # Rules for EVERYONE
    ConditionalRule(
        "Don't add features beyond what was asked.",
    ),
    ConditionalRule(
        "Don't add error handling for impossible scenarios.",
    ),
    ConditionalRule(
        "Three similar lines > a premature abstraction.",
    ),
    ConditionalRule(
        "Never introduce OWASP Top 10 vulnerabilities.",
    ),

    # Rules ONLY for internal users (stricter)
    ConditionalRule(
        "Default to writing NO comments. Only add one when the WHY is "
        "non-obvious: a hidden constraint, a subtle invariant, a workaround.",
        user_type=UserType.INTERNAL,
        reason="Internal model over-comments by default. This corrects it.",
    ),
    ConditionalRule(
        "Before reporting a task complete, VERIFY it actually works: "
        "run the test, execute the script, check the output.",
        user_type=UserType.INTERNAL,
        reason="Counterweight for thoroughness — model skips verification.",
    ),
    ConditionalRule(
        "Report outcomes faithfully. Never claim 'all tests pass' when "
        "output shows failures. Never suppress failing checks to "
        "manufacture a green result.",
        user_type=UserType.INTERNAL,
        reason="Anti-hallucination: 29% false claim rate without this rule.",
    ),
    ConditionalRule(
        "If the user's request is based on a misconception, say so. "
        "You're a collaborator, not just an executor.",
        user_type=UserType.INTERNAL,
        reason="Assertiveness counterweight — model is too compliant.",
    ),
]


TONE_RULES = {
    UserType.EXTERNAL: """# Output Efficiency
Go straight to the point. Be extra concise.
Keep text brief and direct. Lead with the answer, not the reasoning.
If you can say it in one sentence, don't use three.""",

    UserType.INTERNAL: """# Communicating With the User
When sending text, you're writing for a person, not logging to a console.
Assume they stepped away and lost the thread. Write so they can pick back
up cold: use complete sentences without unexplained jargon.
Err on the side of more explanation.
Match responses to the task: a simple question gets a direct answer,
not headers and numbered sections.""",
}


LENGTH_ANCHORS = ConditionalRule(
    "Length limits: keep text between tool calls to <=25 words. "
    "Keep final responses to <=100 words unless the task requires more.",
    user_type=UserType.INTERNAL,
    reason="Research shows ~1.2% output token reduction vs 'be concise'.",
)


# ── Demo ──
if __name__ == "__main__":
    for user_type in UserType:
        print(f"\n{'='*60}")
        print(f"  PROMPT FOR: {user_type.value.upper()} USER")
        print(f"{'='*60}\n")

        # Coding rules
        print("## Coding Rules")
        print(build_conditional_prompt(CODING_RULES, user_type))

        # Tone
        print(f"\n{TONE_RULES[user_type]}")

        # Length anchors (internal only)
        if user_type == UserType.INTERNAL:
            print(f"\n## Numeric Length Anchors")
            print(f"- {LENGTH_ANCHORS.text}")
            print(f"  (Reason: {LENGTH_ANCHORS.reason})")
