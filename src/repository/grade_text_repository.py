from typing import Callable
from src.domain.grade import Grade
from src.repository.text_repository import TextRepository


class GradeTextRepository(TextRepository):
    def __init__(self, filepath: str):
        super().__init__(filepath,
                         self.__serialize,
                         self.__deserialize,
                         lambda g: (g.assignment_id, g.student_id))

    def __serialize(self, entity: Grade) -> list[str]:
        return [
            str(entity.assignment_id),
            str(entity.student_id),
            str(entity.grade_value)
        ]

    def __deserialize(self, args: list[str]) -> Grade:
        return Grade(
            int(args[0]),
            int(args[1]),
            int(args[2])
        )
