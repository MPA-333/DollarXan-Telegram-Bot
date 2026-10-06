from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
)
from lib.command_handler import start_cmd
# ----------------------------------------------------- #


if __name__ == "__main__":
    dollarxan = (
        ApplicationBuilder()
        .token("8700251942:AAGdoMOEKGWgbsJ8RlACsAqFa3tAy8DQcAU")
        .build()
    )

    dollarxan.add_handler(CommandHandler("start", start_cmd))
    dollarxan.run_polling()
