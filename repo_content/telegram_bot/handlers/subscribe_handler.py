"""
/subscribe command handler for Telegram Stars payments.
"""

from telegram import LabeledPrice, Update
from telegram.ext import ContextTypes

from services.user_cache import UserCache
from services.backend_client import get_backend_client

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /subscribe command.

    Shows subscription options with Telegram Stars pricing.
    """
    backend = get_backend_client()
    try:
        pricing = await backend.get_pricing()
    except Exception as e:
        await update.message.reply_text("❌ Błąd pobierania cennika. Spróbuj później.")
        return
    finally:
        await backend.close()

    pricing_text = "\n".join([f"🌟 **{p['stars']} Stars** — {p['title']}" for p in pricing.values()])
    products_text = "\n".join([f"- {k}" for k in pricing.keys()])

    subscribe_text = f"""💎 **Subskrypcja FULL_ACCESS**

**Co zyskujesz:**
✅ Dostęp do wszystkich providerów AI
✅ Tryb DEEP (GPT-4, Claude)
✅ Upload dokumentów (RAG)
✅ Wyszukiwanie w internecie
✅ Wyższy limit zapytań (100/min)

**Cennik:**

{pricing_text}

**Jak kupić:**
Użyj komendy /buy <produkt>

Dostępne produkty:
{products_text}

💡 **Telegram Stars** to wirtualna waluta Telegram.
Możesz kupić Stars w aplikacji Telegram.
"""

    await update.message.reply_text(subscribe_text, parse_mode="HTML")


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /buy command.

    Initiates Telegram Stars payment.
    """
    backend = get_backend_client()
    try:
        pricing = await backend.get_pricing()
    except Exception as e:
        await update.message.reply_text("❌ Błąd pobierania cennika. Spróbuj później.")
        return
    finally:
        await backend.close()

    # Check if product specified
    if not context.args or len(context.args) == 0:
        products_text = "\n".join([f"- {k}" for k in pricing.keys()])
        await update.message.reply_text(
            f"⚠️ **Użycie:** /buy <produkt>\n\n"
            f"Dostępne produkty:\n{products_text}\n\n"
            f"Przykład: /buy full_access_monthly",
            parse_mode="HTML",
        )
        return

    product_id = context.args[0]

    if product_id not in pricing:
        await update.message.reply_text(
            f"❌ Nieznany produkt: {product_id}\n\nUżyj /subscribe aby zobaczyć dostępne produkty."
        )
        return

    product = pricing[product_id]

    # Create invoice
    await update.message.reply_invoice(
        title=product["title"],
        description=product["description"],
        payload=f"product:{product_id}",
        provider_token="",  # Empty for Telegram Stars
        currency="XTR",  # Telegram Stars currency
        prices=[LabeledPrice(label=product["title"], amount=product["stars"])],
    )


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle pre-checkout query.

    Validates payment before processing.
    """
    query = update.pre_checkout_query

    # Always approve (validation done on backend)
    await query.answer(ok=True)


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle successful payment.

    Processes payment and grants benefits.
    """
    user = update.effective_user
    payment = update.message.successful_payment
    backend = get_backend_client()

    async with UserCache() as cache:
        try:
            # Extract product_id from payload
            payload = payment.invoice_payload
            product_id = payload.split(":")[1] if ":" in payload else "unknown"

            # Get token
            token = await cache.get_user_token(user.id)

            if not token:
                await update.message.reply_text(
                    "⚠️ Nie jesteś zalogowany. Użyj /start aby się zarejestrować."
                )
                return

            # Process payment via backend
            await backend.process_payment(token, product_id, payment.total_amount)

            await update.message.reply_text(
                f"✅ <b>Płatność zakończona pomyślnie!</b>\n\n"
                f"Produkt: {product_id}\n"
                f"Zapłacono: {payment.total_amount} Stars\n\n"
                f"Twoje korzyści zostały aktywowane. Użyj /start aby odświeżyć status.",
                parse_mode="HTML",
            )

            # Invalidate cache to force refresh
            await cache.set_user_data(user.id, {}, ttl=1)

        except Exception as e:
            if hasattr(e, "status_code") and e.status_code == 409:
                await update.message.reply_text("⚠️ Ta płatność została już przetworzona.")
                return
            await update.message.reply_text(
                f"❌ Błąd przetwarzania płatności: {str(e)}\n\nSkontaktuj się z supportem."
            )
        finally:
            await backend.close()
