from src.domain.student import Student


class StudentSituationDTO:
    def __init__(self, student: Student, average: float):
        self.__student = student
        self.__average = average

    @property
    def student(self):
        return self.__student

    @property
    def average(self):
        return self.__average
