import datetime

from src.domain.assignment import Assignment
from src.repository.repository import Repository
from src.services.history_manager import HistoryManager


class AssignmentOperationError(BaseException):
    pass

class AssignmentService:
    """ Handles operations on the Assignments repository. """
    def __init__(self, history_manager: HistoryManager, assignment_repository: Repository):
        self.__assignment_repository = assignment_repository
        self.__history = history_manager

    def populate(self):
        """ Adds a couple of entries. """
        self.__assignment_repository.insert_all([
            Assignment(1, "Assignment 1", datetime.datetime.now() + datetime.timedelta(days=-10)),
            Assignment(2, "Assignment 2", datetime.datetime.now() + datetime.timedelta(days=20)),
            Assignment(3, "Assignment 3", datetime.datetime.now() + datetime.timedelta(days=30)),
            Assignment(4, "Assignment 4", datetime.datetime.now() + datetime.timedelta(days=40)),
            Assignment(5, "Assignment 5", datetime.datetime.now() + datetime.timedelta(days=50)),
            Assignment(6, "Assignment 6", datetime.datetime.now() + datetime.timedelta(days=60)),
            Assignment(7, "Assignment 7", datetime.datetime.now() + datetime.timedelta(days=70)),
            Assignment(8, "Assignment 8", datetime.datetime.now() + datetime.timedelta(days=80)),
            Assignment(9, "Assignment 9", datetime.datetime.now() + datetime.timedelta(days=90)),
            Assignment(10, "Assignment 10", datetime.datetime.now() + datetime.timedelta(days=100)),
            Assignment(11, "Assignment 11", datetime.datetime.now() + datetime.timedelta(days=110)),
            Assignment(12, "Assignment 12", datetime.datetime.now() + datetime.timedelta(days=120)),
            Assignment(13, "Assignment 13", datetime.datetime.now() + datetime.timedelta(days=130)),
            Assignment(14, "Assignment 14", datetime.datetime.now() + datetime.timedelta(days=140)),
            Assignment(15, "Assignment 15", datetime.datetime.now() + datetime.timedelta(days=150)),
            Assignment(16, "Assignment 16", datetime.datetime.now() + datetime.timedelta(days=160)),
            Assignment(17, "Assignment 17", datetime.datetime.now() + datetime.timedelta(days=170)),
            Assignment(18, "Assignment 18", datetime.datetime.now() + datetime.timedelta(days=180)),
            Assignment(19, "Assignment 19", datetime.datetime.now() + datetime.timedelta(days=190)),
            Assignment(20, "Assignment 20", datetime.datetime.now() + datetime.timedelta(days=200)),
        ])

    def add_assignment(self, assignment_id, description, deadline):
        """ Adds an assignment. """
        if self.__assignment_repository.id_exists(assignment_id):
            raise AssignmentOperationError("Assignment id already exists")
        assignment = Assignment(assignment_id, description, deadline)
        self.__assignment_repository.add(assignment)
        # add undo op
        self.__history.add_operation(
            self.__assignment_repository.remove_id, [assignment_id],
            self.__assignment_repository.add, [assignment]
        )

    def update_assignment(self, assignment_id, description, deadline):
        """ Updates an assignment, using the assignment id as a primary key. """
        assignment = self.__assignment_repository.find_id(assignment_id)
        original = Assignment(assignment.assignment_id, assignment.description, assignment.deadline)
        assignment.description = description
        assignment.deadline = deadline
        self.__assignment_repository.update(assignment)
        # add undo op
        self.__history.add_operation(
            self.__assignment_repository.update, [original],
            self.__assignment_repository.update, [assignment]
        )

    def get_all_assignments(self):
        """ List all assignments. """
        return self.__assignment_repository.get_all()
