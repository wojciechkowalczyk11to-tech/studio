"""
/mode command handler.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.user_cache import UserCache


async def mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /mode command.

    Allows user to change AI mode (eco, smart, deep).
    """
    user = update.effective_user

    async with UserCache() as cache:
        # Get current mode
        current_mode = await cache.get_user_mode(user.id) or "eco"

        # Check if mode argument provided
        if context.args and len(context.args) > 0:
            new_mode = context.args[0].lower()

            if new_mode not in ("eco", "smart", "deep"):
                await update.message.reply_text("⚠️ Nieprawidłowy tryb. Dostępne: eco, smart, deep")
                return

            # Set new mode
            await cache.set_user_mode(user.id, new_mode)

            mode_descriptions = {
                "eco": "🌱 <b>ECO</b> - Szybki, ekonomiczny (Gemini 2.0 Flash, Groq)",
                "smart": "🧠 <b>SMART</b> - Zbalansowany (DeepSeek Reasoner, Gemini Thinking)",
                "deep": "🔬 <b>DEEP</b> - Zaawansowany (Gemini 2.5 Pro, GPT-4o, Claude) - wymaga FULL ACCESS",
            }

            await update.message.reply_text(
                f"✅ Zmieniono tryb na: {mode_descriptions[new_mode]}",
                parse_mode="HTML",
            )

        else:
            # Show current mode and options
            mode_info = f"""🎛 <b>Aktualny tryb:</b> {current_mode.upper()}

<b>Dostępne tryby:</b>

🌱 <b>ECO</b> - Szybki, ekonomiczny
   Providery: Gemini 2.0 Flash, Groq, DeepSeek Chat
   Koszt: ~$0
   Użyj: <code>/mode eco</code>

🧠 <b>SMART</b> - Zbalansowany
   Providery: DeepSeek Reasoner, Gemini Thinking
   Koszt: ~$0.001-0.01 / zapytanie
   Użyj: <code>/mode smart</code>

🔬 <b>DEEP</b> - Zaawansowany (wymaga FULL ACCESS)
   Providery: DeepSeek, Gemini 2.5 Pro, GPT-4o, Claude Sonnet
   Koszt: ~$0.01-0.10 / zapytanie
   Użyj: <code>/mode deep</code>

💡 <b>Wskazówka:</b> Bot automatycznie wybiera tryb na podstawie trudności zapytania.
🔌 Użyj <code>/provider</code> aby wymusić konkretnego providera.
"""

            await update.message.reply_text(mode_info, parse_mode="HTML")
