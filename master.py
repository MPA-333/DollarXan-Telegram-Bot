from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from lib.command_handler import (
    start_cmd,
    help_cmd,
)


if __name__ == "__main__":
    dollarxan = (
        ApplicationBuilder()
        .token("8700251942:AAGdoMOEKGWgbsJ8RlACsAqFa3tAy8DQcAU")
        .build()
    )

    dollarxan.add_handler(CommandHandler("start", start_cmd))
    dollarxan.add_handler(CommandHandler("help", help_cmd))
    dollarxan.add_handler(CallbackQueryHandler(help_cmd))
    dollarxan.run_polling()
