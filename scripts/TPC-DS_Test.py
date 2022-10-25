from multiprocessing import Pool, cpu_count
from os import listdir, path, getpid, system
import argparse
import cx_Oracle

parser = argparse.ArgumentParser(description='TPC-DS Testing Script')
parser.add_argument('-S', '--svrinstance', help='Server and Instance Name', required=True)
parser.add_argument('-p', '--port', help='Port Number', required=True)
parser.add_argument('-D', '--db', help='Database Name', required=True)
parser.add_argument('-U', '--username', help='Username', required=True)
parser.add_argument('-P', '--password', help='Authenticating Password', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the data files are located', required=True)
parser.add_argument('-C', '--ctlpath', help='UNC path where the control files are located', required=True)
parser.add_argument('-Q', '--querypath', help='UNC path where the query files are located', required=True)
args = parser.parse_args()

if not args.svrinstance or not args.port or not args.db or not args.username or not args.password or not args.filespath or not args.ctlpath or not args.querypath:
    parser.print_help()
    exit(1)

if __name__ == "__main__":
    dsn_tns = cx_Oracle.makedsn(args.srvinstance, args.port, service_name=args.db) # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
    conn = cx_Oracle.connect(user=args.username, password=args.password, dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

    c = conn.cursor()
    c.execute('select username from dba_users')
    conn.close()