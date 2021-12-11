
import unittest

from src.repository.history_repository import HistoryRepository
from src.repository.repository import RepositoryError
from src.services.assignment_service import AssignmentService
from src.services.grade_service import GradeService
from src.services.student_service import *
from datetime import datetime, timedelta

class TestStudentService(unittest.TestCase):
    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.__std_repo = Repository(lambda x: x.student_id)
        self.__grd_repo = Repository(lambda x: (x.assignment_id, x.student_id))
        self.__asn_repo = Repository(lambda x: x.assignment_id)
        self.__history_manager = HistoryManager(HistoryRepository(), HistoryRepository())
        self.__std_service = StudentService(self.__history_manager, self.__std_repo)
        self.__asn_service = AssignmentService(self.__history_manager, self.__asn_repo)
        self.__grd_service = GradeService(self.__history_manager, self.__grd_repo, self.__asn_repo, self.__std_repo)
        self.__std_service.populate()
        self.__asn_service.populate()

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)

    def test_add(self):
        self.__std_service.add_student(24, "bubu", "916")
        self.assertEqual(len(self.__std_repo.get_all()), 21)
        elem = self.__std_repo.find_id(24)
        self.assertEqual(elem.student_id, 24)
        self.assertEqual(elem.name, "bubu")
        self.assertEqual(elem.group, "916")

    def test_populate(self):
        self.assertEqual(len(self.__std_repo.get_all()), 20)

    def test_update(self):
        self.__std_service.add_student(21, "bubu", "916")
        self.__std_service.update_student(21, "no", "911")
        asn = self.__std_repo.find_id(21)

        self.assertEqual(asn.name, "no")
        self.assertEqual(asn.group, "911")

    def test_get_all(self):
        self.assertListEqual(self.__std_service.get_all_students(), self.__std_repo.get_all())
        self.assertEqual(len(self.__std_service.get_all_students_in_group("916")), 6)
