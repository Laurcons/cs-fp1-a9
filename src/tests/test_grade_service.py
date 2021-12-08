
import unittest

from src.repository.repository import RepositoryError
from src.services.assignment_service import AssignmentService
from src.services.grade_service import *
import datetime

from src.services.student_service import StudentService


class TestAssignmentService(unittest.TestCase):
    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.__asn_repo = Repository(lambda x: x.assignment_id)
        self.__std_repo = Repository(lambda x: x.student_id)
        self.__grd_repo = Repository(lambda x: (x.assignment_id, x.student_id))
        self.__grd_service = GradeService(self.__grd_repo, self.__asn_repo, self.__std_repo)
        self.__asn_service = AssignmentService(self.__asn_repo, self.__std_repo, self.__grd_repo)
        self.__std_service = StudentService(self.__std_repo, self.__asn_repo, self.__grd_repo)
        self.__asn_service.populate()
        self.__std_service.populate()

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)
        self.__repo = None
        self.__service = None

    def test_assign(self):
        self.__grd_service.assign_to_student(4, 1)
        grade = self.__grd_repo.find_id((4, 1))

        self.assertEqual(grade.student_id, 1)
        self.assertEqual(grade.assignment_id, 4)
        self.assertEqual(grade.grade_value, 0)
        self.assertFalse(grade.is_graded)

    def test_assign_group(self):
        self.__grd_service.assign_to_group(4, "916")
        self.assertEqual(len(self.__grd_repo.get_all()), 6)

    def test_apply_grade(self):
        self.__grd_service.assign_to_student(4, 5)
        self.__grd_service.assign_to_student(5, 5)
        self.__grd_service.apply_grade_to_student(4, 5, 10)
        grade = self.__grd_repo.find_id((4, 5))

        self.assertEqual(grade.grade_value, 10)

        with self.assertRaises(GradeOperationError):
            self.__grd_service.apply_grade_to_student(4, 5, 9)

