from __future__ import annotations

from google.adk.agents import Agent

from nexus_agent.config.prompts import DEPLOYER_PROMPT


def build_deployer_agent() -> Agent:
    """Build deployer agent."""
    return Agent(name="deployer", instruction=DEPLOYER_PROMPT)
