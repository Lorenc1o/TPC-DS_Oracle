from multiprocessing import Pool, cpu_count
from os import listdir, path, getpid, system
import _thread
import argparse
import cx_Oracle
import time

parser = argparse.ArgumentParser(description='TPC-DS Testing Script')
parser.add_argument('-S', '--svrinstance', help='Server and Instance Name', required=True)
parser.add_argument('-p', '--port', help='Port Number', required=True)
parser.add_argument('-D', '--db', help='Database Name', required=True)
parser.add_argument('-U', '--username', help='Username', required=True)
parser.add_argument('-P', '--password', help='Authenticating Password', required=True)
parser.add_argument('-T', '--tpcdspath', help='UNC path where the tpcds.sql script is located. You should write the full path: [path_to_dir]/tpcds.sql', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the data files are located', required=True)
parser.add_argument('-C', '--ctlpath', help='UNC path where the control files are located', required=True)
parser.add_argument('-Q', '--querypath', help='UNC path of query_0.sql. You should write the full path: [path_to_dir]/query_0.sql', required=True)
parser.add_argument('-O', '--outputdir', help='UNC path where the query results will be stored', required=True)
parser.add_argument('-DROP', '--drop', help='Should tables be dropped (y/n), default: y', required=False, default='y')
args = parser.parse_args()

if not args.svrinstance or not args.port or not args.db or not args.username or not args.password or not args.tpcdspath or not args.filespath or not args.ctlpath or not args.querypath or not args.outputdir:
    parser.print_help()
    exit(1)

"""
Function load_files

Description
	load_files calls the Oracle data loader, sqlldr, with the arguments
	previously got from command line or provided as parameter

Parameters
	table_name: string with the name of the table to be populated
	file_name: string with the name of the file containing the data

Output
	None
"""
def load_files(table_name, file_name):
    full_path = path.join(args.filespath, file_name)
    ctl_path = path.join(args.ctlpath, table_name + '.ctl')
    log_path = path.join(args.filespath, file_name[:-3] + 'log')
    sqlldr = 'sqlldr userid=%s/%s@%s/%s control=%s data=%s log=%s bad=%s' % (
        args.username, args.password, args.svrinstance, args.db, ctl_path, full_path, log_path, log_path)
    system(sqlldr)

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
    if thread_id == 0:
        sub_user = argv.username
    else:
        sub_user = argv.username + f'{thread_id}'
#TODO make the query streams

if __name__ == "__main__":
#Connection to the database
    dsn = args.svrinstance + ':' + args.port + '/' + args.db
    conn = cx_Oracle.connect(user=args.username, password=args.password, dsn=dsn)

    c = conn.cursor()

#Schema creation
#	we execute a modified version of the provided sql script tpcds
#	which drops all the tables and creates them again

    f = open(f'{args.tpcdspath}')
    full_sql = f.read()
    sql_commands = full_sql.split(';')
    
    #If we don't want to drop tables, we omit the drop commands
    if args.drop == 'n':
        sql_commands = [com for com in sql_commands if 'drop table' not in com ]
    sql_commands = sql_commands[:-1] #we have one extra empty command
    for sql_command in sql_commands:
        c.execute(sql_command)

#Load test
#	done from flat files, so we only account for strictly loading time
    load_start_time = time.time() # Timestamp for the starting time

    p = Pool(processes=2*cpu_count())

    for file in listdir(args.filespath):
        if file.endswith(".dat"):
            table_name = ''.join([i for i in path.splitext(file)[0] if not i.isdigit()]).rstrip('_')
            p.apply_async(load_files, [table_name, file])
    p.close()
    p.join()

    load_end_time = time.time() # Timestamp for the ending time
    load_time = load_end_time - load_start_time # Measured load time
    output = f'LOAD TIME:\n\tLoad start time = {load_start_time}\n\tLoad end time = {load_end_time}\n\tLoad time = {load_time}\n'

#Power test
    f = open(f'{args.querypath}')
    full_sql = f.read()
    sql_commands = full_sql.split(';')
    
    #If we don't want to drop tables, we omit the drop commands
    sql_commands = sql_commands[:-1] #we have one extra empty command

    output += '----------------------------------------------------------\n'

    power_test_start_time = time.time() # Timestamp for the starting time

    for sql_command in sql_commands:
        c.execute(sql_command)

    power_test_end_time = time.time() # Timestamp for the ending time
    power_test_time = power_test_end_time - power_test_start_time # Measured power test time

    output += f'POWER TEST TIME:\n\tPower test start time = {power_test_start_time}\n\tPower test end time = {power_test_end_time}\n\tPower test time = {power_test_time}\n'
    conn.close()

#Throughput Test 1
    TP_test_start_time_1 = time.time()

    _thread.start_new_thread(throughput_test, ('0'))
    _thread.start_new_thread(throughput_test, ('1'))
    _thread.start_new_thread(throughput_test, ('2'))
    _thread.start_new_thread(throughput_test, ('3'))

    TP_test_end_time_1 = time.time()
    TP_test_time_1 = time.time()

    output += '----------------------------------------------------------\n'
    output += f'THROUGHPUT TEST 1 TIME:\n\tThroughput test 1 start time = {TP_test_start_time_1}\n\tThroughput test 1 end time = {TP_test_end_time_1}\n\tThroughput test 1 time = {TP_test_time_1}\n'

#Output results
    with open(args.outputdir, 'w') as f:
        print(output, file=f)
