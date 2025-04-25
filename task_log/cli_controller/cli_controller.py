from task_log.cli_controller.project_cli_controller import ProjectCliController
from task_log.cli_controller.record_cli_controller import RecordCliController
from task_log.cli_controller.task_cli_controller import TaskCliController
from task_log.crud.project_crud import ProjectCrud
from task_log.crud.task_crud import TaskCrud


class CliController:
    def __init__(
        self,
        proj_crud: ProjectCrud,
        task_crud: TaskCrud,
        proj_cli_controller: ProjectCliController,
        task_cli_controller: TaskCliController,
        record_cli_controller: RecordCliController,
    ):
        self._proj_crud = proj_crud
        self._task_crud = task_crud
        self._proj_cli_controller = proj_cli_controller
        self.task_cli_controller = task_cli_controller
        self._record_cli_controller = record_cli_controller

    def read_all(self):
        projects = self._proj_crud.get_all()
        for project in projects:
            self._proj_cli_controller.print(project)
            tasks = self._task_crud.get_by_project(project)
            for task in tasks:
                self.task_cli_controller.print(task)
                self._record_cli_controller.print_records_of_project(project, task)
