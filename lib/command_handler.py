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
            text="ربات روشنه\nاگه نمیدونی چطور ازش استفاده کنی بزن /help",
            reply_to_message_id=update.message.message_id,
        )
        return None


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.callback_query is None:
        if update.message is not None:
            await context.bot.send_message(
                chat_id=update.message.chat.id,
                text="این ربات دلار تولید میکند\nشما میتوانید دلار تولید کنید با تایپ کردن 'دلار' , 'پول'\nبرای مشاهده موجودی، تایپ کنید 'دلارهام'\nبرای بازی کردن هم تایپ کنید 'دلاربازی'",
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

                waiting_time = add_dollar(
                    update.callback_query.from_user.id,
                    update.callback_query.from_user.first_name,
                    update.callback_query.from_user.last_name,
                    update.callback_query.message.date,
                )
                if waiting_time:
                    await context.bot.edit_message_text(
                        chat_id=update.callback_query.message.chat.id,
                        message_id=update.callback_query.message.message_id,
                        text=f"{waiting_time}\nصبر کنید",
                    )
                else:
                    dollars = get_dollar(update.callback_query.from_user.id)
                    await context.bot.edit_message_text(
                        chat_id=update.callback_query.message.chat.id,
                        message_id=update.callback_query.message.message_id,
                        text=f"دلارهایت +3\nموجودیت:\n{dollars}$",
                    )

        elif update.callback_query.data == "my_dollars":
            # TODO
            pass
        elif update.callback_query.data == "dollar_game":
            # TODO
            pass
        return None


async def generate_dollar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message is not None:
        if update.message.from_user is not None:

            # print(update.message.date)
            # print("*********************")
            # print(update.message)

            waiting_time = add_dollar(
                update.message.from_user.id,
                update.message.from_user.first_name,
                update.message.from_user.last_name,
                update.message.date,
            )
            if waiting_time:
                await context.bot.send_message(
                    chat_id=update.message.chat.id,
                    reply_to_message_id=update.message.id,
                    text=f"دلارخان سرش شولوغه\n{waiting_time}ثانیه صبر کنید",
                )
            else:
                dollars = get_dollar(update.message.from_user.id)
                await context.bot.send_message(
                    chat_id=update.message.chat.id,
                    text=f"دلارهایت +3\nو موجودیت:\n{dollars}$",
                    reply_to_message_id=update.message.id,
                )
