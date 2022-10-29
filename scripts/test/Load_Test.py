from multiprocessing import Pool, cpu_count
from os import listdir, path, getpid, system
import argparse
import time

parser = argparse.ArgumentParser(description='TPC-DS Data Loading Script')
parser.add_argument('-S', '--svrinstance', help='Server and Instance Name', required=True)
parser.add_argument('-D', '--db', help='Database Name', required=True)
parser.add_argument('-U', '--username', help='Username', required=True)
parser.add_argument('-P', '--password', help='Authenticating Password', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the data files are located', required=True)
parser.add_argument('-C', '--ctlpath', help='UNC path where the control files are located', required=True)
parser.add_argument('-O', '--outputfile', help='UNC path where the load time will be logged', required=False, default=None)
args = parser.parse_args()

if not args.svrinstance or not args.db or not args.username or not args.password or not args.filespath or not args.ctlpath:
    parser.print_help()
    exit(1)


def load_files(table_name, file_name):
    print("Loading from CPU: %s" % getpid())
    full_path = path.join(args.filespath, file_name)
    ctl_path = path.join(args.ctlpath, table_name + '.ctl')
    log_path = path.join(args.filespath, file_name[:-3] + 'log')
    sqlldr = 'sqlldr userid=%s/%s@%s/%s control=%s data=%s log=%s' % (
        args.username, args.password, args.svrinstance, args.db, ctl_path, full_path, log_path)
    print(sqlldr)
    system(sqlldr)
    print("Done loading data from CPU: %s" % getpid())


if __name__ == "__main__":
    load_start_time = time.time()
    p = Pool(processes=2*cpu_count())
    for file in listdir(args.filespath):
        if file.endswith(".dat"):
            table_name = ''.join([i for i in path.splitext(file)[0] if not i.isdigit()]).rstrip('_')
            p.apply_async(load_files, [table_name, file])
    p.close()
    p.join()

    load_end_time = time.time()  # Timestamp for the ending time
    load_time = load_end_time - load_start_time  # Measured load time
    output = f'LOAD TIME:\n\tLoad start time = {load_start_time}\n\tLoad end time = {load_end_time}\n\tLoad time = {load_time}\n'
    print(output)

    if args.outputfile is not None:
        with open(args.outputfile, 'w+') as f:
            f.write(output)
