from os import listdir, path, getpid, system
import re
import os
import argparse
import platform

parser = argparse.ArgumentParser(description='TPC-DS Query Generation Script')
parser.add_argument('-Q', '--qgenpath', help='UNC path where the dsqgen.exe is located', required=True)
parser.add_argument('-L', '--filespath', help='UNC path where the query templates are located', required=True)
parser.add_argument('-O', '--outputdir', help='UNC path where the generated queries will be stored', required=True)
parser.add_argument('-S', '--nstreams', help='Number of streams', required=False, default=1)

args = parser.parse_args()

if not args.filespath or not args.qgenpath or not args.outputdir:
    parser.print_help()
    exit(1)

os.chdir(args.qgenpath)
lstpath = path.join(args.filespath, 'templates.lst')
if platform.system() == 'Windows':
    dsqgen = 'dsqgen /directory %s /input %s /verbose y /qualify y /scale 1 /dialect oracle /output_dir %s /streams %s' % (
        args.filespath, lstpath, args.outputdir, args.nstreams)
elif platform.system() == 'Linux':
    dsqgen = './dsqgen -directory %s -input %s -verbose y -qualify y -scale 1 -dialect oracle -output_dir %s -streams %s' % (
        args.filespath, lstpath, args.outputdir, args.nstreams)
else:
    exit(1)
print(dsqgen)
system(dsqgen)

for file in listdir(args.outputdir):
    if file.endswith(".sql"):
        full_path = os.path.join(args.outputdir, file)
        with open(full_path, "r") as f:
            lines_to_read = f.readlines()
            lines_to_write = []
            for line in lines_to_read:
                if "-- start query " in line:
                    query_n = re.search(r'query\d+', line).group()

                    # timing and outputing the result
                    lines_to_write.append(
                        "spool &1\n"
                        f"timing start {query_n}\n\n"
                    )

                elif "-- end query " in line:
                    lines_to_write.append(
                        "timing stop\n"
                        "spool off\n"
                        "-- end\n"
                    )
                else:
                    lines_to_write.append(line)

        with open(full_path, "w") as query_f:
            query_f.writelines(lines_to_write)