# Claude Code Prompt Engineering Patterns

> Reverse-engineered from the Claude Code source leak (March 31, 2026). 10 production patterns documented and implemented in Python.

<p align="center">
  <img src="https://img.shields.io/badge/patterns-10-blue?style=for-the-badge" alt="10 Patterns">
  <img src="https://img.shields.io/badge/language-Python-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="MIT License">
  <img src="https://img.shields.io/badge/code-zero%20proprietary-red?style=for-the-badge" alt="No proprietary code">
</p>

---

## What Happened

On March 31, 2026, Anthropic accidentally leaked the **entire source code** of Claude Code (512,000 lines of TypeScript) through a misconfigured npm package. Before the DMCA takedowns, I analyzed their prompt engineering architecture and extracted **10 production patterns** that any developer can use.

This repo does **NOT** contain any Anthropic code. It documents the **techniques and patterns** with original Python implementations.

---

## The 10 Patterns

```
    SYSTEM PROMPT ARCHITECTURE (how Claude Code builds its prompt)
    ================================================================

    ┌──────────────────────────────────────────────────────────────┐
    │  Pattern 1: MODULAR PROMPT                                   │
    │  ┌────────────────────────────────────────────────────────┐  │
    │  │  Identity Section                                      │  │
    │  │  "You are an AI coding assistant..."                   │  │
    │  ├────────────────────────────────────────────────────────┤  │
    │  │  Pattern 3: SECURITY GUARDRAILS                        │  │
    │  │  One paragraph that controls all cyber boundaries      │  │
    │  ├────────────────────────────────────────────────────────┤  │
    │  │  Pattern 2: CONDITIONAL BEHAVIOR                       │  │
    │  │  if user == "internal":                                │  │
    │  │      add anti-hallucination rules                      │  │
    │  │      add stricter coding rules                         │  │
    │  │  else:                                                 │  │
    │  │      add "be concise" (save tokens = save $$$)         │  │
    │  ├────────────────────────────────────────────────────────┤  │
    │  │  Pattern 10: TOOL INSTRUCTIONS                         │  │
    │  │  "Use Read instead of cat, Edit instead of sed"        │  │
    │  ├────────────────────────────────────────────────────────┤  │
    │  │  Pattern 9: OUTPUT CONTROL                             │  │
    │  │  "Keep text to ≤25 words between tool calls"           │  │
    │  ├══════════════════════════════════════════════════════════╡  │
    │  │  ^^^ Pattern 8: CACHE BOUNDARY ^^^                     │  │
    │  │  Static above (cached globally, 90% cheaper)           │  │
    │  │  Dynamic below (recomputed each turn)                  │  │
    │  ├────────────────────────────────────────────────────────┤  │
    │  │  Pattern 7: FEATURE FLAGS                              │  │
    │  │  KAIROS, COORDINATOR_MODE, VERIFICATION_AGENT...       │  │
    │  │  30+ unreleased features found behind flags            │  │
    │  ├────────────────────────────────────────────────────────┤  │
    │  │  Language / Memory / MCP Instructions (dynamic)        │  │
    │  └────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────┘

    MULTI-AGENT ARCHITECTURE (how Claude Code orchestrates agents)
    ================================================================

    ┌──────────────────────────────────────────────────────────────┐
    │  Pattern 4: AGENT SPECIALIZATION                             │
    │                                                               │
    │  ┌─────────────┐                                             │
    │  │ COORDINATOR  │  ← Never executes. Only plans & delegates  │
    │  │ (no tools)   │                                             │
    │  └──────┬───────┘                                             │
    │         │ spawns                                              │
    │    ┌────┼────────┬──────────┐                                │
    │    ▼    ▼        ▼          ▼                                │
    │  ┌────┐ ┌──────┐ ┌────────┐ ┌──────────┐                   │
    │  │PLAN│ │EXPLORE│ │GENERAL │ │ VERIFY   │                   │
    │  │read│ │read   │ │all     │ │ read+bash│ ← Pattern 5:     │
    │  │only│ │only   │ │tools   │ │ ADVERSAR │   ANTI-HALLUC.   │
    │  └────┘ └──────┘ └────────┘ └──────────┘                   │
    │                                                               │
    │  Pattern 6: ATTRIBUTION CONTROL                              │
    │  Internal repos → "Co-Authored-By: Claude"                   │
    │  Public repos   → Undercover mode (hide AI identity)         │
    └──────────────────────────────────────────────────────────────┘
```

---

## Key Discoveries

### Internal vs External Users

Anthropic employees receive a **fundamentally different** Claude than you:

| Rule | External Users (you) | Internal Users (Anthropic) |
|---|---|---|
| Response style | "Be concise, go straight to the point" | "Err on the side of more explanation" |
| Comments in code | (no rule) | "Default to writing NO comments" |
| Verification | (no rule) | "Before reporting complete, VERIFY it works" |
| Honesty | (no rule) | "Never claim 'all tests pass' when output shows failures" |
| Length limits | (no rule) | "Keep text to ≤25 words between tool calls" |

### The Undercover Mode

When Anthropic employees contribute to public/open-source repos, Claude activates **Undercover Mode**:

```
"You are operating UNDERCOVER in a PUBLIC repository.
 Your commits MUST NOT contain ANY Anthropic-internal information.
 Do not blow your cover."

FORBIDDEN in commits:
 - Internal codenames (Capybara, Tengu...)
 - Model version numbers
 - "Co-Authored-By: Claude"
 - Any mention of being an AI
```

### 30+ Hidden Feature Flags

Unreleased features found behind compile-time flags:

| Flag | What it does |
|---|---|
| `KAIROS` | Autonomous agent mode — acts without being asked |
| `KAIROS_DREAM` | Dream/imagination skill |
| `PROACTIVE` | Agent anticipates user needs |
| `COORDINATOR_MODE` | Multi-agent orchestration |
| `VERIFICATION_AGENT` | Adversarial verification |
| `TOKEN_BUDGET` | "+500K tokens" mode for big tasks |
| `BASH_CLASSIFIER` | ML classifier for command safety |
| `CONTEXT_COLLAPSE` | Smart context compression |
| `CHICAGO_MCP` | New MCP server system |
| ...and 20+ more | |

### The Security Boundary = 1 Paragraph

The ENTIRE cyber security boundary is controlled by ONE instruction, owned by the "Safeguards Team":

```
"Assist with authorized security testing, defensive security,
 CTF challenges, and educational contexts. Refuse requests for
 destructive techniques, DoS attacks, mass targeting, supply
 chain compromise, or detection evasion for malicious purposes."
```

### Prompt Caching = 90% Cost Reduction

Claude Code splits its prompt at a `SYSTEM_PROMPT_DYNAMIC_BOUNDARY`. Everything above is cached globally (same for all users). Cache reads cost $0.30/M tokens vs $5.00/M for uncached — **94% savings**.

---

## Quick Start

```bash
git clone https://github.com/miloudbelarebia/prompt-engineering-patterns.git
cd prompt-engineering-patterns

# Build a complete system prompt using all 10 patterns
python3 examples/build_system_prompt.py

# See multi-agent architecture in action
python3 examples/multi_agent_prompts.py

# Run any individual pattern
python3 patterns/modular_prompt.py
python3 patterns/conditional_behavior.py
python3 patterns/feature_flags.py
```

---

## Structure

```
prompt-engineering-patterns/
├── README.md
├── requirements.txt
├── patterns/
│   ├── modular_prompt.py          # Pattern 1: Composable prompt sections
│   ├── conditional_behavior.py    # Pattern 2: User-type gating
│   ├── security_guardrails.py     # Pattern 3: Cyber risk boundaries
│   ├── agent_specialization.py    # Pattern 4: Role-specific agent prompts
│   ├── anti_hallucination.py      # Pattern 5: Prevent false claims
│   ├── attribution_control.py     # Pattern 6: Undercover mode
│   ├── feature_flags.py           # Pattern 7: Feature-gated prompt sections
│   ├── prompt_caching.py          # Pattern 8: Cache boundary optimization
│   ├── output_control.py          # Pattern 9: Response length & style
│   └── tool_instructions.py       # Pattern 10: Tool preference rules
└── examples/
    ├── build_system_prompt.py     # Assembles all 10 patterns
    └── multi_agent_prompts.py     # Multi-agent pipeline demo
```

---

## Who Is This For

- Developers building AI coding agents or copilots
- Teams implementing multi-agent systems
- Anyone using Claude, GPT, or open-source LLMs with tool use
- Prompt engineers who want production-grade patterns (not "act as a...")

---

## Author

**Miloud Belarebia** — [@databelarebia](https://github.com/databelarebia)

Tech Lead Data & MLOps | Founder [2PiData](https://2pidata.com)

## License

MIT License — Use these patterns freely in your projects.

## Disclaimer

This repo documents prompt engineering patterns identified through analysis of publicly available source code leaked via npm on March 31, 2026. It does not contain, reproduce, or redistribute any proprietary Anthropic code. All implementations are original Python code.
