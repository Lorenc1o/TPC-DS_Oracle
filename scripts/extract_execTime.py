from os import listdir, path, getpid, system
import re
import os
import argparse
import csv
from natsort import natsorted
from datetime import datetime

parser = argparse.ArgumentParser(description='Extracting Execution Time from the Query Outputs')
parser.add_argument('-F', '--filespath', help='UNC path where query output files are located', required=True)
parser.add_argument('-E', '--execfile', help='UNC path where to save the csv file of execution times', required=True)
args = parser.parse_args()

if not args.filespath:
    parser.print_help()
    exit(1)


def extract_exec(file_name):
    read_path = os.path.join(args.filespath, file_name)
    query_n = re.search(r'query\d+', file_name).group()
    query_n = query_n[5:]
    with open(read_path, "r") as f:
        lines_to_read = f.readlines()
        for idx, line in enumerate(lines_to_read):
            if "timing for: " in line:
                break
        exec_time = re.search(r'\d{2}:\d{2}:\d{2}.\d{2}', lines_to_read[idx+1:][0]).group()
        td = datetime.strptime(exec_time, '%H:%M:%S.%f') - datetime(1900,1,1)
        td = td.total_seconds()
        with open(args.execfile, 'a+') as file:
            writer = csv.writer(file)
            writer.writerow([query_n, td])

if __name__ == "__main__":
    with open(args.execfile, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["query_number", "execution_time(seconds)"])

    files = natsorted(listdir(args.filespath))
    for file in files: # sort by query number
        if file.endswith(".txt") and "query" in file:
            extract_exec(file)
