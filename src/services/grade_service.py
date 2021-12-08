from src.domain.assignment import Assignment
from src.domain.grade import Grade
from src.domain.student import Student
from src.domain.student_assignment_grade_dto import StudentAssignmentGradeDTO
from src.domain.student_situation_dto import StudentSituationDTO
from src.repository.repository import Repository
from src.services.history_manager import HistoryManager


class GradeOperationError(BaseException):
    pass

class GradeService:
    """ Handles operations on the Grades repository. """
    def __init__(self, history_manager: HistoryManager, grade_repository: Repository, assignment_repository: Repository, student_repository: Repository):
        self.__grade_repository = grade_repository
        self.__student_repository = student_repository
        self.__assignment_repository = assignment_repository
        self.__history = history_manager

    def remove_assignment_and_grades(self, assignment_id, undoable=True):
        """ Removes an assignment given its id. Returns the removed assignment. """
        grades = self.__grade_repository.get_all()
        grades = [g for g in grades if g.assignment_id == assignment_id]
        for id_pair in [(g.assignment_id, g.student_id) for g in grades]:
            self.__grade_repository.remove_id(id_pair)
        removed_asn = self.__assignment_repository.remove_id(assignment_id)
        if undoable:
            self.__history.add_operation(
                self.__add_assignment_and_grades, [removed_asn, grades],
                self.remove_student_and_grades, [assignment_id, False]
            )
        return removed_asn

    def __add_assignment_and_grades(self, assignment: Assignment, grades: list[Grade]):
        """ Adds an assignment and some grades. Mainly used for history operations. NOT UNDOABLE. """
        for grade in grades:
            self.__grade_repository.add(grade)
        self.__assignment_repository.add(assignment)

    def remove_student_and_grades(self, student_id, undoable=True):
        """ Removes the student, given their id. Returns the removed student. """
        grades = self.__grade_repository.get_all()
        grades = [g for g in grades if g.student_id == student_id]
        for id_pair in [(g.assignment_id, g.student_id) for g in grades]:
            self.__grade_repository.remove_id(id_pair)
        removed_student = self.__student_repository.remove_id(student_id)
        if undoable:
            self.__history.add_operation(
                self.__add_student_and_grades, [removed_student, grades],
                self.remove_student_and_grades, [student_id, False]
            )

    def __add_student_and_grades(self, student: Student, grades: list[Grade]):
        """ Adds a student and some grades. NOT UNDOABLE. """
        for grade in grades:
            self.__grade_repository.add(grade)
        self.__student_repository.add(student)

    def assign_to_student(self, assignment_id, student_id, undoable=True):
        """ Assigns an assignment to a student. """
        if not self.__assignment_repository.id_exists(assignment_id):
            raise GradeOperationError("Assignment id doesn't exist")
        if not self.__student_repository.id_exists(student_id):
            raise GradeOperationError("Student id doesn't exist")
        grade = Grade(assignment_id, student_id, 0)
        self.__grade_repository.add(grade)
        if undoable:
            self.__history.add_operation(
                self.__unassign_from_student, [assignment_id, student_id],
                self.assign_to_student, [assignment_id, student_id, False]
            )

    def __unassign_from_student(self, assignment_id, student_id):
        """ Unassigns an assignment from a student. NOT UNDOABLE. """
        self.__grade_repository.remove_id((assignment_id, student_id))

    def assign_to_group(self, assignment_id, group, undoable=True):
        """ Assigns an assignment to a group of students. """
        students = self.__student_repository.get_all()
        students = [s for s in students if s.group == group]
        for stud in students:
            self.assign_to_student(assignment_id, stud.student_id)
        if undoable:
            self.__history.add_operation(
                self.__unassign_from_group, [assignment_id, group],
                self.assign_to_group, [assignment_id, group, False]
            )

    def __unassign_from_group(self, assignment_id, group):
        """ Unassigns an assignment from a group of students. NOT UNDOABLE. """
        students = self.__student_repository.get_all()
        students = [s for s in students if s.group == group]
        for stud in students:
            self.__unassign_from_student(assignment_id, stud.student_id)

    def get_all_assignations(self):
        """ Returns a list of all the assignations. """
        return self.__grade_repository.get_all()

    def apply_grade_to_student(self, assignment_id, student_id, grade_value, undoable=True):
        """ Applies a grade to a student. If already applied, raises GradeOperationError. """
        if not self.__assignment_repository.id_exists(assignment_id):
            raise GradeOperationError("Assignment id doesn't exist")
        if not self.__student_repository.id_exists(student_id):
            raise GradeOperationError("Student id doesn't exist")
        grade = self.__grade_repository.find_id((assignment_id, student_id))
        if grade.grade_value != 0:
            raise GradeOperationError("Assignment already graded")
        grade.grade_value = grade_value
        self.__grade_repository.update(grade)
        if undoable:
            self.__history.add_operation(
                self.__remove_grade_from_student, [assignment_id, student_id],
                self.apply_grade_to_student, [assignment_id, student_id, False]
            )

    def __remove_grade_from_student(self, assignment_id, student_id):
        """ Removes a grade from a student. NOT UNDOABLE. """
        grade = self.__grade_repository.find_id((assignment_id, student_id))
        grade.grade_value = 0
        self.__grade_repository.update(grade)

    def get_ungraded_assignments_of_student(self, student_id) -> list[Assignment]:
        """ Returns the ungraded assignments of a student. """
        grades = self.__grade_repository.get_all()
        grades = [g for g in grades if g.student_id == student_id and not g.is_graded]
        ungraded_ids = [g.assignment_id for g in grades]
        asns = self.__grade_repository.get_all()
        asns = [a for a in asns if a.assignment_id in ungraded_ids]
        return asns

    def get_graded_students_for_assignment(self, assignment_id) -> list[StudentAssignmentGradeDTO]:
        """ Gets a list of students, their graded assignments, and the grade for each assignment. """
        grades = self.__grade_repository.get_all()
        grades = [g for g in grades if g.assignment_id == assignment_id and g.is_graded]
        asn = self.__assignment_repository.find_id(assignment_id)
        out = []
        for grade in grades:
            student = self.__student_repository.find_id(grade.student_id)
            out.append(StudentAssignmentGradeDTO(student, asn, grade))
        out.sort(key=lambda dto: dto.grade.grade_value)
        return out

    def get_students_with_late_assignments(self) -> list[StudentAssignmentGradeDTO]:
        """ Gets a list of students, and their late assignments. """
        asns = self.__assignment_repository.get_all()
        overdue_asns = filter(lambda a: a.is_overdue, asns)
        out = []
        for asn in overdue_asns:
            grades = self.__grade_repository.get_all()
            grades = [g for g in grades if g.assignment_id == asn.assignment_id and not g.is_graded]
            for grade in grades:
                student = self.__student_repository.find_id(grade.student_id)
                out.append(StudentAssignmentGradeDTO(student, asn, grade))
        return out

    def get_students_with_best_situation(self) -> list[StudentSituationDTO]:
        """ Gets a list of students, along with their average. """
        out = []
        grades = self.__grade_repository.get_all()
        grade_situation = {}
        for grade in grades:
            student_id = grade.student_id
            if student_id not in grade_situation:
                grade_situation[student_id] = []
            grade_situation[student_id].append(grade.grade_value)
        for student_id in grade_situation:
            student = self.__student_repository.find_id(student_id)
            student_average = sum(grade_situation[student_id]) / len(grade_situation[student_id])
            out.append(StudentSituationDTO(student, student_average))
        out.sort(key=lambda dto: dto.average)
        return out
