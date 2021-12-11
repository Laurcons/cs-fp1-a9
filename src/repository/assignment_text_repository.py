from datetime import datetime
from typing import Callable
from src.domain.assignment import Assignment
from src.repository.text_repository import TextRepository


class AssignmentTextRepository(TextRepository):
    def __init__(self, filepath: str):
        super().__init__(filepath,
                         self.__serialize,
                         self.__deserialize,
                         lambda a: a.assignment_id)

    def __serialize(self, entity: Assignment) -> list[str]:
        return [
            str(entity.assignment_id),
            str(entity.description),
            str(entity.deadline.timestamp())
        ]

    def __deserialize(self, args: list[str]) -> Assignment:
        return Assignment(
            int(args[0]),
            args[1],
            datetime.fromtimestamp(float(args[2]))
        )
