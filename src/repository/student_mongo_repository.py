from src.domain.student import Student
from src.repository.mongo_repository import MongoRepository


class StudentMongoRepository(MongoRepository):
    def __init__(self, connection_string):
        super().__init__(connection_string, "students", lambda s: s.student_id)

    def add(self, entity: Student):
        self._mongo.insert_one({
            'student_id': entity.student_id,
            'name': entity.name,
            'group': entity.group
        })

    def add_all(self, entities: list[Student]):
        self._mongo.insert_many([{
            'student_id': entity.student_id,
            'name': entity.name,
            'group': entity.group
        } for entity in entities])

    def remove_id(self, id: int):
        self._mongo.delete_one({ 'student_id': id })

    def update(self, entity: Student):
        self._mongo.update_one(
            { 'student_id': entity.student_id },
            { 'name': entity.name, 'group': entity.group }
        )

    def count(self):
        return self._mongo.count_documents({})

    def find_id(self, id: int):
        return self.__from_dict(
            self._mongo.find_one({ 'student_id': id })
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
        return Student(
            d['student_id'],
            d['name'],
            d['group']
        )
