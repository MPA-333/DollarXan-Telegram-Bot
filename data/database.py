from data.db_connection import MongoDBConnection
from data.db_manager import MongoDBManager
from datetime import datetime, timezone, timedelta
# =======================================================================


class Database:
    is_connected = False
    manager = None
    def __init__(self) -> None:
        if not Database.is_connected:
            self.connection = MongoDBConnection(
                host="localhost",
                port=27017,
                database_name="dollarxanbot",
            )
            self.connection.connect()
            Database.manager = MongoDBManager(self.connection)
            Database.is_connected = True
            self.manager = Database.manager
        else:
            self.manager = Database.manager

    def user_exist(self, id: int) -> bool:
        """in tabe id user ra migirad agar dakhel paygahdade bud True
        barmigardanad dar gheyr in surat False

        Args:
            id (int): id user mored nazar

        Returns:
            bool: agar True bargardanad yani karbar mojud ast.
        """
        assert self.manager is not None
        if self.manager.find("user", {"user_id": id}):
            return True
        else:
            return False


    def time_isverify(self, id: int, limit: int) -> tuple[bool, int]:
        """in tabe tarikh akharin payam ezafe shodan dollar braye karbar ra az paygah dade mikhanad.
        ba limit dade shode mogayese mikonad. agar zaman entezar tamam shode bud True va zaman entezar lazem ra
        barmigardanad ke ye adad manfi khahad bud.

        Args:
            id (int): id user mored nazar
            limit (int): moddat zaman mored entezar braye gozasht az akharin update (second)

        Returns:
            tuple[bool, int]: yek tuple ke ozv avval agar True bashad yani karbar zaman entezar ra pass karde.
            ozv dovvom second lazem braye entezar ast ke vagti ozv avval False bashad mani dar khahad bud.
        """
        assert self.manager is not None

        date: datetime = self.manager.find("user", {"user_id": id}, {"last_dollar_gen_date": 1})[0]["last_dollar_gen_date"] # type: ignore
        date = date.replace(tzinfo=timezone.utc)

        waitinh_time: timedelta = timedelta(seconds=limit) - (datetime.now(timezone.utc) - date)

        return (datetime.now(timezone.utc) - date > timedelta(seconds=limit), waitinh_time.seconds)
        

    def close(self):
        self.connection.disconnect()
