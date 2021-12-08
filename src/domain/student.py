import re

from src.domain.validator import Validator, ValidationError


class Student:
    def __init__(self, student_id: int, name: str, group: str):
        self.__student_id = student_id
        self.__name = name
        self.__group = group
        StudentValidator.validate(self)

    @property
    def student_id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, value):
        self.__group = value

    @property
    def specialization(self):
        return {
            1: "M",
            2: "I",
            3: "MI",
            4: "MM",
            5: "IM",
            6: "MIM",
            7: "IG",
            8: "MIE",
            9: "IE"
        }[int(self.__group[0])]

    @property
    def year(self):
        return self.__group[1]

    def __str__(self):
        return f"#{self.student_id}: {self.name} in {self.group} at {self.specialization} year {self.year}"

class StudentValidationError(ValidationError):
    pass

class StudentValidator(Validator):
    @staticmethod
    def validate(student: Student):
        # verify the group code
        regex = re.compile("[1-9][1-3][1-9]")
        match = regex.match(student.group)
        if not match:
            raise StudentValidationError("Group is invalid")
