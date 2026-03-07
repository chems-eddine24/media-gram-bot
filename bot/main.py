import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from telegram.request import HTTPXRequest
from handlers.start import start_handler, help_handler
from handlers.messages import url_handler, unknown_handler
from handlers.callbacks import format_choice_callback, quality_choice_callback, cancel_callback
from config import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def main() -> None:
    request = HTTPXRequest(
        connect_timeout=10,
        read_timeout=300,    
        write_timeout=300,   
        media_write_timeout=300,
        )
    app = Application.builder().token(settings.TOKEN).request(request).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, url_handler))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_handler))

    app.add_handler(CallbackQueryHandler(format_choice_callback, pattern="^audio:|^video:"))
    app.add_handler(CallbackQueryHandler(quality_choice_callback, pattern="^quality:"))
    app.add_handler(CallbackQueryHandler(cancel_callback, pattern="^cancel$"))

    app.run_polling()


if __name__ == "__main__":
    main()