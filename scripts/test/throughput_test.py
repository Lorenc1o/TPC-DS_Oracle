from multiprocessing import Pool, cpu_count
from os import listdir, path, getpid, system
import argparse
import time

parser = argparse.ArgumentParser(description='TPC-DS Throughput Test Script')
parser.add_argument('-S', '--svrinstance', help='Server and Instance Name', required=True)
parser.add_argument('-D', '--db', help='Database Name', required=True)
parser.add_argument('-U', '--username', help='Username', required=True)
parser.add_argument('-P', '--password', help='Authenticating Password', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the data files are located', required=True)
parser.add_argument('-O', '--outputfile', help='UNC path where the throughput test time will be logged', required=False, default=None)
args = parser.parse_args()

if not args.svrinstance or not args.db or not args.username or not args.password or not args.filespath:
    parser.print_help()
    exit(1)

class User(object):
    def __init__(self, username, password, stream):
        self.username = username
        self.password = password
        self.stream = stream

def execute_stream(file_name):
    print("Executing from CPU: %s" % getpid())
    full_path = path.join(args.filespath, file_name)
    sqlplus = 'sqlplus %s/%s@%s/%s @%s' % (
        args.username, args.password, args.svrinstance, args.db, full_path)
    print(sqlplus)
    system(sqlplus)
    print("Done executing from CPU: %s" % getpid())

if __name__ == "__main__":
    TP_test_start_time_1 = time.time()

    p = Pool(processes=2*cpu_count())
    for file in listdir(args.filespath):
        if file.endswith(".sql"):
            p.apply_async(execute_stream, [file])
    p.close()
    p.join()

    TP_test_end_time_1 = time.time()
    TP_test_time_1 = TP_test_end_time_1 - TP_test_start_time_1
    output = f'THROUGHPUT TEST 1 TIME:\n\tThroughput test 1 start time = {TP_test_start_time_1}\n\tThroughput test 1 end time = {TP_test_end_time_1}\n\tThroughput test 1 time = {TP_test_time_1}\n'
    print(output)

    if args.outputfile is not None:
        with open(args.outputfile, 'w+') as f:
            f.write(output)
