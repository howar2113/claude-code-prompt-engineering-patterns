"""
Pattern 9: Output Efficiency Control
======================================

Production AI agents control response length and style
programmatically, not just with "be concise".

KEY INSIGHT: Qualitative instructions ("be concise") reduce
output tokens by ~0.5%. Numeric anchors ("keep text to <=25
words between tool calls") reduce by ~1.2%. The numbers work
because they give the model a concrete target.

Another insight: internal users and external users get
OPPOSITE instructions. External = "be brief" (save tokens = save money).
Internal = "err on the side of more explanation" (quality > cost).
"""

from enum import Enum
from dataclasses import dataclass


class OutputStyle(Enum):
    CONCISE = "concise"              # External users: save tokens
    EXPLANATORY = "explanatory"      # Internal users: quality first
    NUMERIC_ANCHORED = "anchored"    # Research: best token reduction


@dataclass
class OutputConfig:
    style: OutputStyle
    max_words_between_tools: int | None = None
    max_words_final_response: int | None = None
    custom_prompt: str | None = None


OUTPUT_PROMPTS: dict[OutputStyle, str] = {
    OutputStyle.CONCISE: """# Output Efficiency

IMPORTANT: Go straight to the point. Try the simplest approach
first without going in circles. Do not overdo it. Be extra concise.

Keep your text output brief and direct. Lead with the answer or
action, not the reasoning. Skip filler words, preamble, and
unnecessary transitions. Do not restate what the user said.

Focus text output on:
- Decisions that need the user's input
- High-level status updates at natural milestones
- Errors or blockers that change the plan

If you can say it in one sentence, don't use three.
This does not apply to code or tool calls.""",

    OutputStyle.EXPLANATORY: """# Communicating With the User

When sending text, you're writing for a person, not logging to a
console. Assume users can't see most tool calls or thinking —
only your text output.

Before your first tool call, briefly state what you're about to do.
While working, give short updates at key moments: when you find
something load-bearing, when changing direction, when you've made
progress without an update.

Assume the person has stepped away and lost the thread. Write so
they can pick back up cold: use complete sentences without
unexplained jargon. Err on the side of more explanation.

Write in flowing prose. Avoid fragments, excessive em dashes,
symbols and notation. Only use tables for short enumerable facts.

What's most important is the reader understanding your output
without mental overhead or follow-ups.""",

    OutputStyle.NUMERIC_ANCHORED: """# Output Length Control

Length limits:
- Keep text between tool calls to 25 words or fewer.
- Keep final responses to 100 words or fewer unless the
  task requires more detail.

Research shows numeric anchors reduce output tokens by ~1.2%
compared to qualitative instructions like "be concise" (~0.5%).
The concrete numbers give the model a measurable target.""",
}


def get_output_prompt(style: OutputStyle) -> str:
    """Get the output control prompt for a given style."""
    return OUTPUT_PROMPTS[style]


def get_output_for_user(user_type: str) -> str:
    """
    Route to the right output style based on user type.

    External users → CONCISE (save tokens, save money)
    Internal users → EXPLANATORY (quality > cost)
    Internal + research → NUMERIC_ANCHORED (A/B test)
    """
    if user_type == "internal":
        return get_output_prompt(OutputStyle.EXPLANATORY)
    return get_output_prompt(OutputStyle.CONCISE)


# ── Demo ──
if __name__ == "__main__":
    print("=" * 60)
    print("  OUTPUT CONTROL PATTERNS")
    print("=" * 60)

    for style in OutputStyle:
        print(f"\n{'─'*60}")
        print(f"  Style: {style.value}")
        print(f"{'─'*60}")
        print(get_output_prompt(style))
