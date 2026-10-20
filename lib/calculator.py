from data.database import Database
from datetime import datetime




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
