import sys
from task_log.json_db.db_info import DbInfo
from task_log.crud.project_crud import ProjectCrud
from task_log.crud.record_crud import RecordCrud
from task_log.crud.task_crud import TaskCrud
from task_log.cli_controller.project_cli_controller import ProjectCliController
from task_log.cli_controller.task_cli_controller import TaskCliController
from task_log.cli_controller.record_cli_controller import RecordCliController
from task_log.cli_controller.cli_controller import CliController


class Cli:
    def __init__(
        self,
        project_cli_controller: ProjectCliController,
        task_cli_controller: TaskCliController,
        record_cli_controller: RecordCliController,
        cli_controller: CliController,
    ):
        self._project_cli_controller = project_cli_controller
        self._task_cli_controller = task_cli_controller
        self._record_cli_controller = record_cli_controller
        self._cli_controller = cli_controller

    def display_menu(self, layout="vertical", grid=None):
        menu_items = [
            "Task Log Menu",
            "-" * 20 + "\n",
            "1. New Project",
            "2. Task",
            "3. Record",
            "4. End Active Record",
            "5. Projects",
            "6. Tasks",
            "7. Records",
            "8. All",
            "9. Exit",
        ]

        title = menu_items[0]
        options = menu_items[1:]

        print(f"\n{title}")

        if grid is not None:
            try:
                rows, cols = grid
                for i in range(rows):
                    start = i * cols
                    end = start + cols
                    row_items = options[start:end]
                    print("  |  ".join(row_items))
                return
            except (ValueError, TypeError):
                print("Invalid grid. Use tuple (rows, cols). Defaulting to layout.")

        if layout == "vertical":
            print("\n".join(options))
        elif layout == "horizontal":
            print("  |  ".join(options))
        else:
            print(
                "Invalid layout. Use 'vertical' or 'horizontal'. Defaulting to vertical."
            )
            print("\n".join(options))

    def run(self):
        self.display_menu(layout="horizontal")
        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            self._project_cli_controller.from_cli_input()
        elif choice == "2":
            self._task_cli_controller.from_cli_input()
        elif choice == "3":
            self._record_cli_controller.from_cli_input()
        elif choice == "4":
            self._record_cli_controller.update_record()
        elif choice == "5":
            self._project_cli_controller.print_all()
        elif choice == "6":
            self._task_cli_controller.print_tasks_of_project()
        elif choice == "7":
            self._record_cli_controller.print_records_of_project()
        elif choice == "8":
            self._cli_controller.read_all()
        elif choice == "9":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice.")


def main():
    db_tables = DbInfo()

    project_crud = ProjectCrud(db_tables)
    task_crud = TaskCrud(db_tables)
    record_crud = RecordCrud(db_tables)

    project_cli_controller = ProjectCliController(db_tables, project_crud)
    task_cli_controller = TaskCliController(
        db_tables, task_crud, project_cli_controller
    )
    record_cli_controller = RecordCliController(
        db_tables, record_crud, project_cli_controller, task_cli_controller
    )

    cli = Cli(
        project_cli_controller,
        task_cli_controller,
        record_cli_controller,
        CliController(
            project_crud,
            task_crud,
            record_crud,
            project_cli_controller,
            task_cli_controller,
            record_cli_controller,
        ),
    )
    cli.run()


if __name__ == "__main__":
    main()
