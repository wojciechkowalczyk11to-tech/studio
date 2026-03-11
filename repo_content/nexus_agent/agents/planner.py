from __future__ import annotations

from google.adk.agents import Agent

from nexus_agent.config.prompts import PLANNER_PROMPT


def build_planner_agent() -> Agent:
    """Build planner agent."""
    return Agent(name="planner", instruction=PLANNER_PROMPT)
