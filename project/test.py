import unittest
import run_tasks


class TDDTest(unittest.TestCase):

    def test_run_task_file_before(self):
        result = run_tasks.main(['_input/test.csv',0])
        self.assertEqualt(result, False)

    def test_run_task_file_exist(self):
        result = run_tasks.main(['_input/test.csv',0])
        self.assertEqualt(result, True)



if __name__ == '__main__':
    unittest.main()
