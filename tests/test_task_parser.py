try:
    from context import google_tasks
except ModuleNotFoundError:
    from .context import google_tasks

import unittest


class TestTaskParser(unittest.TestCase):

    def setUp(self):
        self.good_task = "tasks_good.json"
        self.bad_task = "tasks_bad.json"
        self.TP = google_tasks.task_parser.TaskParser

    def test_good_task(self):
        self.assertIsInstance(self.TP(self.good_task).get_tasks(), list)

    def test_bad_task(self):
        with self.assertRaises(google_tasks.task_parser.UnexpectedDayName):
            self.TP(self.bad_task)

if __name__ == '__main__':
    unittest.main()
