from typing import Callable
from src.domain.student import Student
from src.repository.text_repository import TextRepository


class StudentTextRepository(TextRepository):
    def __init__(self, filepath: str):
        super().__init__(filepath,
                         self.__serialize,
                         self.__deserialize,
                         lambda s: s.student_id)

    def __serialize(self, entity: Student) -> list[str]:
        return [
            str(entity.student_id),
            str(entity.name),
            str(entity.group)
        ]

    def __deserialize(self, args: list[str]) -> Student:
        return Student(
            int(args[0]),
            args[1],
            args[2]
        )
