"""
NexusOmegaCore Telegram Bot - Main entry point.
"""

import logging
import signal
import threading
from types import FrameType

from telegram.ext import Application

from config import settings
from handlers import register_all_handlers
from services.grok_client import GrokClient
from services.db import init_db, close_db
from services.healthcheck import start_healthcheck_server

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.log_level.upper()),
)

logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    """Called after the Application is initialised."""
    await init_db()

    grok = GrokClient(api_key=settings.xai_api_key, base_url=settings.xai_base_url)
    application.bot_data["grok_client"] = grok
    
    logger.info("Bot initialized with GrokClient.")


async def post_shutdown(application: Application) -> None:
    """Called when the Application shuts down."""
    grok: GrokClient | None = application.bot_data.get("grok_client")
    if grok:
        await grok.close()
    await close_db()
    logger.info("Bot shutdown complete.")


def main() -> None:
    """
    Start the Telegram bot.
    """
    logger.info("Starting NexusOmegaCore Telegram Bot...")

    if settings.telegram_dry_run:
        logger.info(
            "Telegram dry-run mode enabled; skipping Telegram network startup "
            "for deterministic CI boot verification."
        )
        stop_event = threading.Event()

        def _handle_signal(signum: int, _frame: FrameType | None) -> None:
            logger.info("Dry-run mode received signal %s, shutting down.", signum)
            stop_event.set()

        signal.signal(signal.SIGTERM, _handle_signal)
        signal.signal(signal.SIGINT, _handle_signal)
        stop_event.wait()
        return

    health_server = None
    try:
        health_server = start_healthcheck_server("local.db", port=8080)
        logger.info("Healthcheck started on port 8080.")
    except Exception as e:
        logger.error(f"Healthcheck start failed: {e}")

    # Create application
    application = (
        Application.builder()
        .token(settings.telegram_bot_token)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    # Register all handlers
    register_all_handlers(application)

    # Start polling with graceful shutdown support for Cloud Run (SIGTERM)
    logger.info("Bot started successfully. Polling for updates...")
    try:
        application.run_polling(
            allowed_updates=["message", "callback_query"],
            stop_signals=(signal.SIGINT, signal.SIGTERM),
        )
    finally:
        if health_server:
            health_server.shutdown()
            health_server.server_close()
            logger.info("Healthcheck stopped.")


if __name__ == "__main__":
    main()
