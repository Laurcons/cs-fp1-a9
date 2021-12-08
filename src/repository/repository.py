
class RepositoryError(BaseException):
    pass

class Repository:
    """ Handles operations on a collection of items. """
    def __init__(self, id_getter):
        self.__collection = {}
        self.__id_get = id_getter

    def insert_all(self, entities):
        """ Inserts all the elements. If any one of the elements results in an id collision,
            the collection is not modified and an RepositoryError is raised.
        """
        for ent in entities:
            if self.__id_get(ent) in self.__collection:
                raise RepositoryError("One of the bulk-added entities resulted in an id collision")
        for ent in entities:
            self.add(ent)

    def add(self, entity):
        """ Inserts a new element, or throws RepositoryError if it exists. """
        if self.__id_get(entity) in self.__collection:
            raise RepositoryError("Id already exists")
        self.__collection[self.__id_get(entity)] = entity

    def update(self, entity):
        """ Updates an element, using the Id as a primary key. Raises RepositoryError if it doesn't exist. """
        if self.__id_get(entity) not in self.__collection:
            raise RepositoryError("Id doesn't exist")
        self.__collection[self.__id_get(entity)] = entity

    def id_exists(self, id):
        """ Returns True if an entity with the given id exists. """
        return id in self.__collection

    def find_id(self, id):
        """ Finds and returns the element with the given id, or None. """
        if self.id_exists(id):
            return self.__collection[id]
        raise RepositoryError("Element not found")

    # def find_all_by_predicate(self, predicate):
    #     """ Finds and returns all elements that satisfy the given predicate, in a list. """
    #     return [x for x in self.__collection.values() if predicate(x)]

    def remove_id(self, id):
        """ Removes the given id and returns it. """
        if self.id_exists(id):
            return self.__collection.pop(id)
        raise RepositoryError("Id doesn't exist")

    def get_all(self):
        """ Returns all the values of the repo, in a list. """
        return list(self.__collection.values())
