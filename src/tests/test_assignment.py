import unittest
from src.domain.assignment import *


class TestAssignment(unittest.TestCase):
    def test_overdue1(self):
        self.__asn = Assignment(1, "The toughest.", datetime.datetime.now() + datetime.timedelta(hours=10))
        self.assertFalse(self.__asn.is_overdue)

    def test_overdue2(self):
        self.__asn = Assignment(1, "The toughest.", datetime.datetime.now() - datetime.timedelta(hours=10))
        self.assertTrue(self.__asn.is_overdue)
