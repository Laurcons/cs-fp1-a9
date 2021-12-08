from typing import Callable


class UndoableOperation:
    def __init__(self, undo_operation: Callable, undo_params: list, redo_operation: Callable, redo_params: list):
        self.__undo_operation = undo_operation
        self.__undo_params = undo_params
        self.__redo_operation = redo_operation
        self.__redo_params = redo_params

    def perform_undo(self):
        self.__undo_operation(*self.__undo_params)

    def perform_redo(self):
        self.__redo_operation(*self.__redo_params)
