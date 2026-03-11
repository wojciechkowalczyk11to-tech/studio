from __future__ import annotations

from google.adk.agents import Agent

from nexus_agent.config.prompts import REVIEWER_PROMPT


def build_reviewer_agent() -> Agent:
    """Build reviewer agent."""
    return Agent(name="reviewer", instruction=REVIEWER_PROMPT)
