"""
/help command handler.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command.

    Shows list of available commands.
    """
    help_text = """📚 <b>NexusOmegaCore - Pomoc</b>

<b>Podstawowe komendy:</b>
/start - Rozpocznij rozmowę
/help - Ta wiadomość
/mode - Zmień tryb AI (eco/smart/deep)
/provider - Wybierz providera AI (grok/claude/auto)

<b>Zarządzanie kontem:</b>
/unlock &lt;kod&gt; - Odblokuj dostęp DEMO
/subscribe - Kup subskrypcję FULL ACCESS
/buy - Kup kredyty (Telegram Stars)

<b>Dokumenty (FULL ACCESS):</b>
📎 Wyślij plik - Upload dokumentu do RAG

<b>Tryby AI:</b>
🌱 <b>ECO</b> - Szybki, ekonomiczny (Gemini Flash, Groq)
🧠 <b>SMART</b> - Zbalansowany (DeepSeek Reasoner, Gemini Thinking)
🔬 <b>DEEP</b> - Zaawansowany (Gemini 2.5 Pro, GPT-4o, Claude)

<b>Providery (wybierz przez /provider):</b>
- Google Gemini (2.0 Flash, Thinking, 2.5 Pro)
- DeepSeek (Chat, Reasoner)
- Groq (Llama 3.3 70B)
- OpenRouter (Llama free tier)
- xAI Grok (Beta)
- OpenAI (GPT-4o)
- Anthropic Claude (Sonnet)

<b>Funkcje:</b>
✅ Multi-provider AI z automatycznym fallback
✅ Wyszukiwanie w internecie (Brave Search)
✅ Dokumenty użytkownika (RAG)
✅ Pamięć konwersacji i preferencji
✅ Automatyczna klasyfikacja trudności
✅ Śledzenie kosztów
✅ ReAct agent z narzędziami

💬 Wyślij mi wiadomość, aby zacząć rozmowę!
"""

    await update.message.reply_text(help_text, parse_mode="HTML")
