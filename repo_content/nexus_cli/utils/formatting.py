from rich.console import Console
from rich.markdown import Markdown

console = Console()

def render_markdown(text: str) -> None:
    console.print(Markdown(text))
