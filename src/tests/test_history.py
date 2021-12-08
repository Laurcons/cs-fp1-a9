import unittest

from src.domain.undoable_operation import UndoableOperation
from src.repository.history_repository import HistoryRepository
from src.services.history_manager import HistoryManager


class TestHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.__undo_repo = HistoryRepository()
        self.__redo_repo = HistoryRepository()
        self.__history = HistoryManager(self.__undo_repo, self.__redo_repo)

    def test_manager(self):
        list_with_stuff = [1, 9, 8, 3]
        list_with_stuff.append(4)
        self.__history.add_operation(
            lambda: list_with_stuff.remove(4), [],
            list_with_stuff.append, [4]
        )

        self.__history.undo()
        self.assertListEqual(list_with_stuff, [1, 9, 8, 3])

        self.__history.redo()
        self.assertListEqual(list_with_stuff, [1, 9, 8, 3, 4])

        self.__history.undo()
        self.assertListEqual(list_with_stuff, [1, 9, 8, 3])

        self.__history.redo()
        self.assertListEqual(list_with_stuff, [1, 9, 8, 3, 4])

