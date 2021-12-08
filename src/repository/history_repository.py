from src.domain.undoable_operation import UndoableOperation

class HistoryRepository:
    def __init__(self):
        self.__stack = []

    def clear(self):
        self.__stack = []

    def count(self):
        return len(self.__stack)

    def push(self, op: UndoableOperation):
        self.__stack.append(op)

    def pop(self) -> UndoableOperation:
        return self.__stack.pop()
