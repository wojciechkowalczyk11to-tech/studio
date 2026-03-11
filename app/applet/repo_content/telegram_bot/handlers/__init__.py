from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters,
)

from .chat_handler_streaming import chat_message_streaming
from .document_handler import document_handler
from .help_handler import help_command
from .mode_handler import mode_command
from .provider_handler import provider_command
from .start_handler import start_command
from .subscribe_handler import (
    buy_command,
    precheckout_callback,
    subscribe_command,
    successful_payment_callback,
)
from .unlock_handler import unlock_command


def register_all_handlers(application: Application) -> None:
    """Register all bot handlers."""
    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mode", mode_command))
    application.add_handler(CommandHandler("provider", provider_command))
    application.add_handler(CommandHandler("unlock", unlock_command))
    application.add_handler(CommandHandler("subscribe", subscribe_command))
    application.add_handler(CommandHandler("buy", buy_command))

    # Register payment handlers
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    # Register message handlers
    application.add_handler(MessageHandler(filters.Document.ALL, document_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message_streaming))
