import argparse
import time
from os import path
import tpcds


parser = argparse.ArgumentParser(description='TPC-DS Testing Script')
parser.add_argument('-S', '--svrinstance', help='Server and Instance Name', required=True)
parser.add_argument('-p', '--port', help='Port Number', required=True)
parser.add_argument('-D', '--db', help='Database Name', required=True)
parser.add_argument('-U', '--username', help='Username', required=True)
parser.add_argument('-P', '--password', help='Authenticating Password', required=True)
parser.add_argument('-Q', '--querypath', help='UNC path of query_0.sql. You should write the full path: [path_to_dir]/query_0.sql', required=True)
parser.add_argument('-O', '--outputfile', help='UNC path where the query results will be stored', required=True)
args = parser.parse_args()

if not args.svrinstance or not args.port or not args.db or not args.username or not args.password or not args.filespath or not args.querypath or not args.outputfile:
    parser.print_help()
    exit(1)

if __name__ == "__main__":
    power_test_start_time = time.time() # Timestamp for the starting time

    new_output = args.outputfile[:-4] + '_power_test.txt'
    tpcds.run_query(args.querypath, output=new_output)

    power_test_end_time = time.time() # Timestamp for the ending time
    power_test_time = power_test_end_time - power_test_start_time # Measured power test time

    output = f'POWER TEST TIME:\n\tPower test start time = {power_test_start_time}\n\tPower test end time = {power_test_end_time}\n\tPower test time = {power_test_time}\n'

    with open(args.outputfile, 'a') as f:
        f.write(output)
