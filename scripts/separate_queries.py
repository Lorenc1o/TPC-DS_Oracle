import re
import os
import argparse

parser = argparse.ArgumentParser(description='Separting query_0.sql into separate files')
parser.add_argument(
    '-D', '--directory', help='Directory where query_0.sql is stored', required=True)
# e.g. "/home/syusupov/Desktop/TPC-DS/test_queries"
parser.add_argument(
    '-F', '--filename', help='name of the sql file', required=False, 
    default="query_0.sql")

args = parser.parse_args()

if not args.directory:
    parser.print_help()
    exit(1)

read_path = os.path.join(args.directory, args.filename)

with open(read_path, "r") as f:
    lines_to_read = f.readlines()
    lines_to_write = []
    for line in lines_to_read:
        lines_to_write.append(line)
        if "-- start query " in line:
            query_n = re.search(r'\d+', line).group()
            query_filename = "query_"+str(query_n)+".sql"
            query_path = os.path.join(args.directory, query_filename)

        elif "-- end query " in line:
            with open(query_path, "w") as query_f:
                query_f.writelines(lines_to_write)
                lines_to_write = []