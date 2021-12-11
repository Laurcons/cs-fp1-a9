from typing import Callable
import pymongo
from src.repository.repository import Repository

class MongoRepository(Repository):
    def __init__(self,
                 connection_string: str,
                 collection_name: str,
                 id_getter: Callable):
        super().__init__(id_getter)
        # connect to mongo
        client = pymongo.MongoClient(connection_string)
        self._collection_name = collection_name
        self._mongo = client["myFirstDatabase"][collection_name]
