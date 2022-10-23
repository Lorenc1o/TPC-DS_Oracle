from os import listdir, path, getpid, system
import argparse

parser = argparse.ArgumentParser(description='TPC-DS Query Execution Script')
parser.add_argument('-S', '--svrinstance', help='Server and Instance Name', required=True)
parser.add_argument('-D', '--db', help='Database Name', required=True)
parser.add_argument('-U', '--username', help='Username', required=True)
parser.add_argument('-P', '--password', help='Authenticating Password', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the queries are located', required=True)
parser.add_argument('-O', '--outputdir', help='UNC path where the query results will be stored', required=True)
args = parser.parse_args()

if not args.svrinstance or not args.db or not args.username or not args.password or not args.filespath or not args.outputdir:
    parser.print_help()
    exit(1)


def run_query(file_name):
    full_path = path.join(args.filespath, file_name)
    out = path.splitext(file_name)[0] + '.txt'
    out_path = path.join(args.outputdir, out)
    sqlplus = 'sqlplus %s/%s@%s/%s @%s %s' % (
        args.username, args.password, args.svrinstance, args.db, full_path, out_path)
    print(sqlplus)
    system(sqlplus)


if __name__ == "__main__":
    for file in listdir(args.filespath):
        if file.endswith(".sql"):
            run_query(file)
