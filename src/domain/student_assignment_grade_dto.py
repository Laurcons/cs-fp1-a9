from src.domain.assignment import Assignment
from src.domain.grade import Grade
from src.domain.student import Student


class StudentAssignmentGradeDTO:
    def __init__(self, student: Student, assignment: Assignment, grade: Grade):
        self.__student = student
        self.__grade = grade
        self.__assignment = assignment

    @property
    def student(self):
        return self.__student

    @property
    def grade(self):
        return self.__grade

    @property
    def assignment(self):
        return self.__assignment

    def __eq__(self, other):
        return self.__assignment == other.__assignment and \
               self.__student == other.__student and \
               self.__grade == other.__grade

    def __repr__(self):
        return f"Student {self.__student} assignment {self.__assignment} grade {self.__grade}"
