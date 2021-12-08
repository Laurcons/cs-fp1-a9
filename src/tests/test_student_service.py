
import unittest

from src.repository.repository import RepositoryError
from src.services.assignment_service import AssignmentService
from src.services.grade_service import GradeService
from src.services.student_service import *
from datetime import datetime, timedelta

class TestAssignmentService(unittest.TestCase):
    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.__std_repo = Repository(lambda x: x.student_id)
        self.__grd_repo = Repository(lambda x: (x.assignment_id, x.student_id))
        self.__asn_repo = Repository(lambda x: x.assignment_id)
        self.__std_service = StudentService(self.__std_repo, self.__asn_repo, self.__grd_repo)
        self.__asn_service = AssignmentService(self.__asn_repo, self.__std_repo, self.__grd_repo)
        self.__grd_service = GradeService(self.__grd_repo, self.__asn_repo, self.__std_repo)
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

    def test_remove(self):
        self.__std_service.remove_student(4)
        self.assertEqual(len(self.__std_repo.get_all()), 19)

        with self.assertRaises(RepositoryError):
            self.__std_service.remove_student(300)

    def test_update(self):
        self.__std_service.add_student(21, "bubu", "916")
        self.__std_service.update_student(21, "no", "911")
        asn = self.__std_repo.find_id(21)

        self.assertEqual(asn.name, "no")
        self.assertEqual(asn.group, "911")

    def test_get_all(self):
        self.assertListEqual(self.__std_service.get_all_students(), self.__std_repo.get_all())
        self.assertEqual(len(self.__std_service.get_all_students_in_group("916")), 6)

    def test_get_ungraded_assignments_of_student(self):
        laur = 1
        self.__grd_service.assign_to_group(1, "916")
        self.__grd_service.assign_to_group(2, "916")
        # should return both assignments
        asns = self.__std_service.get_ungraded_assignments_of_student(laur)
        self.assertSetEqual(set(asns), {
            self.__asn_repo.find_id(2),
            self.__asn_repo.find_id(1),
        })
        self.__grd_service.apply_grade_to_student(1, laur, 10)
        # one is graded, return only the other
        asns = self.__std_service.get_ungraded_assignments_of_student(laur)
        self.assertListEqual(asns, [self.__asn_repo.find_id(2)])

        self.__grd_service.assign_to_group(4, "913")
        asns = self.__std_service.get_ungraded_assignments_of_student(laur)
        # should be uninfluenced since the prev assignation doesn't influence student 'laur'
        self.assertListEqual(asns, [self.__asn_repo.find_id(2)])

    def test_get_graded_students_for_assignment(self):
        # prepare
        laur = self.__std_repo.find_id(1)
        iacob = self.__std_repo.find_id(2)
        a1 = self.__asn_repo.find_id(1)
        a2 = self.__asn_repo.find_id(2)
        self.__grd_service.assign_to_group(a1.assignment_id, "916")
        self.__grd_service.assign_to_group(a1.assignment_id, "913")
        self.__grd_service.assign_to_group(a2.assignment_id, "916")
        self.__grd_service.assign_to_group(a2.assignment_id, "913")
        self.__grd_service.apply_grade_to_student(a1.assignment_id, laur.student_id, 8)
        self.__grd_service.apply_grade_to_student(a2.assignment_id, laur.student_id, 8)
        self.__grd_service.apply_grade_to_student(a2.assignment_id, iacob.student_id, 9)

        # test for A1
        dtos = self.__std_service.get_graded_students_for_assignment(a1.assignment_id)
        self.assertEqual(len(dtos), 1, f"Dtos was {dtos}")

        # test for A2
        dtos = self.__std_service.get_graded_students_for_assignment(a2.assignment_id)
        self.assertEqual(len(dtos), 2, f"Dtos was {dtos}")

    def test_get_students_with_late_assignments(self):
        self.__asn_service.add_assignment(21, "LATE ASSIGNMENT!", datetime.now() + timedelta(days=-10))
        late_students_dto = self.__std_service.get_students_with_late_assignments()
        # no one should have a late asn since it's not assigned
        self.assertEqual(len(late_students_dto), 0)

        self.__grd_service.assign_to_group(21, "916")

        students_in_916 = self.__std_repo.find_all_by_predicate(lambda s: s.group == "916")
        late_students_dto = self.__std_service.get_students_with_late_assignments()
        self.assertSetEqual(
            {dto.student for dto in late_students_dto},
            set(students_in_916)
        )
        self.assertSetEqual(
            {dto.assignment for dto in late_students_dto},
            {self.__asn_repo.find_id(21)}
        )
