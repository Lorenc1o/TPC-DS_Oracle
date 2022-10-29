import argparse
import time
import tpcds
from threading import Thread
from os import path

parser = argparse.ArgumentParser(description='TPC-DS Testing Script')
parser.add_argument('-S', '--svrinstance', help='Server and Instance Name', required=True)
parser.add_argument('-p', '--port', help='Port Number', required=True)
parser.add_argument('-D', '--db', help='Database Name', required=True)
parser.add_argument('-U', '--username', help='Username', required=True)
parser.add_argument('-P', '--password', help='Authenticating Password', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the data files are located', required=True)
parser.add_argument('-O', '--outputfile', help='UNC path where the query results will be stored', required=True)
parser.add_argument('-TP', '--throughputdir', help='UNC path of the streams', required=True)
parser.add_argument('-PREFIX', '--userprefix', help='User prefix in Oracle, default = \'\'', required=False, default='')
args = parser.parse_args()

'''
Function throughput_test

Description
	this functions connect to the database using the username provided as argument and the thread_id provided as parameter, then executes a batch of queries

Assumptions
	the users exist prior to execution and have access to the database

Parameters
	thread_id: integer representing the thread
'''
def throughput_test(thread_id):
    queries = path.join(args.throughputdir, 'query_' + thread_id + '.sql')
    output = path.join(args.throughputdir, 'queries_times' + thread_id + '.txt')

    username = args.userprefix + 'user' + thread_id
    password = 'user' + thread_id

    print('user: ' + username + '\npwd: ' + password)

    test_start_time = time.time()  # Timestamp for the starting time

    tpcds.run_query(queries, output, username, password)

    test_end_time = time.time()  # Timestamp for the ending time
    test_time = test_end_time - test_start_time  # Measured power test time
    print(test_time)

if __name__ == '__main__':    
    threads = []
    
    t0 = Thread(target = throughput_test, args = ('0',))
    threads.append(t0)
    t1 = Thread(target = throughput_test, args = ('1',))
    threads.append(t1)
    t2 = Thread(target = throughput_test, args = ('2',))
    threads.append(t2)
    t3 = Thread(target = throughput_test, args = ('3',))
    threads.append(t3)
    
    TP_test_start_time_1 = time.time()

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    TP_test_end_time_1 = time.time()
    TP_test_time_1 = TP_test_end_time_1 - TP_test_start_time_1

    output = f'THROUGHPUT TEST 1 TIME:\n\tThroughput test 1 start time = {TP_test_start_time_1}\n\tThroughput test 1 end time = {TP_test_end_time_1}\n\tThroughput test 1 time = {TP_test_time_1}\n'

    with open(args.outputfile, 'a') as f:
        f.write(output)
