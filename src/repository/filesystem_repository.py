from abc import abstractmethod, ABC

from src.repository.repository import Repository


class FilesystemRepository(Repository, ABC):
    """ Extends the Repository class with abstract methods to support generic filesystem saving-loading features. """

    @abstractmethod
    def _save(self):
        pass

    @abstractmethod
    def _load(self):
        pass

    def __init__(self, id_getter):
        super().__init__(id_getter)

    def add(self, entity):
        super().add(entity)
        self._save()

    def add_all(self, entities):
        super().add_all(entities)
        self._save()

    def remove_id(self, id):
        super().remove_id(id)
        self._save()

    def update(self, entity):
        super().update(entity)
        self._save()
