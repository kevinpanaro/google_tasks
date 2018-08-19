import json
import datetime
import calendar


class TaskParser(object):
    """
    Handles the creation of the Tasks for that day
    given an input tasks json

    :param filename: the name of the tasks file (optional)
    :returns: a list of task tuples
    """
    def __init__(self, filename="tasks.json"):
        self.filename = self._read_file(filename)
        self.todo_list = []
        self._parse_file()

    def __call__(self):
        """
        When the class is called immediately, and
        returns the todo_list

        :returns: the list of tuples
        """
        return(self.todo_list)

    def _read_file(self, filename):
        """
        Reads the file

        :returns: task dict
        """
        with open(filename, 'r') as f:
            return(json.loads(f.read()))

    def _parse_file(self):
        """
        Parses the file for tasklist and tasks
        """
        for task_list, value in self.filename.items():
            for task, days in value.items():
                for day in days:
                    self._parse_day(day, task_list, task)

    def _parse_day(self, day, task_list, task):
        """
        Since everything is validated, this will see
        if the day matches the value, and then append
        that tasklist and task to the todo_list

        :param day: the day the task must be done
        :param task_list: the task list
        :param task: the task
        """
        today = datetime.date.today().strftime("%a")
        self._validate_tasks(day, task_list, task)
        if day == today:
            self.todo_list.append((task_list, task))

    def _validate_tasks(self, day, task_list, task):
        """
        This validates that the task names are
        valid

        :returns: UnexpectedDayName, if bad
        """
        valid = list(calendar.day_abbr)
        if day not in valid:
            raise UnexpectedDayName(f"\"{day}\" day in {task_list} "
                                    "-> {task} not in {valid}.")


class UnexpectedDayName(Exception):
    pass
