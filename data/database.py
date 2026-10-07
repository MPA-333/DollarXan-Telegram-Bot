from data.db_connection import MongoDBConnection
from data.db_manager import MongoDBManager


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

    def close(self):
        self.connection.disconnect()

    def user_exist(self, id) -> bool:
        assert self.manager is not None
        if self.manager.find("user", {"user_id": id}):
            return True
        else:
            return False
