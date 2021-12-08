from src.domain.student import Student
from src.repository.repository import Repository
from src.services.history_manager import HistoryManager


class StudentOperationError(BaseException):
    pass

class StudentService:
    """ Handles operations on the Student repository. """
    def __init__(self, history_manager: HistoryManager, student_repository: Repository):
        self.__student_repository = student_repository
        self.__history = history_manager

    def populate(self):
        """ Adds a couple of entries. """
        self.__student_repository.insert_all([
            Student(1, "Pricop Laurentiu", "916"),
            Student(2, "Edward Iakab", "913"),
            Student(3, "Briana Salagean", "916"),
            Student(4, "Mircea Gabriel", "111"),
            Student(5, "Stan Andrei", "916"),
            Student(6, "Bradea Codrin", "435"),
            Student(7, "Pop Codin", "123"),
            Student(8, "Gates Bill", "432"),
            Student(9, "Manole Mesteru", "732"),
            Student(10, "Inca Unu", "123"),
            Student(11, "Pricop Laurentiu 2", "916"),
            Student(12, "Edward Iakab 2", "913"),
            Student(13, "Briana Salagean 2", "916"),
            Student(14, "Mircea Gabriel 2", "111"),
            Student(15, "Stan Andrei 2", "916"),
            Student(16, "Bradea Codrin 2", "435"),
            Student(17, "Pop Codin 2", "123"),
            Student(18, "Gates Bill 2", "432"),
            Student(19, "Manole Mesteru 2", "732"),
            Student(20, "Inca Unu 2", "123"),
        ])

    def add_student(self, student_id, name, group):
        """ Adds a new student. """
        if self.__student_repository.id_exists(student_id):
            raise StudentOperationError("Student id already exists")
        student = Student(student_id, name, group)
        self.__student_repository.add(student)
        self.__history.add_operation(
            self.__student_repository.remove_id, [student_id],
            self.__student_repository.add, [student]
        )

    def update_student(self, student_id, name, group):
        """ Updates the data for a student, found by their id. """
        student = self.__student_repository.find_id(student_id)
        original = Student(student.student_id, student.name, student.group)
        student.name = name
        student.group = group
        self.__student_repository.update(student)
        self.__history.add_operation(
            self.__student_repository.update, [original],
            self.__student_repository.update, [student]
        )

    def get_all_students(self):
        """ Returns a list of all the students. """
        return self.__student_repository.get_all()

    def get_all_students_in_group(self, group):
        """ Returns a list of all students that are in a group. """
        students = self.__student_repository.get_all()
        return [s for s in students if s.group == group]
