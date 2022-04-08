import unittest
import run_tasks
import tasks
from MyWork import *
from celery.utils.log import get_task_logger


class TDDTest(unittest.TestCase):

    def test_run_task_file_before(self):
        result = run_tasks.main(['run_tasks.py', '_input_file/test.csv',"0"])
        self.assertEqual(result, True)

    def test_tasks(self):
        result = tasks.my_task_0("ObjectId(""623ab4b85d3e87467f54cb1b"")","test2_first","test2_second")
        self.assertEqual(result,True)

    def test_class_MyWork(self):
        logger = get_task_logger(__name__)
        mywork = MyWork("ObjectId(""623ab4b85d3e87467f54cb1b"")","test2_first","test2_second", logger)


    #DBHandler already Test Complete

        #init test

if __name__ == '__main__':
    unittest.main()
