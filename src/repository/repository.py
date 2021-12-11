from typing import Callable, Generic, TypeVar


class RepositoryError(BaseException):
    pass

Entity = TypeVar("Entity")
Id = TypeVar("Id")
class Repository(Generic[Entity]):
    """ Handles operations on a collection of items. """
    def __init__(self, id_getter: Callable[[Entity], Id]):
        self._collection = {}
        self._id_get = id_getter

    def add_all(self, entities: list[Entity]):
        """ Inserts all the elements. If any one of the elements results in an id collision,
            the collection is not modified and an RepositoryError is raised.
        """
        for ent in entities:
            if self._id_get(ent) in self._collection:
                raise RepositoryError("One of the bulk-added entities resulted in an id collision")
        for ent in entities:
            self.add(ent)

    def add(self, entity: Entity):
        """ Inserts a new element, or throws RepositoryError if it exists. """
        if self._id_get(entity) in self._collection:
            raise RepositoryError("Id already exists")
        self._collection[self._id_get(entity)] = entity

    def update(self, entity: Entity):
        """ Updates an element, using the Id as a primary key. Raises RepositoryError if it doesn't exist. """
        if self._id_get(entity) not in self._collection:
            raise RepositoryError("Id doesn't exist")
        self._collection[self._id_get(entity)] = entity

    def id_exists(self, id: Id):
        """ Returns True if an entity with the given id exists. """
        return id in self._collection

    def find_id(self, id: Id):
        """ Finds and returns the element with the given id, or None. """
        if self.id_exists(id):
            return self._collection[id]
        raise RepositoryError("Element not found")

    # def find_all_by_predicate(self, predicate):
    #     """ Finds and returns all elements that satisfy the given predicate, in a list. """
    #     return [x for x in self.__collection.values() if predicate(x)]

    def remove_id(self, id: Id):
        """ Removes the given id and returns it. """
        if self.id_exists(id):
            return self._collection.pop(id)
        raise RepositoryError("Id doesn't exist")

    def get_all(self):
        """ Returns all the values of the repo, in a list. """
        return list(self._collection.values())

    def count(self):
        return len(self._collection)
