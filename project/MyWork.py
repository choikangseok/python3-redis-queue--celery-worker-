from celery import Celery
from command_ import *
import subprocess as sp
import datetime
import hashlib
import os, sys, time
from celery.exceptions import SoftTimeLimitExceeded
from bson.objectid import ObjectId
from time import sleep
import logging



class MyWork:

    def __init__(self, Objectid, First_value, Second_value):
        try:
            #Woker를 실행 하기위한 queue 데이터 init
            self.Objectid = Objectid
            self.today = datetime.date.today()
            self.dict_value = {}
            self.dict_value["First_value"] = First_value
            self.dict_value["Second_value"] = Second_value

        except Exception as e:
            logging.error(f"[{self.__class__.__name__}] __init__ {e}")

    def run(self):
        try:
            mongo = DBHandler()
            result = mongo.update_item_many({"_id" :ObjectId(self.Objectid)}, {"$set":self.dict_value}, "my_database", "my_collection")
            logging.debug(f"[{self.__class__.__name__}] [db_update] [{self.Objectid}] {result}")

        except Exception as e:
            logging.error(f"[{self.__class__.__name__}] [run] {e}")
        finally:
            mongo.client.close()
            logging.debug(f"[{self.__class__.__name__}] [db_update] [{self.Objectid}] mongodb close")
