from pymongo import MongoClient
from pymongo.errors import PyMongoError


class MongoDBConnection:
    def __init__(self, host='localhost', port=27017, database_name=None, username=None, password=None):
        self.host = host
        self.port = port
        self.database_name = database_name
        self.username = username
        self.password = password
        self.client = None
        self.database = None

    def connect(self):
        try:
            if self.username and self.password:
                self.client = MongoClient(
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    authSource='admin'
                )
            else:
                self.client = MongoClient(host=self.host, port=self.port)
            
            self.client.admin.command('ping')
            print("Connected to MongoDB successfully!")

            if self.database_name:
                print(f"Database created with {self.database_name}")
                self.database = self.client[self.database_name]

        except PyMongoError as e:
            print(f"Error while connecting to MongoDB: {e}")

    def disconnect(self):
        if self.client:
            self.client.close()
            print("MongoDB connection is closed")
