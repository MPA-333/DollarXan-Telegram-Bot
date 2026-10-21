from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
from lib.calculator import get_dollar, update_dollar
from uuid import uuid4
import re


class Player:
    def __init__(self, id: int, name: str, score: int, is_paid: bool) -> None:
        self.id = id
        self.name = name
        self.score = score
        self.is_paid = is_paid


class Game:
    STATUS = {
        0: "Off",
        1: "ChooseType",
        2: "ChooseFee",
        3: "ChoosePlayer",
        4: "Start",
        5: "Running",
        6: "ChooseWinner",
        7: "End",
    }

    def __init__(
        self,
        game_type="",
        player_count=0,
        entry_fee=0,
        game_chat_id=0,
        game_message_id=0,
        user_message_id=0,
        creator_id=0,
        creator_name="",
    ) -> None:
        self.id = uuid4()
        self.type = game_type
        self.player_count = player_count
        self.entry_fee = entry_fee
        self.main_chat_id = game_chat_id
        self.main_message_id = game_message_id
        self.user_message_id = user_message_id
        self.creator_id = creator_id
        self.creator_name = creator_name
        self.players_data: list[Player] = []
        self.status = Game.STATUS[0]

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, Game):
            return False
        return self.id == obj.id

    def __hash__(self) -> int:
        return hash(self.id)


async def expire_game(context: ContextTypes.DEFAULT_TYPE):
    if context.job:
        id = context.job.data.get("game_id")  # type: ignore
        chat_id = context.job.data.get("chat_id")  # type: ignore
        message_id = context.job.data.get("message_id")  # type: ignore

        if id in context.application.bot_data.keys():
            context.application.bot_data.pop(id)
            print(f"game with id {id} is deleted from bot context")
            try:
                await context.bot.delete_message(
                    chat_id=chat_id,
                    message_id=message_id,
                )
            except:
                pass
        else:
            print(f"Not Found\ngame with id {id} not found :(")


async def initialize_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message:
        if update.message.from_user:
            if update.message.from_user.id not in context.application.bot_data.keys():
                game = Game()

                game.status = Game.STATUS[1]
                game.creator_id = update.message.from_user.id  # set creators id
                game.creator_name = update.message.from_user.full_name
                game.main_chat_id = update.message.chat.id
                game.user_message_id = update.message.id

                context.application.bot_data[update.message.from_user.id] = game

                # print("init game")
                # print(update.message.reply_to_message)
                # print("#################################")

                sent_message = await context.bot.send_message(
                    chat_id=game.main_chat_id,
                    reply_to_message_id=game.user_message_id,
                    text="لطفا بازی مورد نظر خود را انتخاب کنید\nفعلا فقط یک بازی داریم",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="🎲", callback_data="dice_game"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="❌", callback_data="cancel_game"
                                )
                            ],
                        ]
                    ),
                )

                assert context.job_queue is not None
                context.job_queue.run_once(
                    expire_game,
                    when=150,
                    data={
                        "game_id": update.message.from_user.id,
                        "chat_id": update.message.chat.id,
                        "message_id": sent_message.message_id,
                    },
                    name=f"expire game of user {update.message.from_user.id}",
                    user_id=update.message.from_user.id,
                )

                game.main_message_id = sent_message.message_id
                print("game id (set step): ", game.id)
                print("main message id (set step): ", game.main_message_id)
                print("main message id (update method): ", sent_message.message_id)
                print("################")

            else:
                sent_message = await context.bot.send_message(
                    chat_id=update.message.chat.id,
                    reply_to_message_id=update.message.id,
                    text="به دلارخان استراحت بده\nپس لطفا چند دقیقه بعد امتحان کن",
                )


async def game_query_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if update.callback_query:
        if update.callback_query.data == "dice_game":

            game = context.application.bot_data.get(update.callback_query.from_user.id)
            if game:
                if update.callback_query.from_user.id == game.creator_id:

                    if update.callback_query.message:

                        # game.main_message_id = update.callback_query.message.message_id
                        game.type = "dice"
                        game.status = Game.STATUS[2]
                        print("game id (set step): ", game.id)
                        print("main message id (use step): ", game.main_message_id)
                        print(
                            "main message id (update method): ",
                            update.callback_query.message.message_id,
                        )
                        print("################")

                        await context.bot.edit_message_text(
                            chat_id=game.main_chat_id,
                            message_id=game.main_message_id,
                            text="لطفا مبلغ ورودی را تعیین کنید\n(به عنوان پاسخ این پیام ریپلای کنید)",
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="❌", callback_data="cancel_game"
                                        )
                                    ]
                                ]
                            ),
                        )

        elif update.callback_query.data == "cancel_game":

            # TODO باید مطمئن شویم هرکی پول پرداخت کرده بهش برگرده

            game = context.application.bot_data.get(update.callback_query.from_user.id)
            if game:
                if update.callback_query.from_user.id == game.creator_id:

                    if update.callback_query.message:

                        game.status = Game.STATUS[7]
                        print("game id (set step): ", game.id)
                        print("main message id (cancel step): ", game.main_message_id)
                        print(
                            "main message id (update method): ",
                            update.callback_query.message.message_id,
                        )
                        print("################")

                        await context.bot.edit_message_text(
                            chat_id=game.main_chat_id,
                            message_id=game.main_message_id,
                            text="بازی کنسل شد",
                        )

        elif update.callback_query.data == "one_player_game":
            game = context.application.bot_data.get(update.callback_query.from_user.id)

            if game and update.callback_query.from_user.id == game.creator_id and game.status == Game.STATUS[3]:
                # game = Game() # WARNING

                game.player_count = 1

                # game.players_data = [Player(id=game.creator_id, score=0, is_paid=False)]

                # if update_dollar(game.creator_id, game.entry_fee):
                #     game.status = Game.STATUS[4]

                print("1 player mod activated")



        elif update.callback_query.data == "two_player_game":
            game = context.application.bot_data.get(update.callback_query.from_user.id)

            if game and update.callback_query.from_user.id == game.creator_id and game.status == Game.STATUS[3]:
                # game = Game()

                
                game.player_count = 2

                #  PLAYER 1
                player1 = Player(id=game.creator_id, name=game.creator_name, score=0, is_paid=False)
                game.players_data.append(player1)

                #  PLAYER 1
                player2 = Player(id=12345678, name="Ali", score=0, is_paid=False)
                game.players_data.append(player2)

                # "{"+ f"player_{x+1}" + "}"
                text_list: list[str] = [f"کاربر{x+1}: " + "{name}" + "\n" for x in range(game.player_count)]

                text_template = "لطفا برای این که وارد بازی شوید\nروی شرکت کردن بزنید\n\n"

                result: str = ""

                for text in text_list:
                    text_template += f"{text}"

                for player in game.players_data:
                    result = text_template.replace("{name}", player.name, 1)

                if "{name}" in result:
                    result = result.replace("{name}", " ")

                

                # i = 0
                # for str_player in text_list:
                #     text_template += f"{str_player}"

                #     try:
                #         if game.players_data[i]:
                #             result = text_template.replace("{name}", game.players_data[i].name, 1)
                #             print(game.players_data[i], i)
                #             print(result)                            

                #     except IndexError:
                #         result = text_template.
                #         print("Index Out of list range")
                #     finally:
                #         print("**\nI AM IN FINALLYYYYYYYYYYYYYYY\n**")
                #         i += 1
                    

                if result == "":
                    result = "لطفا برای این که وارد بازی شوید\nروی شرکت کردن بزنید\n\nمتاسفانه در گرفتن نام شرکت کنندگان مشکلی پیش آمد"
                
                await context.bot.edit_message_text(
                    chat_id=game.main_chat_id,
                    message_id=game.main_message_id,
                    text=result,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="🙋‍♂️شرکت میکنم🙋‍♂️", callback_data="join_game"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="❌", callback_data="cancel_game"
                                )
                            ]
                        ]
                    ),
                )

                print("2 player mod activated")




        elif update.callback_query.data == "three_player_game":
            game = context.application.bot_data.get(update.callback_query.from_user.id)
            if game and update.callback_query.from_user.id == game.creator_id and game.status == Game.STATUS[3]:
                
                game.player_count = 3
                
                print("3 player mod activated")



async def choose_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("CHOOSE PRICE Entierd")

    if update.message:
        print("update.message is OK")

        if update.message.from_user:
            print("update.message.from_user is OK")

            game = context.application.bot_data.get(update.message.from_user.id)

            if (
                game
                and game.creator_id == update.message.from_user.id
                and game.status == Game.STATUS[2]
                and update.message.reply_to_message
            ):
                if update.message.text:
                    value = await verify_user_value(update.message.text)
                    print("returned value is:", value)
                    print(update.message.text)
                    if value:
                        user_dollar = get_dollar(game.creator_id)
                        if user_dollar and value <= user_dollar:
                            game.entry_fee = value
                            game.status = Game.STATUS[3]
                            await context.bot.edit_message_text(
                                chat_id=game.main_chat_id,
                                message_id=game.main_message_id,
                                text="لطفا تعداد بازیکن ها را تعیین کنید\n(یکی از اعداد زیر را انتخاب کنید)",
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [
                                            InlineKeyboardButton(
                                                text="1",
                                                callback_data="one_player_game",
                                            ),
                                            InlineKeyboardButton(
                                                text="2",
                                                callback_data="two_player_game",
                                            ),
                                            InlineKeyboardButton(
                                                text="3",
                                                callback_data="three_player_game",
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

                        else:
                            print("You not have enough dollar")
                            await context.bot.edit_message_text(
                                chat_id=game.main_chat_id,
                                message_id=game.main_message_id,
                                text="مبلغ وارد شده از موجودی شما بیشتر است\nدوباره امتحان کنید",
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [
                                            InlineKeyboardButton(
                                                text="❌", callback_data="cancel_game"
                                            )
                                        ]
                                    ]
                                ),
                            )
                else:
                    print("message has no text :(")


async def verify_user_value(text: str) -> int | None:
    """in tabe reshte migirad va an ra be adad tabdil mokonad
    reshte mitavanad 10k ya 10m bashad va moshabeh haye an

    Args:
        text (str): 1000 ya 1k ya ۱کا ya ...

    Returns:
        int|None: adad hasel az reshte ra midahad ya None midahad
    """

    text = text.strip().lower()

    translation_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

    text = text.translate(translation_english)

    result = re.fullmatch(r"(\d+(?:\.\d)?)\s*([kmامکا]*|دلار)", text)
    if result:
        number = result.group(1)
        suffix = result.group(2)

        try:
            number = int(number)

            if suffix in ("k", "کا"):
                number *= 1_000

            elif suffix in ("m", "ام"):
                number *= 1_000_000

            elif suffix == "":
                pass

            elif suffix == "دلار":
                pass

            else:
                print("Error from input :(")

            return number

        except:
            print("converted to int fail :(")
            return None
    else:
        print("Not Match :(")
        return None
