from typing import Callable, Generic, TypeVar
import os.path
from src.repository.filesystem_repository import FilesystemRepository

class TextRepository(FilesystemRepository):
    """ Extends the FilesystemRepository abstract class and adds save/load functionality for CSV files. """
    def __init__(self,
                 filepath: str,
                 serializer: Callable[[any], list[str]],
                 deserializer: Callable[[list[str]], any],
                 id_getter: Callable[[any], any]):
        super().__init__(id_getter)
        self.__filepath = filepath
        self.__serializer = serializer
        self.__deserializer = deserializer
        self._load()

    def _load(self):
        if not os.path.isfile(self.__filepath):
            self._collection = {}
            return
        with open(self.__filepath, "r") as file:
            lines = file.readlines()
        entities = []
        for line in lines:
            parts = line.split('\0')
            entities.append(self.__deserializer(parts))
        self._collection = {
            self._id_get(ent) : ent
            for ent in entities
        }

    def _save(self):
        lines = []
        for ent in self._collection.values():
            lines.append("\0".join(self.__serializer(ent)))
        with open(self.__filepath, "w") as file:
            file.writelines("\n".join(lines))
