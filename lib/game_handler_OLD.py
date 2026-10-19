import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# ================================================ #
# faal kardane log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
# ================================================ #
# tarife marahele conversation
CHOOSE_GAME, CHOOSE_PRICE, CHOOSE_PLAYER = range(3)
# ================================================ #


async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """in tabe moge shorue bazi run mishavad va payam entekhabe bazi ra nomayesh midahad

    Args:
        update (Update): az samt telegram data hara miaavarad
        context (ContextTypes.DEFAULT_TYPE): data hayi ke ma be telegram ersal mikonim

    Returns:
        int: adad marbut be marhale badi ra return mikonad
    """
    if update.message is not None:
        if update.message.from_user is not None:

            logger.info(
                "User %s started game conversation", update.message.from_user.first_name
            )

            await context.bot.send_message(
                chat_id=update.message.chat.id,
                reply_to_message_id=update.message.id,
                text="لطفا بازی مورد نظر خود را انتخاب کنید\nفعلا فقط یک بازی داریم",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [
                            "تاس", "هیچی", "هیچی"
                        ],
                        [
                            "❌"
                        ]
                    ]
                )
                # reply_markup=InlineKeyboardMarkup(
                #     [
                #         [
                #             InlineKeyboardButton(text="🎲", callback_data="dice_game"),
                #             InlineKeyboardButton(
                #                 text="هیچی", callback_data="nothing1_game"
                #             ),
                #             InlineKeyboardButton(
                #                 text="هیچی", callback_data="nothing2_game"
                #             ),
                #         ],
                #         [InlineKeyboardButton(text="❌", callback_data="cancel_game")],
                #     ]
                # ),
            )
            logger.info("\n***\nThis is the end of function\n***\n")
    return CHOOSE_GAME


async def choose_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """in tabe game entekhab shodera ra tashkhis dade va run mikonad

    Args:
        update (Update): az samt telegram data hara miaavarad
        context (ContextTypes.DEFAULT_TYPE): data hayi ke ma be telegram ersal mikonim

    Returns:
        int: adad marbut be marhale badi ra return mikonad
    """
    logger.info("\n***\nThis is the choose game function\n***\n")

    if update.callback_query is not None:
        if update.callback_query.data == "dice_game":

            logger.info("Dice game selected")

            if update.callback_query.message is not None:
                await context.bot.edit_message_text(
                    chat_id=update.callback_query.message.chat.id,
                    message_id=update.callback_query.message.message_id,
                    text="لطفا مبلغ ورودی را تعیین کنید\n(به عنوان پاسخ این پیام ریپلای کنید)",
                )
    logger.info("\n***\nThis is the choose game function\n***\n")
    return CHOOSE_PRICE


async def choose_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """in tabe mablaghe vorudi ra sabt mikonad

    Args:
        update (Update): az samt telegram data hara miaavarad
        context (ContextTypes.DEFAULT_TYPE): data hayi ke ma be telegram ersal mikonim

    Returns:
        int: adad marbut be marhale badi ra return mikonad
    """
    if update.message is not None:
        if update.message.from_user is not None:
            print("###############################")
            print(update.message)
            print("###############################")

            logger.info("User %s enterd price", update.message.from_user.first_name)

            # TODO agar mablagh kamtar ya mosavi mojudi karbar bud edame bede.
            # TODO agar payam be surat reply bud edame bede.

            await context.bot.send_message(
                chat_id=update.message.chat.id,
                reply_to_message_id=update.message.id,
                text="مبلغ تعیین شده برابر است با\n---$\nحالا لطفا تعداد بازیکن ها را مشخص کنید",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="1", callback_data="dice_game_player1"
                            ),
                            InlineKeyboardButton(
                                text="2", callback_data="dice_game_player2"
                            ),
                            InlineKeyboardButton(
                                text="3", callback_data="dice_game_player3"
                            ),
                        ],
                        [InlineKeyboardButton(text="❌", callback_data="cancel_game")],
                    ]
                ),
            )

    return CHOOSE_PLAYER



async def choose_player(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """in tabe tedad bazikon hara gerefte va manteg ra ijad mikonad

    Args:
        update (Update): az samt telegram data hara miaavarad
        context (ContextTypes.DEFAULT_TYPE): data hayi ke ma be telegram ersal mikonim

    Returns:
        int: adad marbut be marhale badi ra return mikonad
    """
    # TODO in tabe garar ast be tedad taiin shode karbar daryaft konad
    # yani roye sherkat click shavad
    # mablage taiin shode ba mojudi karbar mogayese shavad
    # 
    if update.callback_query is not None:
        if update.callback_query.data == "dice_game_player1":
            pass

        elif update.callback_query.data == "dice_game_player2":

            logger.info("Player set to 2")

            if update.callback_query.message is not None:
                await context.bot.edit_message_text(
                    chat_id=update.callback_query.message.chat.id,
                    message_id=update.callback_query.message.message_id,
                    text=f"بازیکن : {update.callback_query.message.chat.first_name}\nبازیکن : \nبرای شرکت کردن روی دکمه شرکت بزنید",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="🙋‍♂️شرکت میکنم🙋‍♂️", callback_data="game_on", 
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    text="❌", callback_data="cancel_game"
                                )
                            ],
                        ]
                    ),
                )

    return ConversationHandler.END

async def cancel_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """in tabe bazi ra cancel mikonad

    Args:
        update (Update): az samt telegram data hara miaavarad
        context (ContextTypes.DEFAULT_TYPE): data hayi ke ma be telegram ersal mikonim

    Returns:
        int: adad marbut be marhale PAYAN ra return mikonad
    """
    # TODO in tabe garar ast be tedad taiin shode karbar daryaft konad
    # yani roye sherkat click shavad
    # mablage taiin shode ba mojudi karbar mogayese shavad
    # 
    if update.callback_query is not None:
        if update.callback_query.data == "cancel_game":

            logger.info("Game is canceld")

            if update.callback_query.message is not None:
                await context.bot.edit_message_text(
                    chat_id=update.callback_query.message.chat.id,
                    message_id=update.callback_query.message.message_id,
                    text="بازی کنسل شد",
                )

    return ConversationHandler.END




# ============================================================= #
def dice_game_conversation() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^(دلاربازی|dollar game|بازی دلاری|بازیه دلاری)$"),
                start_game,
            ),
            # CallbackQueryHandler(cancel_game)
        ],
        states={
            CHOOSE_GAME: [MessageHandler(filters.ALL, choose_game)],
            CHOOSE_PRICE: [
                MessageHandler(
                    filters.Regex(r"^(\d+k|\d+m|\d+کا|\d+ام)$"), choose_price
                )
            ],
            CHOOSE_PLAYER: [MessageHandler(filters.ALL, choose_player)],
        },
        fallbacks=[MessageHandler(filters.ALL, cancel_game)],
    )
# ============================================================= #
