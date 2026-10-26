from data.database import Database
from datetime import datetime
# =======================================================================


def add_dollar(user_id: int, fname: str|None, lname: str|None, date: datetime) -> int|None:
    """in tabe vrudi hara grefte va 3 dollar be user mored nazar ezafe mikonad.
    agar user gablan hesab nadashte bashad ye hesab jadid misazad.

    Args:
        user_id (int): id user mored nazar
        fname (str | None): name user ke optional ast
        lname (str | None): family user ke optional ast
        date (datetime | None): tarikh ersal payam

    Returns:
        int|None: agar amaliyat (sakht hesab ya ezafe kardan dollar) movafag bud 
        None barmigardanad. dar gheyr in surat zaman entezar (second) ta faal shodan add ra barmigardanad.
    """
    db = Database()
    if db.manager is not None:
        if db.user_exist(user_id):
            isverify, wait= db.time_isverify(user_id, 90)
            if isverify:
                db.manager.update("user", {"user_id": user_id}, {"$inc": {"dollar": 3}, "$set": {"last_dollar_gen_date": date}})
            else:
                return wait

        else:
            db.manager.insert("user", {
                "user_id": user_id,
                "first_name": fname,
                "last_name": lname,
                "dollar": 1,
                "last_dollar_gen_date": date,
            })


def get_dollar(user_id: int) -> int | None:
    """in tabe mojudi karbar ra midahad. agar karbar yaft nashod None midahad.

    Args:
        user_id (int): id user mored nazar.

    Returns:
        int | None: mojudi hesab user | user yaft nashod.
    """
    db = Database()
    if db.manager is not None:
        if db.user_exist(user_id):
            return db.manager.find("user", {"user_id": user_id}, {"dollar": 1})[0]["dollar"] # pyright: ignore[reportOptionalSubscript]
    return None


def update_dollar(user_id: int, value: int) -> bool:
    """in tabe ye megdar migirad va ba megdar dollar mojudi user jam mikonad.
    agar manfi begirad kam mikonad. agar mosbat begirad ezafe mikonad.
    dar akhar agar chizi ezafe ya kam shod True barmigardanad.

    Args:
        user_id (int): id user mored nazar
        value (int): adad mored nazar braye jam shodan ba dollar haye karbar

    Returns:
        bool: agar taghiri da paygahdade anjam shod True barmigardanad. 
    """
    db = Database()
    if db.manager is not None:
        if db.user_exist(user_id):
            result = db.manager.update("user", {"user_id": user_id}, {"$inc": {"dollar": value} })
            if result:
                print("your price is updated")
                return True
    return False




# def add_game(
#         game_type: str|None = None,
#         creator_id: int|None = None,
#         creator_name: str|None = None,
#         player_count: int|None = None,
#         players_data: list[Player]|None = None,
#         entry_fee: int|None = None,
#         main_chat_id: int|None = None,
#         main_message_id: int|None = None,
#         user_message_id: int|None = None,
#         status: str|None = None,
#         date: datetime|None = None
#         ):
    
#         # self.type = game_type
#         # self.player_count = player_count
#         # self.entry_fee = entry_fee
#         # self.main_chat_id = game_chat_id
#         # self.main_message_id = game_message_id
#         # self.user_message_id = user_message_id
#         # self.creator_id = creator_id
#         # self.creator_name = creator_name
#         # self.players_data: list[Player] = []
#         # self.status = Game.STATUS[0]
#     db = Database()
#     if db.manager is not None:
#         id = db.manager.insert("game", {
#             "type": game_type,
#             "creator_id": creator_id,
#             "creator_name": creator_name,
#             "player_count": player_count,
#             "players_data": players_data,
#             "entry_fee": entry_fee,
#             "main_chat_id": main_chat_id,
#             "main_message_id": main_message_id,
#             "user_message_id": user_message_id,
#             "status": status,
#             "create_date": date
#         })
