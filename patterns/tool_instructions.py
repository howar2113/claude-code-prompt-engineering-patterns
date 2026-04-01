"""
Pattern 10: Tool Use Instructions
===================================

AI agents with tool access need explicit instructions about
WHICH tool to prefer for each task. Without these, the model
defaults to generic tools (like Bash for everything).

KEY INSIGHT: The instruction "Do NOT use Bash to run commands
when a relevant dedicated tool is provided" is marked as
CRITICAL in production. Tool-specific instructions improve:
- User experience (dedicated tools show better UI)
- Safety (dedicated tools have built-in validation)
- Performance (dedicated tools are optimized)
"""

from dataclasses import dataclass


@dataclass
class ToolPreference:
    """Maps a task to the preferred tool instead of the generic fallback."""
    task: str
    preferred_tool: str
    instead_of: str
    reason: str


# ── Production tool preferences ──

TOOL_PREFERENCES = [
    ToolPreference(
        task="Read files",
        preferred_tool="Read",
        instead_of="cat, head, tail, sed",
        reason="Dedicated tool shows file contents with line numbers in UI",
    ),
    ToolPreference(
        task="Edit files",
        preferred_tool="Edit",
        instead_of="sed, awk",
        reason="Dedicated tool shows diffs, validates edits, prevents errors",
    ),
    ToolPreference(
        task="Create files",
        preferred_tool="Write",
        instead_of="cat with heredoc, echo redirection",
        reason="Dedicated tool validates path, shows creation in UI",
    ),
    ToolPreference(
        task="Search for files",
        preferred_tool="Glob",
        instead_of="find, ls",
        reason="Dedicated tool is faster, returns sorted by modification time",
    ),
    ToolPreference(
        task="Search file contents",
        preferred_tool="Grep",
        instead_of="grep, rg",
        reason="Dedicated tool has optimized permissions and access",
    ),
]


def build_tool_instructions(
    available_tools: set[str],
    bash_tool_name: str = "Bash",
) -> str:
    """
    Build tool use instructions based on available tools.

    Only includes preferences for tools that are actually available.
    """
    lines = [
        f"# Using Your Tools",
        f"- Do NOT use {bash_tool_name} to run commands when a relevant "
        f"dedicated tool is provided. Using dedicated tools allows the user "
        f"to better understand and review your work. This is CRITICAL:",
    ]

    for pref in TOOL_PREFERENCES:
        if pref.preferred_tool.lower() in {t.lower() for t in available_tools}:
            lines.append(
                f"  - To {pref.task.lower()}: use {pref.preferred_tool} "
                f"instead of {pref.instead_of}"
            )

    lines.append(
        f"- Reserve {bash_tool_name} exclusively for system commands and "
        f"terminal operations that require shell execution."
    )

    # Parallelism instruction
    lines.append(
        "- You can call multiple tools in a single response. If there are "
        "no dependencies between calls, make all independent calls in "
        "parallel for efficiency."
    )

    return "\n".join(lines)


# ── Agent tool scoping ──

def get_agent_tools(agent_type: str) -> list[str]:
    """
    Different agents get different tool sets.

    This is a critical security pattern: read-only agents
    cannot modify files, coordinators cannot execute directly.
    """
    AGENT_TOOL_SETS = {
        "coordinator": [],  # Coordinator delegates, never executes
        "explorer": ["Read", "Glob", "Grep", "Bash"],  # Read-only + search
        "planner": ["Read", "Glob", "Grep"],  # Read-only, no bash
        "verifier": ["Read", "Glob", "Grep", "Bash"],  # Can run tests
        "general": ["*"],  # Full access
    }
    return AGENT_TOOL_SETS.get(agent_type, ["*"])


# ── Demo ──
if __name__ == "__main__":
    available = {"Read", "Edit", "Write", "Glob", "Grep", "Bash", "Agent"}

    print("=" * 60)
    print("  TOOL USE INSTRUCTIONS")
    print("=" * 60)
    print(build_tool_instructions(available))

    print(f"\n{'─'*60}")
    print("  AGENT TOOL SCOPING")
    print(f"{'─'*60}")
    for agent_type in ["coordinator", "explorer", "planner", "verifier", "general"]:
        tools = get_agent_tools(agent_type)
        print(f"  {agent_type:15s} → {tools}")
