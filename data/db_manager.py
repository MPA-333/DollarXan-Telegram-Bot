from pymongo.errors import PyMongoError      


class MongoDBManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection


    def insert(self, collection_name, document):
        try:
            collection = self.db_connection.database[collection_name]
            result = collection.insert_one(document)
            print(f"Document inserted with id: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Error while inserting document: {e}")
            return None


    def find(self, collection_name, query=None, projection=None):
        try:
            collection = self.db_connection.database[collection_name]
            if query is None:
                query = {}
            documents = list(collection.find(query, projection))
            return documents
        except PyMongoError as e:
            print(f"Error while finding documents: {e}")
            return None


    def update(self, collection_name, query, update_data, upsert=False):
        try:
            # update_data = {"$set": {price: 500}}
            collection = self.db_connection.database[collection_name]
            result = collection.update_many(query, update_data, upsert=upsert)
            print(
                f"Matched {result.matched_count} documents and modified {result.modified_count} documents"
            )
            return result.modified_count
        except PyMongoError as e:
            print(f"Error while updating documents: {e}")
            return None


    def delete(self, collection_name, query):
        try:
            collection = self.db_connection.database[collection_name]
            result = collection.delete_many(query)
            print(f"Deleted {result.deleted_count} documents")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Error while deleting documents: {e}")
            return None


    def aggregate(self, collection_name, pipeline):
        try:
            collection = self.db_connection.database[collection_name]
            return list(collection.aggregate(pipeline))
        except PyMongoError as e:
            print(f"Error while aggregating documents: {e}")
            return None
