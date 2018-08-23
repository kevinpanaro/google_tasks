try:
    from wrapper import GoogleTasksWrapper
    from task_parser import TaskParser
except ModuleNotFoundError:
    from .wrapper import GoogleTasksWrapper
    from .task_parser import TaskParser


def core():
    google_tasks = GoogleTasksWrapper()
    tasks = TaskParser().get_tasks()

    for task in tasks:
        task_list, task = task
        google_tasks.add(task_list, task)


if __name__ == '__main__':
    core()
