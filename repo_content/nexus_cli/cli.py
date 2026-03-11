from __future__ import annotations

import sys
import uuid

import click
from rich.console import Console

from nexus_cli.config.settings import RuntimeConfig, load_config, save_config
from nexus_cli.config.system_prompts import (
    CODE_PROMPT,
    DEPLOY_PROMPT,
    GENERAL_PROMPT,
    REVIEW_PROMPT,
)
from nexus_cli.providers.gemini import ask_gemini
from nexus_cli.router import select_model
from nexus_cli.utils.cost_tracker import log_cost, stats
from nexus_cli.utils.history import add_message, clear_history, list_sessions

console = Console()


@click.group()
def cli() -> None:
    """Unified CLI for Nexus AI aggregator."""


@cli.command()
@click.argument("query", required=False)
@click.option("--best", is_flag=True)
@click.option("--local", is_flag=True)
@click.option("--cheap", is_flag=True)
@click.option("--model", "model_override", default=None)
def ask(query: str | None, best: bool, local: bool, cheap: bool, model_override: str | None) -> None:
    text = query or sys.stdin.read().strip()
    if not text:
        raise click.ClickException("Brak zapytania wejściowego.")
    model = select_model(best, local, model_override)
    cfg = load_config()
    response = ask_gemini("", model, GENERAL_PROMPT, text)
    console.print(response)
    log_cost("gemini", model, len(text.split()), len(response.split()), 0.0)
    if cheap:
        console.print("Tryb oszczędny aktywny.")
    if cfg.cost_alert_daily <= 0.0:
        console.print("Alert kosztowy wyłączony.")


@cli.command()
@click.argument("query", required=False)
def code(query: str | None) -> None:
    text = query or sys.stdin.read().strip()
    console.print(ask_gemini("", "gemini-3.0-flash-preview", CODE_PROMPT, text))


@cli.command()
@click.argument("query", required=False)
def review(query: str | None) -> None:
    text = query or sys.stdin.read().strip()
    console.print(ask_gemini("", "gemini-3.0-flash-preview", REVIEW_PROMPT, text))


@cli.command()
@click.argument("target", required=False)
def deploy(target: str | None) -> None:
    text = target or sys.stdin.read().strip() or "cloudflare"
    console.print(ask_gemini("", "gemini-3.0-flash-preview", DEPLOY_PROMPT, f"Deploy target: {text}"))


@cli.group()
def config() -> None:
    """Manage runtime config."""


@config.command("show")
def config_show() -> None:
    console.print(load_config().model_dump_json(indent=2))


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    cfg = load_config()
    data = cfg.model_dump()
    if key not in data:
        raise click.ClickException("Nieprawidłowy klucz konfiguracji.")
    data[key] = value if key not in {"cost_alert_daily"} else float(value)
    save_config(RuntimeConfig(**data))
    console.print("Zapisano konfigurację.")


@cli.command()
def costs() -> None:
    for row in stats():
        console.print(row)


@cli.command()
def chat() -> None:
    session = str(uuid.uuid4())
    try:
        while True:
            prompt = input("nexus> ").strip()
            if prompt in {"exit", "quit"}:
                break
            add_message(session, "user", prompt)
            answer = ask_gemini("", "gemini-3.0-flash-preview", GENERAL_PROMPT, prompt)
            add_message(session, "assistant", answer)
            console.print(answer)
    except (KeyboardInterrupt, EOFError):
        console.print("\nZakończono sesję czatu.")


@cli.group()
def history() -> None:
    """History management."""


@history.command("list")
def history_list() -> None:
    for item in list_sessions():
        console.print(item)


@history.command("clear")
def history_clear() -> None:
    clear_history()
    console.print("Historia została wyczyszczona.")
