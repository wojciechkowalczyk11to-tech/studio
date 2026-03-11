from __future__ import annotations

import asyncio

import click
from google import genai
from google.adk.agents import ParallelAgent, SequentialAgent
from rich.console import Console

from nexus_agent.agents.coder import build_coder_agent
from nexus_agent.agents.deployer import build_deployer_agent
from nexus_agent.agents.planner import build_planner_agent
from nexus_agent.agents.reviewer import build_reviewer_agent
from nexus_agent.config.models import LOCAL_MODEL, PREMIUM_MODEL, PRIMARY_MODEL
from nexus_agent.config.prompts import PLANNER_PROMPT
from nexus_agent.config.settings import NexusAgentSettings
from nexus_shared.thinking import build_genai_config

console = Console()


def resolve_model(best: bool, local: bool) -> str:
    if local:
        return LOCAL_MODEL
    if best:
        return PREMIUM_MODEL
    return PRIMARY_MODEL


async def run_once(prompt: str, best: bool, local: bool) -> str:
    settings = NexusAgentSettings()
    model = resolve_model(best, local)
    if local:
        return f"Lokalny model {LOCAL_MODEL} powinien zostać wywołany pod adresem {settings.local_llama_url}."
    try:
        client = genai.Client(api_key=settings.google_api_key or None)
        cfg = build_genai_config(PLANNER_PROMPT, prompt, command="nexus-agent")
        response = client.models.generate_content(model=model, contents=prompt, config=cfg)
        return response.text or "Brak odpowiedzi modelu."
    except Exception as exc:
        raise RuntimeError(f"Błąd zapytania do modelu: {exc}") from exc


def build_pipeline() -> SequentialAgent:
    planner = build_planner_agent()
    coder = build_coder_agent()
    reviewer = build_reviewer_agent()
    _parallel = ParallelAgent(name="tool-parallel", sub_agents=[reviewer, build_deployer_agent()])
    return SequentialAgent(name="nexus-seq", sub_agents=[planner, coder, reviewer])


@click.command()
@click.argument("query", required=False)
@click.option("-p", "prompt_opt", default="", help="Prompt for scripting mode.")
@click.option("--best", is_flag=True, default=False)
@click.option("--local", is_flag=True, default=False)
def main(query: str | None, prompt_opt: str, best: bool, local: bool) -> None:
    prompt = prompt_opt or query
    if prompt:
        text = asyncio.run(run_once(prompt, best, local))
        console.print(text)
        return
    console.print("Tryb czatu. Wpisz 'exit' aby zakończyć.")
    try:
        while True:
            user = input("nexus-agent> ").strip()
            if user.lower() in {"exit", "quit"}:
                break
            text = asyncio.run(run_once(user, best, local))
            console.print(text)
    except (KeyboardInterrupt, EOFError):
        console.print("\nZakończono sesję.")
