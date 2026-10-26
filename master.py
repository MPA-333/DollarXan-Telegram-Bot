from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from lib.command_handler import (
    start_cmd,
    help_cmd,
    query_handler_cmd,
    generate_dollar_cmd,
    get_dollar_cmd,
    say_goodnight_cmd,
)
from lib.game_handler import (
    initialize_game,
    game_query_handler,
    choose_price,
    choose_winner,
)
from secret_key import BOT_TOKEN
# ===================================================================


def main():
    dollarxan = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    dollarxan.add_handler(CommandHandler("start", start_cmd))
    dollarxan.add_handler(CommandHandler("help", help_cmd))
    dollarxan.add_handler(
        CallbackQueryHandler(query_handler_cmd, pattern=r"^\w+_dollars$")
    )
    dollarxan.add_handler(
        MessageHandler(
            filters.Regex("^(دلاربازی|بازی دلاری|بازیه دلاری|dollar game)$"),
            initialize_game,
        )
    )
    dollarxan.add_handler(
        CallbackQueryHandler(game_query_handler, pattern=r"^\w+_game$")
    )
    dollarxan.add_handler(
        MessageHandler(filters.Regex(r"^(\d+k|\d+m|\d+کا|\d+ام|\d+|\d+دلار|\d+\$)$"), choose_price)
    )
    dollarxan.add_handler(
        MessageHandler(filters.Dice(), choose_winner)
    )
    dollarxan.add_handler(
        MessageHandler(
            filters.Regex("^(دلار|پول|money|dolar|dollar|cash|کش|)$"),
            generate_dollar_cmd,
        )
    )
    dollarxan.add_handler(
        MessageHandler(
            filters.Regex(
                "^(دلارهام|دلارهایم|دلار هایم|دلار هام|موجودی|موجودی من|موجودی‌من|my dollar|چقدر دلار دارم)$"
            ),
            get_dollar_cmd,
        )
    )
    dollarxan.add_handler(
        MessageHandler(
            filters.Regex(
                "^(شب خوش ربات|شب بخیر ربات|good night bot|گجن خیر ربات|برایم شب بخیر بگو ربات|شب بخیر بگو ربات|میخوام بخوایم ربات|رفتم بخوابم ربات)$"
            ),
            say_goodnight_cmd,
        )
    )
    dollarxan.run_polling(allowed_updates=Update.ALL_TYPES)
# =================================================================== #


if __name__ == "__main__":
    main()
