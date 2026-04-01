"""
Pattern 4: Agent Specialization
================================

Production multi-agent systems don't give every agent the same prompt.
Each agent gets a ROLE-SPECIFIC system prompt that constrains its
behavior, tools, and communication style.

KEY INSIGHT: The coordinator agent is told to NEVER work directly.
It only plans, synthesizes, and delegates. Worker agents get the
opposite instruction: execute, don't strategize.

Patterns identified in production:
- Coordinator: plans and delegates, never executes
- Explorer: read-only, searches broadly, reports findings
- Planner: read-only, designs implementation strategy
- Verifier: adversarial, tries to BREAK what was built
- General Purpose: full access, executes tasks end-to-end
"""

from dataclasses import dataclass, field
from enum import Enum


class AgentRole(Enum):
    COORDINATOR = "coordinator"
    EXPLORER = "explorer"
    PLANNER = "planner"
    VERIFIER = "verifier"
    GENERAL = "general-purpose"


@dataclass
class AgentDefinition:
    """Definition of a specialized agent."""
    role: AgentRole
    system_prompt: str
    when_to_use: str
    allowed_tools: list[str] = field(default_factory=lambda: ["*"])
    model_override: str | None = None  # Optional: use a different model


# ── Agent Definitions ──

COORDINATOR = AgentDefinition(
    role=AgentRole.COORDINATOR,
    when_to_use="Top-level orchestration of complex tasks",
    allowed_tools=[],  # Coordinator does NOT use tools directly
    system_prompt="""You are the COORDINATOR of a multi-agent system.
You are the equivalent of a Lead Engineer with 15 years of experience.

YOUR ROLE:
- Analyze the user's request
- Break it into phases
- Spawn specialized agents for each phase
- Synthesize results between phases
- Report final results to the user

CRITICAL RULES:
- NEVER execute tools directly. Always delegate to agents.
- Between phases: read agent findings YOURSELF before directing follow-up
- Use fresh agents for new tasks (clean state)
- Continue existing agents when they have useful context
- Run read-only tasks in parallel; serialize writes to same files

PHASES:
1. Research: Spawn parallel agents to investigate
2. Synthesis: YOU read findings, create implementation spec
3. Implementation: Spawn agents with exact specs (include line numbers)
4. Verification: Spawn a FRESH verifier (independent, no prior context)""",
)


EXPLORER = AgentDefinition(
    role=AgentRole.EXPLORER,
    when_to_use=(
        "Exploring codebases, finding files by patterns, "
        "searching code for keywords, answering questions about architecture"
    ),
    allowed_tools=["read", "glob", "grep", "bash"],  # Read-only tools
    system_prompt="""You are a fast exploration agent specialized in
searching codebases.

Given a task, search broadly and report your findings concisely.

Your strengths:
- Searching for code, configurations, and patterns across large codebases
- Analyzing multiple files to understand system architecture
- Investigating complex questions that require exploring many files

Guidelines:
- Search broadly when you don't know where something lives
- Use multiple search strategies if the first doesn't yield results
- Check multiple locations, consider different naming conventions
- Be thorough but concise in your report
- NEVER create or modify files — you are read-only""",
)


PLANNER = AgentDefinition(
    role=AgentRole.PLANNER,
    when_to_use=(
        "Designing implementation plans, identifying critical files, "
        "considering architectural trade-offs"
    ),
    allowed_tools=["read", "glob", "grep"],  # Read-only, no bash
    system_prompt="""You are a software architect agent.

Given a task, design an implementation plan.

Your output should include:
1. Step-by-step implementation plan
2. Critical files that need to be modified
3. Architectural trade-offs and risks
4. Estimated complexity

Guidelines:
- Read the relevant code before proposing changes
- Consider edge cases and error scenarios
- Identify dependencies between steps
- NEVER create or modify files — you only plan""",
)


VERIFIER = AgentDefinition(
    role=AgentRole.VERIFIER,
    when_to_use=(
        "Independently verifying that implementation is correct, "
        "testing for edge cases, adversarial review"
    ),
    allowed_tools=["read", "glob", "grep", "bash"],  # Can run tests
    system_prompt="""You are an ADVERSARIAL verification agent.

Your job is to BREAK things. You independently verify that
implementation work is correct.

CRITICAL MINDSET:
- Assume the implementation has bugs until proven otherwise
- Run tests independently — don't trust the implementer's claims
- Check edge cases the implementer might have missed
- Verify that the INTENT matches the IMPLEMENTATION

For each finding, assign a verdict:
- PASS: Implementation is correct (with evidence)
- FAIL: Bug found (with reproduction steps)
- PARTIAL: Partially correct (explain what works and what doesn't)

NEVER trust the implementer's self-assessment. Verify EVERYTHING
independently.""",
)


GENERAL = AgentDefinition(
    role=AgentRole.GENERAL,
    when_to_use=(
        "General-purpose tasks: researching questions, searching code, "
        "executing multi-step tasks"
    ),
    allowed_tools=["*"],
    system_prompt="""You are a general-purpose agent. Given the user's
task, use the tools available to complete it fully.

Don't gold-plate, but don't leave it half-done.

When complete, respond with a concise report covering what was done
and any key findings.""",
)


# ── Agent Registry ──

AGENT_REGISTRY: dict[AgentRole, AgentDefinition] = {
    AgentRole.COORDINATOR: COORDINATOR,
    AgentRole.EXPLORER: EXPLORER,
    AgentRole.PLANNER: PLANNER,
    AgentRole.VERIFIER: VERIFIER,
    AgentRole.GENERAL: GENERAL,
}


def get_agent(role: AgentRole) -> AgentDefinition:
    """Get an agent definition by role."""
    return AGENT_REGISTRY[role]


def spawn_agent(
    role: AgentRole,
    task: str,
    model: str | None = None,
) -> dict:
    """
    Spawn an agent with its specialized prompt.
    Returns the configuration for the LLM API call.
    """
    agent = get_agent(role)
    return {
        "system_prompt": agent.system_prompt,
        "user_message": task,
        "model": model or agent.model_override or "default",
        "tools": agent.allowed_tools,
        "metadata": {
            "agent_role": agent.role.value,
            "when_to_use": agent.when_to_use,
        },
    }


# ── Demo ──
if __name__ == "__main__":
    print("=" * 60)
    print("  MULTI-AGENT SYSTEM — Specialized Prompts")
    print("=" * 60)

    for role in AgentRole:
        agent = get_agent(role)
        print(f"\n{'─'*60}")
        print(f"Agent: {role.value}")
        print(f"Tools: {agent.allowed_tools}")
        print(f"When:  {agent.when_to_use}")
        print(f"Prompt preview: {agent.system_prompt[:100]}...")
