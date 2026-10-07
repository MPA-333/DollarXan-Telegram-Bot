from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
)
from lib.calculate import add_dollar, get_dollar


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return None
    else:
        await context.bot.send_message(
            chat_id=update.message.chat.id,
            text="Bot is runnig\nFor use this bot use /help",
            reply_to_message_id=update.message.message_id,
        )
        return None


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query is None:
        if update.message is not None:
            await context.bot.send_message(
                chat_id=update.message.chat.id,
                text="This bot generates dollars.\nYou can generate dollars by typing the word 'dollar', 'money' or 'cash'\nTo check your balance, type 'my dollars'\nTo play with group members, type 'dollar game'",
                reply_to_message_id=update.message.message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="دلار", callback_data="generate_dollar"
                            ),
                            InlineKeyboardButton(
                                text="دلارهایم", callback_data="my_dollars"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="دلاربازی", callback_data="dollar_game"
                            )
                        ],
                    ]
                ),
            )
            return None
    else:
        if update.callback_query.data == "generate_dollar":
            if update.callback_query.message is not None:

                add_dollar(
                    update.callback_query.from_user.id,
                    update.callback_query.from_user.first_name,
                    update.callback_query.from_user.last_name,
                    update.callback_query.message.date,
                )

                dollars = get_dollar(update.callback_query.from_user.id)
                await context.bot.edit_message_text(
                    chat_id=update.callback_query.message.chat.id,
                    message_id=update.callback_query.message.message_id,
                    text=f"Your Dollar +3\nand is:\n{dollars}$",
                )




        elif update.callback_query.data == "my_dollars":
            pass
        elif update.callback_query.data == "dollar_game":
            pass
        return None
