import json
import datetime

class TaskParser(object):
    def __init__(self, filename="tasks.json"):
        self.filename = self._read_file(filename)
        self.todo_list = []
        self._parse_file()

    def __call__(self):
        pass

    def _read_file(self, filename):
        with open(filename, 'r') as f:
            return(json.loads(f.read()))

    def _parse_file(self):
        for task_list, value in self.filename.items():
            for task, days in value.items():
                for day in days:
                    if self._parse_day(day):
                        self.todo_list.append((task_list, task))

    def _parse_day(self, day):
        today = datetime.date.today().strftime("%a")
        if day == today:
            return(True)
        else:
            return(False)

tasks = TaskParser()
