from data.database import Database
from datetime import datetime




def add_dollar(user_id: int, fname: str|None, lname: str|None, date: datetime|None) -> int|None:
    db = Database()
    if db.manager is not None:
        if db.user_exist(user_id):
            isverify, wait= db.time_isverify(user_id, 1)
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
    db = Database()
    if db.manager is not None:
        if db.user_exist(user_id):
            return db.manager.find("user", {"user_id": user_id}, {"dollar": 1})[0]["dollar"] # pyright: ignore[reportOptionalSubscript]
    return None
