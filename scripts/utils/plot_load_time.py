import matplotlib.pyplot as plt
import argparse
import numpy as np
import csv
import os
import re

plt.style.use('ggplot')

parser = argparse.ArgumentParser(description='Extracting Execution Time from the Query Outputs')
parser.add_argument('-L', '--loaddir', help='UNC path where load results are (should be scale*_load.txt)', required=True)
parser.add_argument('-O', '--outputfile', help='UNC path of the jpg file where to save the graph', required=True)
args = parser.parse_args()

if not args.loaddir or not args.outputfile:
    parser.print_help()
    exit(1)

# extract the loading times
dirs = os.listdir(args.loaddir)

# This would print all the files and directories
x = []
y = []

for file in dirs:
    if "_load" in file:
        scale_n = re.search('(\d+)_load', file).group()[0]
        x.append(scale_n)
        path = os.path.join(args.loaddir,file)
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "Load time" in line:
                    load_t = float(line.split(" = ")[1])
                    y.append(load_t)
 
# creating the bar plot
bar_list = plt.bar(x, y,
        width = 0.4)

plt.tight_layout()
plt.xlabel("Scale Number")
plt.ylabel("Loading Time (in seconds)")
plt.savefig(args.outputfile, dpi=500, bbox_inches='tight')