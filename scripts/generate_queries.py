from os import listdir, path, getpid, system
import re
import os
import argparse

parser = argparse.ArgumentParser(description='TPC-DS Query Generation Script')
parser.add_argument('-Q', '--qgenpath', help='UNC path where the dsqgen.exe is located', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the query templates are located', required=True)
parser.add_argument('-O', '--outputdir', help='UNC path where the generated queries will be stored', required=True)
args = parser.parse_args()

if not args.filespath or not args.qgenpath or not args.outputdir:
    parser.print_help()
    exit(1)


def generate_query(file_name):
    dsqgen = 'dsqgen /directory %s /input templates.lst /verbose y /qualify y /scale 1 /dialect oracle /output_dir %s /template %s' % (
        args.filespath, args.outputdir, file_name)
    print(dsqgen)
    system(dsqgen)

    read_path = os.path.join(args.outputdir, 'query_0.sql')
    with open(read_path, "r") as f:
        lines_to_read = f.readlines()
        lines_to_write = []
        for line in lines_to_read:
            if "-- start query " in line:
                query_n = re.search(r'query\d+', line).group()
                query_filename = query_n + ".sql"
                query_path = os.path.join(args.outputdir, query_filename)

                # timing and outputing the result
                lines_to_write.append(
                    "WHENEVER SQLERROR EXIT 1\n"
                    "SET LINES 32000\n"
                    "SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF\n"
                    "SET SERVEROUTPUT OFF\n"
                    "\n"
                    f"spool &1\n"
                    "timing start t\n\n"
                )

            elif "-- end query " in line:
                lines_to_write.append(
                    "timing stop\n"
                    "spool off\n"
                    "exit\n"
                )
                with open(query_path, "w") as query_f:
                    query_f.writelines(lines_to_write)
                    lines_to_write = []
            else:
                lines_to_write.append(line)
    os.remove(read_path)


if __name__ == "__main__":
    os.chdir(args.qgenpath)
    for file in listdir(args.filespath):
        if file.endswith(".tpl") and "query" in file:
            generate_query(file)
