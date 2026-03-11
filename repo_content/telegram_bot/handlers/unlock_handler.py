"""
/unlock command handler.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.backend_client import get_backend_client
from services.user_cache import UserCache


async def unlock_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /unlock command.

    Unlocks DEMO access with unlock code.
    """
    user = update.effective_user

    # Check if code provided
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "⚠️ <b>Użycie:</b> /unlock &lt;kod&gt;\n\n"
            "Przykład: /unlock DEMO2024\n\n"
            "Nie masz kodu? Skontaktuj się z administratorem.",
            parse_mode="HTML",
        )
        return

    unlock_code = context.args[0]

    backend = get_backend_client()

    async with UserCache() as cache:
        try:
            # Unlock via backend
            response = await backend.unlock_demo(user.id, unlock_code)

            # Invalidate cache
            await cache.set_user_data(user.id, response, ttl=3600)

            await update.message.reply_text(
                f"✅ <b>Dostęp DEMO odblokowany!</b>\n\n"
                f"Twoja rola: <b>{response.get('role', 'demo')}</b>\n"
                f"Status: ✅ Autoryzowany\n\n"
                f"Możesz teraz korzystać z bota. Wyślij wiadomość aby zacząć!",
                parse_mode="HTML",
            )

        except Exception as e:
            error_message = str(e)

            if "401" in error_message or "Nieprawidłowy" in error_message:
                await update.message.reply_text(
                    "❌ <b>Nieprawidłowy kod odblokowania.</b>\n\nSprawdź kod i spróbuj ponownie.",
                    parse_mode="HTML",
                )
            elif "404" in error_message:
                await update.message.reply_text(
                    "❌ <b>Użytkownik nie istnieje.</b>\n\nNajpierw użyj /start aby się zarejestrować.",
                    parse_mode="HTML",
                )
            else:
                await update.message.reply_text(f"❌ Błąd: {error_message}\n\nSpróbuj ponownie.")
