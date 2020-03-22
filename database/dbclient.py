import pymongo

class DbClient:
    """Creates an instance of pymongo client and stores it in a private variable.

    The instance of this class is injected as a dependency for request validators and processors.

    Attributes:
        database (Database): The database object.
        collection_list (list): List of collection names as str.
    """
    database = None
    collection_list = None

    def __init__(self, mongo_uri, database):
        """
        Args:
            mongo_uri (str): Uri of the MongoDB database.
            database (str): Name of the database.
        """
        client = pymongo.MongoClient(mongo_uri)
        self.database = client[database]
        self.collection_list = [collection for collection in self.database.collection_names()]
    
    def get_collection(self, collection):
        """
        Args:
            collection (str): Name of the collection to get.
        Returns:
            Collection: The collection by name.
        """
        assert collection in self.collection_list
        return self.database[collection]