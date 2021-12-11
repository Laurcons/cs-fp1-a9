import os
from typing import Callable, TypeVar
import pickle
from src.repository.filesystem_repository import FilesystemRepository

class PickleRepository(FilesystemRepository):
    """ Extends the FilesystemRepository abstract class and adds save/load functionality for Pickle. """
    def __init__(self, filepath: str, id_getter: Callable[[any], any]):
        super().__init__(id_getter)
        self.__filepath = filepath

    def _load(self):
        if not os.path.isfile(self.__filepath):
            self._collection = {}
            return
        with open(self.__filepath, "rb") as file:
            pickle.load(file)

    def _save(self):
        with open(self.__filepath, "wb") as file:
            pickle.dump(self._collection, file)
