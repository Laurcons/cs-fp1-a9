from datetime import datetime

from src.domain.grade import Grade
from src.repository.mongo_repository import MongoRepository


class GradeMongoRepository(MongoRepository):
    def __init__(self, connection_string):
        super().__init__(connection_string, "grades", lambda g: (g.assignment_id, g.student_id))

    def add(self, entity: Grade):
        self._mongo.insert_one(self.__to_dict(entity))

    def add_all(self, entities: list[Grade]):
        self._mongo.insert_many([
            self.__to_dict(entity)
            for entity in entities])

    def remove_id(self, id: (int, int)):
        self._mongo.delete_one({ 'student_id': id[1], 'assignment_id': id[0] })

    def update(self, entity: Grade):
        self._mongo.update_one(
            { 'student_id': entity.student_id, 'assignment_id': entity.assignment_id },
            { '$set': self.__to_dict(entity) }
        )

    def count(self):
        return self._mongo.count_documents({})

    def find_id(self, id: (int, int)):
        return self.__from_dict(
            self._mongo.find_one({ 'student_id': id[1], 'assignment_id': id[0] })
        )

    def get_all(self):
        return [
            self.__from_dict(result)
            for result in self._mongo.find()
        ]

    def id_exists(self, id: (int, int)):
        return self.find_id(id) is not None

    def __from_dict(self, d: dict):
        if d is None:
            return None
        return Grade(
            d['assignment_id'],
            d['student_id'],
            d['grade_value']
        )

    def __to_dict(self, entity: Grade):
        if entity is None:
            return None
        return {
            'assignment_id': entity.assignment_id,
            'student_id': entity.student_id,
            'grade_value': entity.grade_value
        }
