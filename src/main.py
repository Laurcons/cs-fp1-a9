from src.repository.history_repository import HistoryRepository
from src.repository.repository import Repository
from src.services.assignment_service import AssignmentService
from src.services.grade_service import GradeService
from src.services.history_manager import HistoryManager
from src.services.student_service import StudentService
from src.ui.console import Console

student_repository = Repository(lambda s: s.student_id)
assignment_repository = Repository(lambda a: a.assignment_id)
grade_repository = Repository(lambda g: (g.assignment_id, g.student_id))
undo_repository = HistoryRepository()
redo_repository = HistoryRepository()

history_manager = HistoryManager(undo_repository, redo_repository)

grade_service = GradeService(history_manager, grade_repository, assignment_repository, student_repository)
student_service = StudentService(history_manager, student_repository)
assignment_service = AssignmentService(history_manager, assignment_repository)

console = Console(history_manager, student_service, assignment_service, grade_service)
console.start()
