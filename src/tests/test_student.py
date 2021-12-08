import unittest

from src.domain.student import Student, StudentValidator, StudentValidationError


class TestStudent(unittest.TestCase):
    def test_basic(self):
        self.__student = Student(1, "Martin Luther King", "916")
        self.assertEquals(self.__student.specialization, "IE")
        self.assertEquals(self.__student.year, "1")

    def test_get_year(self):
        self.__student = Student(2, "Edward Iakab gg wp", "933")
        self.assertEquals(self.__student.year, "3")

    def test_validate_group(self):
        with self.assertRaises(StudentValidationError) as re:
            self.__student = Student(3, "who tf", "143")
        self.assertEquals(str(re.exception), "Group is invalid")
