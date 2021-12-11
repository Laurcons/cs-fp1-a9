from datetime import datetime

from src.domain.assignment import Assignment
from src.repository.mongo_repository import MongoRepository


class AssignmentMongoRepository(MongoRepository):
    def __init__(self, connection_string):
        super().__init__(connection_string, "assignments", lambda s: s.assignment_id)

    def add(self, entity: Assignment):
        self._mongo.insert_one(self.__to_dict(entity))

    def add_all(self, entities: list[Assignment]):
        self._mongo.insert_many([
            self.__to_dict(entity)
            for entity in entities])

    def remove_id(self, id: int):
        self._mongo.delete_one({ 'assignment_id': id })

    def update(self, entity: Assignment):
        self._mongo.update_one(
            { 'assignment_id': entity.assignment_id },
            { '$set': self.__to_dict(entity) }
        )

    def count(self):
        return self._mongo.count_documents({})

    def find_id(self, id: int):
        return self.__from_dict(
            self._mongo.find_one({ 'assignment_id': id })
        )

    def get_all(self):
        return [
            self.__from_dict(result)
            for result in self._mongo.find()
        ]

    def id_exists(self, id: int):
        return self.find_id(id) is not None

    def __from_dict(self, d: dict):
        if d is None:
            return None
        return Assignment(
            d['assignment_id'],
            d['description'],
            datetime.fromtimestamp(d['deadline'])
        )

    def __to_dict(self, entity: Assignment):
        if entity is None:
            return None
        return {
            'assignment_id': entity.assignment_id,
            'description': entity.description,
            'deadline': entity.deadline.timestamp()
        }
