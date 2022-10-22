import matplotlib.pyplot as plt
import argparse
import numpy as np
import csv

parser = argparse.ArgumentParser(description='Extracting Execution Time from the Query Outputs')
parser.add_argument('-E', '--timefile', help='UNC path of the csv file of execution times', required=True)
parser.add_argument('-O', '--outputfile', help='UNC path of the jpg file where to save the graph', required=True)
args = parser.parse_args()

if not args.timefile or not args.outputfile:
    parser.print_help()
    exit(1)

# loading the exec times
x=[]
y=[]
with open(args.timefile,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
    next(plots, None) # the header
    
    for row in plots:
        x.append(row[0])
        y.append(float(row[1]))
 
# creating the bar plot
plt.bar(x, y, color ='maroon',
        width = 0.4)
plt.axhline(y=np.mean(y), color='r', linestyle='-')

plt.tight_layout()
plt.xticks(fontsize=4, rotation=90)
plt.xlabel("Query Number")
plt.ylabel("Execution Time (in seconds)")
plt.title("Scale=1 Performance")
plt.savefig(args.outputfile, dpi=500, bbox_inches='tight')