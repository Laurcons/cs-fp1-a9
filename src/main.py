from src.domain.student import Student
from src.lib.settings import Settings
from src.repository.assignment_mongo_repository import AssignmentMongoRepository
from src.repository.assignment_text_repository import AssignmentTextRepository
from src.repository.grade_mongo_repository import GradeMongoRepository
from src.repository.grade_text_repository import GradeTextRepository
from src.repository.history_repository import HistoryRepository
from src.repository.json_repository import JsonRepository
from src.repository.pickle_repository import PickleRepository
from src.repository.repository import Repository
from src.repository.student_mongo_repository import StudentMongoRepository
from src.repository.student_text_repository import StudentTextRepository
from src.repository.text_repository import TextRepository
from src.services.assignment_service import AssignmentService
from src.services.grade_service import GradeService
from src.services.history_manager import HistoryManager
from src.services.student_service import StudentService
from src.ui.console import Console

# read settings file
settings = Settings()
settings.load_file("application.properties")

student_repository = None
assignment_repository = None
grade_repository = None
student_lambda = lambda s: s.student_id
assignment_lambda = lambda a: a.assignment_id
grade_lambda = lambda g: (g.assignment_id, g.student_id)

if settings['repository'] == 'inmemory':
    student_repository = Repository(student_lambda)
    assignment_repository = Repository(assignment_lambda)
    grade_repository = Repository(grade_lambda)
if settings['repository'] == 'pickle':
    student_repository = PickleRepository(settings['students_path'], student_lambda)
    assignment_repository = PickleRepository(settings['assignments_path'], assignment_lambda)
    grade_repository = PickleRepository(settings['grades_path'], grade_lambda)
if settings['repository'] == 'csv':
    student_repository = StudentTextRepository(settings['students_path'])
    assignment_repository = AssignmentTextRepository(settings['assignments_path'])
    grade_repository = GradeTextRepository(settings['grades_path'])
if settings['repository'] == 'json':
    student_repository = JsonRepository(settings['students_path'], student_lambda)
    assignment_repository = JsonRepository(settings['assignments_path'], assignment_lambda)
    grade_repository = JsonRepository(settings['grades_path'], grade_lambda)

student_repository = StudentMongoRepository(settings['connection_string'])
assignment_repository = AssignmentMongoRepository(settings['connection_string'])
grade_repository = GradeMongoRepository(settings['connection_string'])

undo_repository = HistoryRepository()
redo_repository = HistoryRepository()

history_manager = HistoryManager(undo_repository, redo_repository)

grade_service = GradeService(history_manager, grade_repository, assignment_repository, student_repository)
student_service = StudentService(history_manager, student_repository)
assignment_service = AssignmentService(history_manager, assignment_repository)

console = Console(history_manager, student_service, assignment_service, grade_service)
console.start()
