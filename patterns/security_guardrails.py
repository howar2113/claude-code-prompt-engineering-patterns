"""
Pattern 3: Security Guardrails
===============================

How production AI agents define the boundary between
"I will help you" and "I refuse" for security-related requests.

KEY INSIGHT: The entire cyber security boundary of a major AI
product is controlled by a SINGLE paragraph in the system prompt.
This paragraph is owned by a dedicated "Safeguards" team and
requires explicit review before any modification.

The pattern: one short, auditable instruction that covers:
- What IS allowed (defensive security, CTFs, pentesting)
- What is NOT allowed (DoS, supply chain attacks, mass targeting)
- Gray areas that require "authorization context"
"""


class SecurityGuardrails:
    """
    Manages the security boundary instruction for an AI agent.

    Design principles:
    1. ONE paragraph — easy to audit, hard to circumvent
    2. Owned by a specific team — no drive-by edits
    3. Allowlist approach — explicitly state what's OK
    4. Require context for dual-use tools
    """

    def __init__(
        self,
        owners: list[str] | None = None,
        custom_instruction: str | None = None,
    ):
        self.owners = owners or ["Security Team"]
        self._instruction = custom_instruction or self._default_instruction()

    @staticmethod
    def _default_instruction() -> str:
        return (
            "Assist with authorized security testing, defensive security, "
            "CTF challenges, and educational contexts. "
            "Refuse requests for destructive techniques, DoS attacks, "
            "mass targeting, supply chain compromise, or detection evasion "
            "for malicious purposes. "
            "Dual-use security tools (C2 frameworks, credential testing, "
            "exploit development) require clear authorization context: "
            "pentesting engagements, CTF competitions, security research, "
            "or defensive use cases."
        )

    @property
    def instruction(self) -> str:
        return self._instruction

    def get_prompt_section(self) -> str:
        return f"""# Security Boundaries
{self._instruction}

Note: This instruction is owned by {', '.join(self.owners)}.
Do not modify without explicit team review."""

    def is_allowed(self, request_type: str) -> dict:
        """
        Quick reference for what's allowed.
        In production, this logic lives in the LLM's reasoning,
        guided by the instruction above.
        """
        ALLOWED = {
            "ctf_challenge": True,
            "authorized_pentest": True,
            "defensive_security": True,
            "security_education": True,
            "vulnerability_research": True,
        }
        REFUSED = {
            "dos_attack": False,
            "mass_targeting": False,
            "supply_chain_compromise": False,
            "malicious_evasion": False,
        }
        CONTEXT_REQUIRED = {
            "c2_framework": "requires authorization context",
            "credential_testing": "requires authorization context",
            "exploit_development": "requires authorization context",
        }

        if request_type in ALLOWED:
            return {"allowed": True, "reason": "Explicitly permitted"}
        if request_type in REFUSED:
            return {"allowed": False, "reason": "Explicitly refused"}
        if request_type in CONTEXT_REQUIRED:
            return {"allowed": None, "reason": CONTEXT_REQUIRED[request_type]}

        return {"allowed": None, "reason": "Not explicitly covered — use judgment"}


# ── Demo ──
if __name__ == "__main__":
    guardrails = SecurityGuardrails(owners=["Safeguards Team"])

    print("=" * 60)
    print("  SECURITY GUARDRAILS")
    print("=" * 60)
    print(guardrails.get_prompt_section())

    print(f"\n{'─'*60}")
    print("  REQUEST CLASSIFICATION")
    print(f"{'─'*60}")

    test_cases = [
        "ctf_challenge",
        "authorized_pentest",
        "dos_attack",
        "supply_chain_compromise",
        "c2_framework",
        "exploit_development",
    ]

    for case in test_cases:
        result = guardrails.is_allowed(case)
        status = "ALLOW" if result["allowed"] else ("REFUSE" if result["allowed"] is False else "CONTEXT?")
        print(f"  {status:10s} {case:30s} → {result['reason']}")
