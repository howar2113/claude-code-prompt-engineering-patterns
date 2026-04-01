"""
Complete Example: Multi-Agent System with Specialized Prompts
=============================================================

Shows how to set up a Coordinator + Workers system where
each agent gets a role-specific prompt, tools, and model.

Run: python examples/multi_agent_prompts.py
"""

import sys
sys.path.insert(0, ".")

from patterns.agent_specialization import (
    AgentRole,
    get_agent,
    spawn_agent,
    COORDINATOR,
    VERIFIER,
)


def simulate_audit_pipeline():
    """
    Simulate a multi-agent pipeline like a production AI tool.

    Flow:
    Phase 0: Coordinator analyzes the task and creates a plan
    Phase 1: Explorer searches the codebase
    Phase 2: Planner designs the implementation
    Phase 3: General agent implements the changes
    Phase 4: Verifier checks the implementation
    """
    print("=" * 60)
    print("  MULTI-AGENT PIPELINE SIMULATION")
    print("=" * 60)

    phases = [
        (AgentRole.COORDINATOR, "Analyze this task: Add rate limiting to the API"),
        (AgentRole.EXPLORER, "Find all API route handlers in the codebase"),
        (AgentRole.PLANNER, "Design a rate limiting implementation for FastAPI"),
        (AgentRole.GENERAL, "Implement rate limiting using slowapi on all routes"),
        (AgentRole.VERIFIER, "Verify rate limiting works: test 100 requests in 10s"),
    ]

    for i, (role, task) in enumerate(phases):
        config = spawn_agent(role, task)

        print(f"\n{'─'*60}")
        print(f"  Phase {i}: {role.value.upper()}")
        print(f"{'─'*60}")
        print(f"  Task:   {task}")
        print(f"  Model:  {config['model']}")
        print(f"  Tools:  {config['tools']}")
        print(f"  Prompt: {config['system_prompt'][:80]}...")
        print()


def show_coordinator_pattern():
    """
    The Coordinator Pattern in detail.

    KEY RULE: The coordinator NEVER executes tools directly.
    It only plans, delegates, and synthesizes.

    This is the #1 pattern from production multi-agent systems.
    """
    print("\n" + "=" * 60)
    print("  THE COORDINATOR PATTERN")
    print("=" * 60)

    coord = get_agent(AgentRole.COORDINATOR)

    print(f"\nTools allowed: {coord.allowed_tools}")
    print("(Empty list = coordinator CANNOT use tools directly)")

    print(f"\nFull system prompt:")
    print(f"{'─'*60}")
    print(coord.system_prompt)

    print(f"\n{'─'*60}")
    print("THE KEY INSIGHT:")
    print("The coordinator's power comes from RESTRICTING it.")
    print("By removing tool access, you force it to think and delegate.")
    print("This prevents the coordinator from getting lost in details.")


def show_verifier_pattern():
    """
    The Adversarial Verifier Pattern.

    KEY RULE: The verifier is spawned FRESH (no prior context).
    It must independently verify, never trust the implementer.
    """
    print("\n" + "=" * 60)
    print("  THE ADVERSARIAL VERIFIER PATTERN")
    print("=" * 60)

    verifier = get_agent(AgentRole.VERIFIER)

    print(f"\nTools allowed: {verifier.allowed_tools}")
    print("(Has bash access = can run tests independently)")

    print(f"\nFull system prompt:")
    print(f"{'─'*60}")
    print(verifier.system_prompt)

    print(f"\n{'─'*60}")
    print("THE KEY INSIGHT:")
    print("Spawn the verifier FRESH — no shared context with the builder.")
    print("If the verifier saw the builder's reasoning, it would be biased.")
    print("Independent verification catches what self-checks miss.")


if __name__ == "__main__":
    simulate_audit_pipeline()
    show_coordinator_pattern()
    show_verifier_pattern()
