
import unittest
from src.repository.repository import *

class TestRepository1(unittest.TestCase):
    def test_repository(self):
        # create a mock repository of number tuples: (id, sth_else)
        repo = Repository(lambda x: x[0])

        repo.add((1, 3))
        repo.add((2, 4))
        repo.add((3, 5))

        with self.assertRaises(RepositoryError):
            repo.add((2, 6))  # id collision

        repo.insert_all([
            (4, 5),
            (5, 6)
        ])

        with self.assertRaises(RepositoryError):
            repo.insert_all([
                (4, 5)  # id collision
            ])

        self.assertFalse(repo.id_exists(100))
        self.assertTrue(repo.id_exists(3))

        self.assertListEqual([(3, 5), (4, 5)], repo.find_all_by_predicate(lambda t: t[1] == 5))

        with self.assertRaises(RepositoryError):
            repo.remove_id(200)

        repo.remove_id(3)
