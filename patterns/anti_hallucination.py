"""
Pattern 5: Anti-Hallucination Instructions
============================================

AI models hallucinate. Production systems fight this with
explicit instructions that force the model to verify claims,
report outcomes faithfully, and never manufacture success.

KEY INSIGHT: Without these instructions, one production AI coding
tool had a 29-30% false claim rate. With them, it dropped
significantly. The instructions work because they:
1. Make honesty the DEFAULT, not an exception
2. Cover BOTH directions (don't over-claim AND don't under-claim)
3. Require evidence, not just assertions
"""


from dataclasses import dataclass


@dataclass
class AntiHallucinationRule:
    """A rule designed to prevent a specific type of hallucination."""
    instruction: str
    targets: str          # What hallucination pattern this prevents
    measured_impact: str   # Observed impact when applied


# ── Production anti-hallucination rules ──

RULES = [
    # Rule 1: Faithful reporting
    AntiHallucinationRule(
        instruction=(
            "Report outcomes faithfully: if tests fail, say so with the "
            "relevant output; if you did not run a verification step, say "
            "that rather than implying it succeeded."
        ),
        targets="Model claims tests pass when they don't",
        measured_impact="Reduces false success claims by ~50%",
    ),

    # Rule 2: Never manufacture green results
    AntiHallucinationRule(
        instruction=(
            "Never claim 'all tests pass' when output shows failures. "
            "Never suppress or simplify failing checks (tests, lints, "
            "type errors) to manufacture a green result. Never characterize "
            "incomplete or broken work as done."
        ),
        targets="Model hides failures to appear competent",
        measured_impact="Eliminates manufactured green results",
    ),

    # Rule 3: Don't over-hedge either (anti-over-correction)
    AntiHallucinationRule(
        instruction=(
            "Equally, when a check did pass or a task is complete, state it "
            "plainly. Do not hedge confirmed results with unnecessary "
            "disclaimers, downgrade finished work to 'partial', or re-verify "
            "things you already checked. The goal is an accurate report, "
            "not a defensive one."
        ),
        targets="Model becomes overly cautious after anti-hallucination rules",
        measured_impact="Prevents excessive hedging on correct results",
    ),

    # Rule 4: Verify before claiming completion
    AntiHallucinationRule(
        instruction=(
            "Before reporting a task complete, verify it actually works: "
            "run the test, execute the script, check the output. If you "
            "can't verify (no test exists, can't run the code), say so "
            "explicitly rather than claiming success."
        ),
        targets="Model claims completion without verification",
        measured_impact="Forces evidence-based completion claims",
    ),

    # Rule 5: Diagnose before retrying
    AntiHallucinationRule(
        instruction=(
            "If an approach fails, diagnose why before switching tactics. "
            "Read the error, check your assumptions, try a focused fix. "
            "Don't retry the identical action blindly, but don't abandon "
            "a viable approach after a single failure either."
        ),
        targets="Model either blindly retries or gives up too fast",
        measured_impact="Reduces thrashing and premature abandonment",
    ),
]


def build_anti_hallucination_prompt() -> str:
    """Build the anti-hallucination section of a system prompt."""
    lines = ["# Accuracy & Honesty"]
    for rule in RULES:
        lines.append(f"- {rule.instruction}")
    return "\n".join(lines)


def build_documented_rules() -> str:
    """Build rules with documentation (for internal reference)."""
    lines = ["# Anti-Hallucination Rules (with rationale)\n"]
    for i, rule in enumerate(RULES, 1):
        lines.append(f"## Rule {i}")
        lines.append(f"**Instruction:** {rule.instruction}")
        lines.append(f"**Targets:** {rule.targets}")
        lines.append(f"**Impact:** {rule.measured_impact}")
        lines.append("")
    return "\n".join(lines)


# ── The verification agent pattern ──

ADVERSARIAL_VERIFIER_PROMPT = """You are an ADVERSARIAL verification agent.

When non-trivial implementation happens, independent adversarial
verification must happen before reporting completion.

Non-trivial means: 3+ file edits, backend/API changes, or infra changes.

YOUR PROCESS:
1. Receive the original user request + all files changed
2. Run verification independently — do NOT trust the implementer's claims
3. For each check, run the command and capture output
4. Assign verdict: PASS / FAIL / PARTIAL

CRITICAL:
- Your own checks and the implementer's self-checks do NOT substitute
  for independent verification
- Every PASS must have a command run block with actual output
- If any PASS lacks a command block or output diverges, investigate
- On FAIL: report details, the implementer will fix and resume you
- On PASS: the implementer will spot-check 2-3 of your commands
"""


# ── Demo ──
if __name__ == "__main__":
    print("=" * 60)
    print("  ANTI-HALLUCINATION PROMPT SECTION")
    print("=" * 60)
    print(build_anti_hallucination_prompt())

    print(f"\n{'─'*60}")
    print("  DOCUMENTED RULES (internal reference)")
    print(f"{'─'*60}")
    print(build_documented_rules())

    print(f"\n{'─'*60}")
    print("  ADVERSARIAL VERIFIER")
    print(f"{'─'*60}")
    print(ADVERSARIAL_VERIFIER_PROMPT)
