import unittest
import run_tasks


class TDDTest(unittest.TestCase):

    def test_run_task_file_before(self):
        result = run_tasks.main(['run_tasks.py', '_input/test.csv',"0"])
        self.assertEqual(result, False)

    def test_run_task_file_exist(self):
        result = run_tasks.main(['run_tasks.py', '_input/test.csv',"0"])
        self.assertEqual(result, True)



if __name__ == '__main__':
    unittest.main()
