
import unittest
from src.domain.grade import *

class TestGrade(unittest.TestCase):
    def test_grade(self):
        with self.assertRaises(GradeValidationError):
            Grade(1, 2, 11)
        with self.assertRaises(GradeValidationError):
            Grade(2, 1, -1)
        Grade(2, 1, 5)
