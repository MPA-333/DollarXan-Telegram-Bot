from data.database import Database
from datetime import datetime, timedelta, timezone

# def time_is_ok(user_id: int) -> bool:
#     db.manager.find("user", {"user_id": user_id}, {"dollar": 1})[0]["dollar"] # pyright: ignore[reportOptionalSubscript]
#     return True


def add_dollar(user_id: int, fname: str|None, lname: str|None, date: datetime|None) -> int|None:
    db = Database()
    if db.manager is not None:
        if db.user_exist(user_id):
            # last_update_date: datetime = db.last_update_date(user_id)

            # waitinh_time: timedelta = timedelta(minutes=1) - (datetime.now(timezone.utc) - last_update_date)
            # print(f"wait: {waitinh_time}")

            # # print(f"last: {last_update_date}")
            # # print(f"now: {datetime.now(timezone.utc)}")
            # # print(f"tafazol: {datetime.now(timezone.utc) - last_update_date > timedelta(minutes=1)}")
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