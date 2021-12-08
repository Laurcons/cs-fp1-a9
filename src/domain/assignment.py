import datetime

from src.domain.validator import Validator, ValidationError


class Assignment:
    """ Represents an assignment. """
    def __init__(self, assignment_id: int, description: str, deadline: datetime.datetime):
        """
        :param assignment_id: Integer.
        :param description: String.
        :param deadline: Date.
        """
        self.__assignment_id = assignment_id
        self.__description = description
        self.__deadline = deadline
        AssignmentValidator.validate(self)

    @property
    def assignment_id(self):
        return self.__assignment_id

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, value: datetime.datetime):
        self.__deadline = value

    @property
    def is_overdue(self):
        return datetime.datetime.now() > self.deadline

    def __str__(self):
        return f"#{self.assignment_id} until {self.deadline}: {self.description}"

class AssignmentValidationError(ValidationError):
    pass

class AssignmentValidator(Validator):
    """ Provides static methods to validate an assignment. """
    @staticmethod
    def validate(assignment):
        # nothing much to validate.
        pass
