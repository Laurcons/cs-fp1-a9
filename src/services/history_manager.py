from typing import Callable

from src.domain.undoable_operation import UndoableOperation
from src.repository.history_repository import HistoryRepository

class HistoryError(BaseException):
    pass

class HistoryManager:
    def __init__(self, undo_repository: HistoryRepository, redo_repository: HistoryRepository):
        self.__undo_repo = undo_repository
        self.__redo_repo = redo_repository

    def add_operation(self, undo_op: Callable, undo_params: list, redo_op: Callable, redo_params: list):
        op = UndoableOperation(undo_op, undo_params, redo_op, redo_params)
        self.__undo_repo.push(op)
        self.__redo_repo.clear()

    def undo(self):
        if self.__undo_repo.count() == 0:
            raise HistoryError("Nothing to undo.")
        op = self.__undo_repo.pop()
        op.perform_undo()
        self.__redo_repo.push(op)

    def redo(self):
        if self.__redo_repo.count() == 0:
            raise HistoryError("Nothing to redo.")
        op = self.__redo_repo.pop()
        op.perform_redo()
        self.__undo_repo.push(op)