from tasks import *
import csv,sys

def main(argv):
    if len(argv) != 3:
        print("Usage python run_tasks.py <input_file> <use_collections>")
        exit(0)

    input_file = argv
    collection_num = int(argv)


    #수집 유형에 따른 다른 task를 실행하기 위함
    if not collection_num in range(0, 4):
        print("Collections num range in [0,1,2,3]")
        exit(0)
    file_name, file_ext = os.path.splitext(input_file)

    # Check file extension
    if file_ext not in '.csv':
        print("Only input .csv format")
        exit(0)

    # Open file
    #파일을 읽어서 해당 데이터를 읽고 Queue 프로세스를 진행함
    try:
        with open(input_file, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                Objectid = row['_id']
                First_value = row['_first_value']
                Second_value = row['_second_value']

                #수집 유형에 따라 다른 task를 실행
                if collection_num == 0:
                    result = my_task_0.delay(Objectid, First_value, Second_value)
                elif collection_num == 1:
                    result = my_task_1.delay(Objectid, First_value, Second_value)
                elif collection_num == 2:
                    result = my_task_2.delay(Objectid, First_value, Second_value)
                elif collection_num == 3:
                    result = my_task_3.delay(Objectid, First_value, Second_value)
    except:
        return False
    else:
        print("[run_tasks.py]",result)
        return True

if __name__ == '__main__':
    main(sys.argv[1:])
        # Check parameter
        # run_tasks.py <csv file>
