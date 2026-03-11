from __future__ import annotations

from google.adk.agents import Agent

from nexus_agent.config.prompts import CODER_PROMPT


def build_coder_agent() -> Agent:
    """Build coder agent."""
    return Agent(name="coder", instruction=CODER_PROMPT)
