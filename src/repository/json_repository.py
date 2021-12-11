import os
from datetime import datetime, date
from typing import Callable
import json
from src.repository.filesystem_repository import FilesystemRepository

class JsonRepository(FilesystemRepository):
    """ Extends the FilesystemRepository abstract class and adds save/load functionality for Pickle. """
    def __init__(self, filepath: str, id_getter: Callable[[any], any]):
        super().__init__(id_getter)
        self.__filepath = filepath

    def _load(self):
        if not os.path.isfile(self.__filepath):
            self._collection = {}
            return
        with open(self.__filepath, "r") as file:
            entities = json.load(file)
            self._collection = {
                self._id_get(ent) : ent
                for ent in entities
            }

    def _save(self):
        with open(self.__filepath, "w") as file:
            json.dump([ent.__dict__ for ent in self._collection.values()], file, default=self.__json_serial)

    def __json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))
