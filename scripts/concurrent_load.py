from multiprocessing import Pool, cpu_count
from os import listdir, path, getpid, system
import argparse

parser = argparse.ArgumentParser(description='TPC-DS Data Loading Script')
parser.add_argument('-S', '--svrinstance', help='Server and Instance Name', required=True)
parser.add_argument('-D', '--db', help='Database Name', required=True)
parser.add_argument('-U', '--username', help='Username', required=True)
parser.add_argument('-P', '--password', help='Authenticating Password', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the data files are located', required=True)
parser.add_argument('-C', '--ctlpath', help='UNC path where the control files are located', required=True)
args = parser.parse_args()

if not args.svrinstance or not args.db or not args.username or not args.password or not args.filespath or not args.ctlpath:
    parser.print_help()
    exit(1)


def load_files(table_name, file_name):
    print("Loading from CPU: %s" % getpid())
    full_path = path.join(args.filespath, file_name)
    ctl_path = path.join(args.ctlpath, table_name + '.ctl')
    sqlldr = 'sqlldr userid=%s/%s@%s/%s control=%s data=%s' % (
        args.username, args.password, args.svrinstance, args.db, ctl_path, full_path)
    print(sqlldr)
    system(sqlldr)
    print("Done loading data from CPU: %s" % getpid())


if __name__ == "__main__":
    p = Pool(processes=2*cpu_count())
    for file in listdir(args.filespath):
        if file.endswith(".dat"):
            table_name = ''.join([i for i in path.splitext(file)[0] if not i.isdigit()]).rstrip('_')
            p.apply_async(load_files, [table_name, file])
    p.close()
    p.join()