"""
/start command handler.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.backend_client import get_backend_client
from services.user_cache import UserCache


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command.

    Registers user and shows welcome message.
    """
    user = update.effective_user
    backend = get_backend_client()

    async with UserCache() as cache:
        try:
            # Register user
            response = await backend.register_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
            )

            # Cache token
            await cache.set_user_token(user.id, response["token"])

            # Welcome message
            role = response["role"]
            authorized = response["authorized"]

            welcome_text = f"""👋 Witaj w <b>NexusOmegaCore</b>!

Twoja rola: <b>{role}</b>
Status: {"✅ Autoryzowany" if authorized else "⚠️ Nieautoryzowany"}

🤖 Jestem zaawansowanym asystentem AI z dostępem do:
- 7 providerów AI (Gemini, DeepSeek, Groq, OpenRouter, Grok, OpenAI, Claude)
- Bazy wiedzy (Vertex AI Search)
- Twoich dokumentów (RAG)
- Internetu (Brave Search)

📚 <b>Dostępne komendy:</b>
/help - Lista komend
/mode - Zmień tryb AI (eco/smart/deep)
/unlock - Odblokuj dostęp DEMO
/subscribe - Kup subskrypcję

💬 Wyślij mi wiadomość, aby zacząć rozmowę!
"""

            if not authorized:
                welcome_text += "\n⚠️ <b>Uwaga:</b> Musisz odblokować dostęp: /unlock &lt;kod&gt;"

            await update.message.reply_text(welcome_text, parse_mode="HTML")

        except Exception as e:
            await update.message.reply_text(
                f"❌ Błąd rejestracji: {str(e)}\n\nSpróbuj ponownie: /start"
            )
