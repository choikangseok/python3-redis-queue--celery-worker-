from celery import Celery
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded
import datetime
from bson.objectid import ObjectId


class MyWork:
    def __init__(self, Objectid, First_value, Second_value, logger):
        try:
            #Woker를 실행 하기위한 queue 데이터 init
            self.logger = logger
            self.Objectid = Objectid
            self.dict_value = {}
            self.dict_value["Today"] = datetime.date.today()
            self.dict_value["First_value"] = First_value
            self.dict_value["Second_value"] = Second_value
        except Exception as e:
            self.logger.error(f"[{self.__class__.__name__}] __init__ {e}")

    def run(self):
        try:
            mongo = DBHandler()
            result = mongo.update_item_many({"_id" :ObjectId(self.Objectid)}, {"$set":self.dict_value}, "my_database", "my_collection")

        except Exception as e:
            self.logger.error(f"[{self.__class__.__name__}] [run] {e}")
        finally:
            mongo.client.close()
            self.logger.debug(f"[{self.__class__.__name__}] [db_update] [{self.Objectid}] mongodb close")
