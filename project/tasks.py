from Mywork import *



logger = get_task_logger(__name__)

app = Celery('tasks', backend='rpc://', broker='redis://localhost:6379')

@app.task(bind=True, name='tasks.my_task_0.jobs', soft_time_limit=300)
def my_task_0(self, Objectid, First_value, Second_value):
    try:

        obj = MyWork(Objectid, First_value, Second_value, logger)
        logger.info(f"Exec MyWork")

        #분석 시작 & download check 부분 DB업데이트
        obj.run()
        logger.info(f"run")

        #전체 결과 DB 업데이트
        obj.db_update()
        logger.info(f"db_update")

        pass
        #로직 정의


    except Exception as e:
        logger.error(f"[my_task_0], [{e}]")
    finally:
        return f"{obj.today} {obj.Objectid} finished!"

@app.task(bind=True, name='tasks.my_task_1.jobs', soft_time_limit=300)
def my_task_1(self, Objectid, First_value, Second_value):
    try:
        pass
        #로직 정의

    except Exception as e:
        logging.error(f"[my_task_1], [{e}]")
    finally:
        return f"{obj.today} {obj.Objectid} finished!"

@app.task(bind=True, name='tasks.my_task_2.jobs', soft_time_limit=300)
def my_task_2(self, Objectid, First_value, Second_value):
    try:
        pass
        #로직 정의

    except Exception as e:
        logging.error(f"[my_task_2], [{e}]")
    finally:
        return f"{obj.today} {obj.Objectid} finished!"

@app.task(bind=True, name='tasks.my_task_3.jobs', soft_time_limit=300)
def my_task_3(self, Objectid, First_value, Second_value):
    try:
        pass
        #로직 정의

    except Exception as e:
        logging.error(f"[my_task_3], [{e}]")
    finally:
        return f"{obj.today} {obj.Objectid} finished!"
