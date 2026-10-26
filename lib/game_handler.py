from collections import defaultdict

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
    def __init__(self, id: int, name: str, score: int, is_paid: bool, is_winner: bool) -> None:
        self.id = id
        self.name = name
        self.score = score
        self.is_paid = is_paid
        self.is_winner = is_winner

    def __str__(self) -> str:
        return f"{self.id}|{self.name}|{self.score}|"



class Game:
    STATUS = {
        0: "Off",
        1: "ChooseType",
        2: "ChooseFee",
        3: "ChoosePlayer",
        4: "Starting",
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
        self.finished_player: list[Player] = []
        self.status = Game.STATUS[0]

    def get_players_id(self) -> tuple[int,]:
        ids = []
        for player in self.players_data:
            ids.append(player.id)
        return tuple(ids)

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, Game):
            return False
        return self.id == obj.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return f"{self.creator_id}|{self.creator_name}|{self.status}|{self.player_count}"


async def expire_game(context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.job:
        id = context.job.data.get("game_id")  # type: ignore
        game = context.job.data.get("game")  # type: ignore
        chat_id = context.job.data.get("chat_id")  # type: ignore
        message_id = context.job.data.get("message_id")  # type: ignore

        if id in context.application.bot_data.keys():
            if context.user_data and context.user_data["game"]:
                context.user_data.pop("game")
            context.application.bot_data.pop(id)
            del game
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

                # assert context.job_queue is not None
                context.job_queue.run_once( # type: ignore
                    expire_game,
                    when=150,
                    data={
                        "game_id": update.message.from_user.id,
                        "game": game,
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

            if (
                game
                and update.callback_query.from_user.id == game.creator_id
                and game.status == Game.STATUS[3]
            ):
                # game = Game() # WARNING

                game.player_count = 1

                # gablan mojudi in karbar check shode va bishtar az entry_fee ast.
                if update_dollar(update.callback_query.from_user.id, -game.entry_fee):
                    game.players_data.append(Player(id=game.creator_id, name=game.creator_name, score=0, is_paid=True, is_winner=False))

                    context.user_data["game"] = game # type: ignore
                    # print(f"user: {user_id} | context: {context.user_data}")
                    game.status = Game.STATUS[4]
                else:
                    print("update dollar Faild :(\t{1 player mod}")

                # player = Player(
                #     id=game.creator_id, name=game.creator_name, score=0, is_paid=False
                # )
                # game.players_data.append(player)

                print("1 player mod activated")

                await add_player_or_run_game(game.creator_id, game.creator_name, game, context)

        elif update.callback_query.data == "two_player_game":
            game = context.application.bot_data.get(update.callback_query.from_user.id)

            if (
                game
                and update.callback_query.from_user.id == game.creator_id
                and game.status == Game.STATUS[3]
            ):
                # game = Game() # WARNING

                game.player_count = 2

                # gablan mojudi in karbar check shode va bishtar az entry_fee ast.
                if update_dollar(update.callback_query.from_user.id, -game.entry_fee):
                    game.players_data.append(Player(id=game.creator_id, name=game.creator_name, score=0, is_paid=True, is_winner=False))

                    context.user_data["game"] = game # type: ignore
                    # print(f"user: {user_id} | context: {context.user_data}")
                    game.status = Game.STATUS[4]
                else:
                    print("update dollar Faild :(\t{2 player mod}")

                #  PLAYER 1
                # player1 = Player(
                #     id=game.creator_id, name=game.creator_name, score=0, is_paid=False
                # )
                # game.players_data.append(player1)

                #  PLAYER 2
                # player2 = Player(id=12345678, name="Ali", score=0, is_paid=False)
                # game.players_data.append(player2)

                text = generate_text_for_join_user(game)
                # "{"+ f"player_{x+1}" + "}"
                # text_list: list[str] = [f"کاربر{x+1}: " + "{"+ f"player_{x+1}" + "}" + "\n" for x in range(game.player_count)]

                # text_template = "لطفا برای این که وارد بازی شوید\nروی شرکت کردن بزنید\n\n"

                # result: str = ""

                # for text in text_list:
                # text_template += f"{text}"

                # result = text_template
                # for i, player in enumerate(game.players_data):
                # print("index is: " + f"{i}")
                # result = result.replace("{player_"+ f"{i+1}" + "}", player.name, 1)
                # print("\n***\n"+ result + "\n***\n")

                # print(r"\{player_\d\}")

                # find_text_list = re.findall(r"\{player_\d\}", result)
                # if find_text_list:
                # print(find_text_list)
                # for item in find_text_list:
                # result = result.replace(item, " ")

                # if result == "":
                # result = "لطفا برای این که وارد بازی شوید\nروی شرکت کردن بزنید\n\nمتاسفانه در گرفتن نام شرکت کنندگان مشکلی پیش آمد"

                await context.bot.edit_message_text(
                    chat_id=game.main_chat_id,
                    message_id=game.main_message_id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="🙋‍♂️شرکت میکنم🙋‍♂️",
                                    callback_data=f"{game.creator_id}_join_game",
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

                print("2 player mod activated")

        elif update.callback_query.data == "three_player_game":
            game = context.application.bot_data.get(update.callback_query.from_user.id)
            if (
                game
                and update.callback_query.from_user.id == game.creator_id
                and game.status == Game.STATUS[3]
            ):

                game.player_count = 3

                if update_dollar(update.callback_query.from_user.id, -game.entry_fee):
                    game.players_data.append(Player(id=game.creator_id, name=game.creator_name, score=0, is_paid=True, is_winner=False))

                    context.user_data["game"] = game # type: ignore
                    # print(f"user: {user_id} | context: {context.user_data}")
                    game.status = Game.STATUS[4]
                else:
                    print("update dollar Faild :(\t{2 player mod}")

                text = generate_text_for_join_user(game)
                await context.bot.edit_message_text(
                    chat_id=game.main_chat_id,
                    message_id=game.main_message_id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="🙋‍♂️شرکت میکنم🙋‍♂️",
                                    callback_data=f"{game.creator_id}_join_game",
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

                print("3 player mod activated")

        elif update.callback_query.data and "_join_game" in update.callback_query.data:
            # print("regex query Success")
            # print(update.callback_query.data)

            if update.callback_query.from_user:
                game_creator_id = None

                text: str = update.callback_query.data

                id_and_text = re.fullmatch(r"^(\d+)_join_game$", text)

                if id_and_text:
                    id = id_and_text.group(1)
                    # print("Game Creator id is:")
                    # print(id)
                    game_creator_id = id

                # print(type(game_creator_id))
                if game_creator_id:
                    game = context.application.bot_data.get(int(game_creator_id))
                    # print(game)
                    if game:
                        await add_player_or_run_game(
                            update.callback_query.from_user.id,
                            update.callback_query.from_user.full_name,
                            game,
                            context,
                        )
            # game = context.application.bot_data.get(update.callback_query.from_user.id)
            # if game and update.callback_query.from_user.id == game.creator_id and game.status == Game.STATUS[3]:

            #     game.player_count = 3

            #     print("3 player mod activated")

        elif update.callback_query.data == "run_game":
            print("\n\n***Game is RUNNIG ***\n\n")

            game: Game|None = context.application.bot_data.get(update.callback_query.from_user.id)
            if (
                game
                and update.callback_query.from_user.id == game.creator_id
                and game.status == Game.STATUS[5]
            ):
                game.status = Game.STATUS[6]


                await context.bot.edit_message_text(
                    chat_id=game.main_chat_id,
                    message_id=game.main_message_id,
                    text="لطفا استیکر 🎲 را در پاسخ به این پیام ارسال کنید\n(یعنی هر بازیکن استیکر تاس را به عنوان ریپلای همین پیام ارسال کند)\n\nمنتظرم...",
                )


async def choose_winner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("CHOOSE WINNER FUNCTION")
    print(f"context.user_data: {context.user_data}")

    if update.message and update.message.from_user and context.user_data:

        game: Game|None = context.user_data.get("game")
        

        if (
            game
            and update.message.from_user.id in game.get_players_id()
            and game.status == Game.STATUS[6]
            and update.message.reply_to_message
        ):
            print("ALL CONDITION PASSED")

            print(f"user: {update.message.from_user.id} | context.user_data: {context.user_data}")

            if game.player_count > 1:
                if game.players_data:
                    for player in game.players_data:
                        if player.id == update.message.from_user.id:
                            
                            dice = update.message.dice
                            if dice and dice.emoji == "🎲":
                                player.score = dice.value
                                game.finished_player.append(player)
                                game.players_data.remove(player)
                                context.user_data.pop("game")
                                print(f"megdar dice daruaft shod: {player.score} | user is: {update.message.from_user.full_name}\nplayer is : {player.name}")
                            
                            else:
                                player.score = 0
                                print("sticker dorost nist")
                else:
                    print("list player_data is [] -> empty")
                

            if game.player_count == 1:
                pass
                # TODO halat single player
                # garar ast khode robat tas bendazad va natije ba robat sanjesh mishavad.


            if game.player_count == len(game.finished_player):
                
                # is_tie, reward, winners = calculate_winner(game)

                text = generate_text_for_show_winners(game, *calculate_winner(game))
                # text = ""
                # text_list: list[str] = [
                #     f"\u200Fامتیاز \u200F{player.name}: \u200F{player.score}" + "\n"
                #     for player in game.finished_player
                # ]
                # for t in text_list:
                #     text += f"{t}"

                # if is_tie:
                #     result = f"😎بازی مساوی شد😎" + "\n\nامتیازات:\n" + text + "\n\nپولتون رو خوردم🙂‍↔️"
                
                # elif not is_tie and len(winners) == 1:
                #     result = f"\u200F{winners[0]} برنده شد💙" + "\n\nامتیازات:\n" + text + f"\nمبلغ {reward}دلار به برنده واریز شد"
                # elif not is_tie and len(winners) > 1:
                #     names = ""
                #     winner_names: list[str] = [f"\u200F{player.name} " for player in winners]
                #     for i, t in enumerate(winner_names, 1):
                #         if i == len(winner_names):
                #             names += f"{t}"
                #         else:
                #             names += f"{t}" + "و"

                #     result = names + "برنده شدند💙" +"\n\nامتیازات:\n" + text + f"\nمبلغ {reward}دلار به برنده واریز شد"
                # else:
                #     result = "مشکلی پیش آمد، نمیتوانم دقیق مشخص کنم چه کسی برنده شد و چه مقدار پول دریافت کرد"

                await context.bot.edit_message_text(
                    chat_id=game.main_chat_id,
                    message_id=game.main_message_id,
                    text=text,
                )

                print("Finishing game")

                # context.application.bot_data.pop(game.creator_id)
                # del game
                       

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
                                            # InlineKeyboardButton(
                                            #     text="1",
                                            #     callback_data="one_player_game",
                                            # ),
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

            return abs(number)

        except:
            print("converted to int fail :(")
            return None
    else:
        print("Not Match :(")
        return None


async def add_player_or_run_game(
    user_id: int, user_name: str, game: Game, context: ContextTypes.DEFAULT_TYPE
) -> None:
    # print("in add_player function")
    if len(game.players_data) < game.player_count:
        # players_id = []
        # for player in game.players_data:
        #     players_id.append(player.id)

        if user_id not in game.get_players_id():
            user_dollar = get_dollar(user_id)
            if user_dollar and game.entry_fee <= user_dollar:
                if update_dollar(user_id, -game.entry_fee):
                    # player = Player(id=user_id, name=user_name, score=0, is_paid=False)
                    game.players_data.append(
                        Player(id=user_id, name=user_name, score=0, is_paid=True, is_winner=False)
                    )
                    game.status = Game.STATUS[4]
                    # print(
                    #     f"this user: {user_name} added to game\n creator id: {game.creator_name}"
                    # )

                    context.user_data["game"] = game # type: ignore
                    # print(f"user: {user_id} | context: {context.user_data}")

                    text = generate_text_for_join_user(game)
                    await context.bot.edit_message_text(
                        chat_id=game.main_chat_id,
                        message_id=game.main_message_id,
                        text=text,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="🙋‍♂️شرکت میکنم🙋‍♂️",
                                        callback_data=f"{game.creator_id}_join_game",
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

                else:
                    pass
                    # print("update dollar Faild :(")

            else:
                await context.bot.send_message(
                    chat_id=game.main_chat_id,
                    text=f"دلار شما کافی نیست\n\u200F{user_name} عزیز",
                )
                # print("Not enough dollar :(")

        else:
            await context.bot.send_message(
                chat_id=game.main_chat_id,
                text=f"{user_name} عزیز\nشما در بازی هستید لازم نیست روی شرکت کردن بزنید",
            )
            # print("this user is in game\n duplication error")

    if len(game.players_data) == game.player_count:
        game.status = Game.STATUS[5]
        # text_template = ""
        # result = ""

        # text_list: list[str] = [
        #     f"بازیکن{x+1}: " + "{" + f"player_{x+1}" + "}" + "\n"
        #     for x in range(game.player_count)
        # ]

        # for text in text_list:
        #     text_template += f"{text}"

        # result = text_template
        # # print(game.players_data)
        # for i, player in enumerate(game.players_data):
        #     # print("index is: " + f"{i}")
        #     result = result.replace("{player_" + f"{i+1}" + "}", player.name, 1)

        # result += "برای شروع بازی روی شروع بزنید"

        # find_text_list = re.findall(r"\{player_\d\}", result)
        # if find_text_list:
        #     result = "برای شروع بازی روی شروع بزنید"

        text = generate_text_for_run_game(game)
        await context.bot.edit_message_text(
            chat_id=game.main_chat_id,
            message_id=game.main_message_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔥شروع🔥",
                            callback_data=f"run_game",
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


def generate_text_for_run_game(game: Game) -> str:
    """in tabe yek object az noe Game migirad
    barhasb tedad player taiin shode dar game
    matn mored nazar ra misazad va barmigardanad
    
    Args:
        game (Game): yek object az noe Game
    
    Returns:
        str: matne sakhte shode motanaseb ba tedad bazikon
    """
    text_template = ""
    result = ""

    text_list: list[str] = [
        f"بازیکن{x+1}: " + "{" + f"player_{x+1}" + "}" + "\n"
        for x in range(game.player_count)
    ]

    for text in text_list:
        text_template += f"{text}"

    result = text_template
    # print(game.players_data)
    for i, player in enumerate(game.players_data):
        # print("index is: " + f"{i}")
        result = result.replace("{player_" + f"{i+1}" + "}", player.name, 1)

    result += f"\n\nبرای شروع بازی روی شروع بزن\n\u200F{game.creator_name} جان"

    find_text_list = re.findall(r"\{player_\d\}", result)
    if find_text_list:
        result = f"برای شروع بازی روی شروع بزن {game.creator_name} جان"

    return result


def generate_text_for_join_user(game: Game) -> str:
    """in tabe yek object az noe Game migirad
    barhasb tedad player taiin shode dar game
    matn mored nazar ra misazad va barmigardanad

    Args:
        game (Game): yek object az noe Game

    Returns:
        str: matne sakhte shode motanaseb ba tedad bazikon
    """
    # "{"+ f"player_{x+1}" + "}"
    text_list: list[str] = [
        f"کاربر{x+1}: " + "{" + f"player_{x+1}" + "}" + "\n"
        for x in range(game.player_count)
    ]

    text_template = "لطفا برای این که وارد بازی شوید\nروی شرکت کردن بزنید\n\n"

    result: str = ""

    for text in text_list:
        text_template += f"{text}"

    result = text_template
    # print(game.players_data)
    for i, player in enumerate(game.players_data):
        # print("index is: " + f"{i}")
        result = result.replace("{player_" + f"{i+1}" + "}", player.name, 1)
        # print("\n***\n"+ result + "\n***\n")

    # print(r"\{player_\d\}")
    find_text_list = re.findall(r"\{player_\d\}", result)
    if find_text_list:
        # print(find_text_list)
        for item in find_text_list:
            result = result.replace(item, " ")

    if result == "":
        result = "لطفا برای این که وارد بازی شوید\nروی شرکت کردن بزنید\n\nمتاسفانه در گرفتن نام شرکت کنندگان مشکلی پیش آمد"

    # print(result)
    return result


def generate_text_for_show_winners(game: Game, is_tie: bool, reward: int, winners: list[Player]) -> str:
    text = ""
    text_list: list[str] = [
        f"\u200Fامتیاز \u200F{player.name}: \u200F{player.score}" + "\n"
        for player in game.finished_player
    ]
    for t in text_list:
        text += f"{t}"

    if is_tie:
        result = f"😎بازی مساوی شد😎" + "\n\nامتیازات:\n" + text + "\n\nپولتون رو خوردم🙂‍↔️"
    
    elif not is_tie and len(winners) == 1:
        result = f"\u200F{winners[0].name} برنده شد💙" + "\n\nامتیازات:\n" + text + f"\nمبلغ {reward}دلار به برنده واریز شد"
    elif not is_tie and len(winners) > 1:
        names = ""
        winner_names: list[str] = [f"\u200F{player.name} " for player in winners]
        for i, t in enumerate(winner_names, 1):
            if i == len(winner_names):
                names += f"{t}"
            else:
                names += f"{t}" + "و"

        result = names + "برنده شدند💙" +"\n\nامتیازات:\n" + text + f"\nمبلغ {reward}دلار به برنده واریز شد"
    else:
        result = "مشکلی پیش آمد، نمیتوانم دقیق مشخص کنم چه کسی برنده شد و چه مقدار پول دریافت کرد"

    return result


def calculate_winner(game: Game) -> tuple[bool, int, list[Player]]:
    is_tie = False
    reward: int = int(game.entry_fee * game.player_count)
    # ===============================
    scores = []

    for player in game.finished_player:
        scores.append(player.score)

    print("scores is:", scores)
    high_score = max(scores)
    print("high score is:", high_score)

    winners: list[Player] = []
    for player in game.finished_player:
        if player.score == high_score:
            player.is_winner = True
            winners.append(player)

    if len(winners) == game.player_count:
        is_tie = True
        reward = 0
    elif len(winners) < game.player_count:
        is_tie = False
        reward = int(reward / len(winners))
    else:
        print("Error calculate winner!")
        reward = 0

    for player in winners:
        update_dollar(player.id, reward)

    return is_tie, reward, winners

    

