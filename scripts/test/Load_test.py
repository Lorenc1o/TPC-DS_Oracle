import argparse
import cx_Oracle
import time
from os import path, listdir
from multiprocessing import Pool
import tpcds


parser = argparse.ArgumentParser(description='TPC-DS Testing Script')
parser.add_argument('-S', '--svrinstance', help='Server and Instance Name', required=True)
parser.add_argument('-p', '--port', help='Port Number', required=True)
parser.add_argument('-D', '--db', help='Database Name', required=True)
parser.add_argument('-U', '--username', help='Username', required=True)
parser.add_argument('-P', '--password', help='Authenticating Password', required=True)
parser.add_argument('-T', '--tpcdspath', help='UNC path where the tpcds.sql script is located. You should write the full path: [path_to_dir]/tpcds.sql', required=True)
parser.add_argument('-TRI', '--tpcdsripath', help='UNC path where the tpcds_ri.sql script is located. You should write the full path: [path_to_dir]/tpcds_ri.sql', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the data files are located', required=True)
parser.add_argument('-C', '--ctlpath', help='UNC path where the control files are located', required=True)
parser.add_argument('-DROP', '--drop', help='Should tables be dropped (y/n), default: y', required=False, default='y')
parser.add_argument('-O', '--outputfile', help='UNC path where the query results will be stored', required=True)
args = parser.parse_args()

if not args.svrinstance or not args.port or not args.db or not args.username or not args.password or not args.tpcdspath or not args.tpcdsripath or not args.filespath or not args.ctlpath or not args.outputfile:
    parser.print_help()
    exit(1)

if __name__ == "__main__":
    dsn = args.svrinstance + ':' + args.port + '/' + args.db
    conn = cx_Oracle.connect(user=args.username, password=args.password, dsn=dsn)
    c = conn.cursor() 
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

#TODO see how to do this in parallel keeping the order of the files
    p = Pool(processes=1)

    for file in listdir(args.filespath):
        if file.endswith(".dat"):
            table_name = ''.join([i for i in path.splitext(file)[0] if not i.isdigit()]).rstrip('_')
            p.apply_async(tpcds.load_files, [args.filespath, args.ctlpath, args.username, args.password, args.svrinstance, args.db, table_name, file])
    p.close()
    p.join()

    load_end_time = time.time() # Timestamp for the ending time
    load_time = load_end_time - load_start_time # Measured load time
    output = f'LOAD TIME:\n\tLoad start time = {load_start_time}\n\tLoad end time = {load_end_time}\n\tLoad time = {load_time}\n'
    
    conn.close()

    tpcds.run_query(args.tpcdsripath, None, args.username, args.password, args.svrinstance, args.port, args.db)

    with open(args.outputfile, 'w') as f:
        f.write(output)
