from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    CallbackQueryHandler,
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

# New GigaGrok Handlers
from .voice_handler import handle_voice, voice_toggle
from .image_handler import handle_photo, image_command
from .search_handler import websearch_command, xsearch_command
from .power_handler import gigagrok_command
from .github_handler import github_command, workspace_command
from .conversation_handler import clear_command, profile_command, stats_command, system_command, think_command
from .collection_handler import collection_command
from .collection_search_handler import collectionsearch_command
from .admin_handler import adduser_command, removeuser_command, users_command
from .file_handler import file_command, handle_document


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

    # New GigaGrok Command Handlers
    application.add_handler(CommandHandler("voice", voice_toggle))
    application.add_handler(CommandHandler("image", image_command))
    application.add_handler(CommandHandler("websearch", websearch_command))
    application.add_handler(CommandHandler("xsearch", xsearch_command))
    application.add_handler(CommandHandler("gigagrok", gigagrok_command))
    application.add_handler(CommandHandler("github", github_command))
    application.add_handler(CommandHandler("workspace", workspace_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("system", system_command))
    application.add_handler(CommandHandler("think", think_command))
    application.add_handler(CommandHandler("collection", collection_command))
    application.add_handler(CommandHandler("collectionsearch", collectionsearch_command))
    application.add_handler(CommandHandler("users", users_command))
    application.add_handler(CommandHandler("adduser", adduser_command))
    application.add_handler(CommandHandler("removeuser", removeuser_command))
    application.add_handler(CommandHandler("file", file_command))

    # Register payment handlers
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    # Register message handlers
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message_streaming))
