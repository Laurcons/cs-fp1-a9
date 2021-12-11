
import unittest

from src.tests.test_assignment import TestAssignment
from src.tests.test_assignment_service import TestAssignmentService
from src.tests.test_grade import TestGrade
from src.tests.test_grade_service import TestGradeService
from src.tests.test_history import TestHistory
from src.tests.test_repository import TestRepository
from src.tests.test_settings import TestSettings
from src.tests.test_student import TestStudent
from src.tests.test_student_service import TestStudentService


def test_all():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAssignment))
    suite.addTest(unittest.makeSuite(TestAssignmentService))
    suite.addTest(unittest.makeSuite(TestGrade))
    suite.addTest(unittest.makeSuite(TestGradeService))
    suite.addTest(unittest.makeSuite(TestHistory))
    suite.addTest(unittest.makeSuite(TestRepository))
    suite.addTest(unittest.makeSuite(TestSettings))
    suite.addTest(unittest.makeSuite(TestStudent))
    suite.addTest(unittest.makeSuite(TestStudentService))

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    test_all()