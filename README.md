# Prompt Engineering Patterns for AI Coding Agents

## What This Repo Is

A practical guide to **prompt engineering patterns** used in production AI coding agents, documented and implemented in Python.

These patterns were identified through analysis of publicly available source code from major AI tools. This repo does NOT contain any proprietary code -- it documents the **techniques and patterns** with original Python implementations.

## Why This Matters

Most prompt engineering guides teach you to write "Act as a senior developer". Real production systems use sophisticated patterns:
- Multi-section system prompts with caching boundaries
- Conditional rules based on user type
- Feature-gated behaviors
- Agent-specific prompt specialization
- Anti-hallucination instructions
- Security guardrails

This repo documents ALL of these patterns.

## Patterns Documented

### 1. Modular System Prompt Architecture
How to build a system prompt from composable sections, with caching boundaries.

### 2. Conditional Behavior (User-Type Gating)
Different instructions for different user types (internal vs external).

### 3. Security Guardrails Pattern
How to define cyber risk boundaries in a single, auditable instruction.

### 4. Agent Specialization Pattern
How to create specialized agents (Recon, Plan, Verify, Execute) with role-specific prompts.

### 5. Anti-Hallucination Instructions
Explicit rules to prevent false claims and verify work.

### 6. Undercover / Attribution Control
How to control AI attribution in commits and public-facing outputs.

### 7. Feature Flag Gating in Prompts
How to gate prompt sections behind feature flags for gradual rollout.

### 8. Prompt Caching Strategy
Static vs dynamic sections, cache boundaries, and cost optimization.

### 9. Output Efficiency Control
How to control response length and style programmatically.

### 10. Tool Use Instructions
How to instruct an AI to prefer specific tools over generic alternatives.

## Quick Start

```bash
pip install -r requirements.txt
python examples/build_system_prompt.py
python examples/multi_agent_prompts.py
```

## Structure

```
prompt-engineering-patterns/
|-- README.md
|-- requirements.txt
|-- patterns/
|   |-- __init__.py
|   |-- modular_prompt.py        # Pattern 1: Composable prompt sections
|   |-- conditional_behavior.py  # Pattern 2: User-type gating
|   |-- security_guardrails.py   # Pattern 3: Cyber risk boundaries
|   |-- agent_specialization.py  # Pattern 4: Role-specific prompts
|   |-- anti_hallucination.py    # Pattern 5: Prevent false claims
|   |-- attribution_control.py   # Pattern 6: Undercover mode
|   |-- feature_flags.py         # Pattern 7: Feature-gated prompts
|   |-- prompt_caching.py        # Pattern 8: Cache optimization
|   |-- output_control.py        # Pattern 9: Response length/style
|   |-- tool_instructions.py     # Pattern 10: Tool preference rules
|-- examples/
|   |-- build_system_prompt.py   # Full system prompt builder
|   |-- multi_agent_prompts.py   # Multi-agent setup
|   |-- cost_comparison.py       # Cache hit vs miss cost analysis
|-- diagrams/
|   |-- prompt_architecture.md   # Visual architecture diagrams
```

## Who Is This For

- Developers building AI coding agents
- Teams implementing multi-agent systems
- Anyone using Claude, GPT, or open-source LLMs with tool use
- Prompt engineers who want production-grade patterns

## Author

**Miloud Belarebia** - [2PiData](https://2pidata.com)
Tech Lead Data & MLOps | Arabic & Darija AI Advocate

## License

MIT License - Use these patterns freely in your projects.

## Disclaimer

This repo documents prompt engineering patterns identified through analysis of publicly available source code. It does not contain, reproduce, or redistribute any proprietary code. All implementations are original Python code written from scratch.
