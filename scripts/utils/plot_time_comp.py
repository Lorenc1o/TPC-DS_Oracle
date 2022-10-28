import matplotlib.pyplot as plt
import argparse
import csv

plt.style.use('ggplot')

parser = argparse.ArgumentParser(description='Extracting Execution Time from the Query Outputs')
parser.add_argument('-B', '--timefile_before', help='UNC path of the csv file of execution times of all queries', required=True)
parser.add_argument('-A', '--timefile_after', help='UNC path of the csv file of execution times of optimized queries', required=True)
parser.add_argument('-O', '--outputfile', help='UNC path of the jpg file where to save the graph', required=True)
args = parser.parse_args()

if not args.timefile_before or not args.timefile_after or not args.outputfile:
    parser.print_help()
    exit(1)

# loading after
x=[]
y_after=[]
with open(args.timefile_after,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
    next(plots, None) # the header
    
    for row in plots:
        if row:
            x.append(row[0])
            y_after.append(float(row[1]))

# getting only the optimized queries from before
with open(args.timefile_before,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
    next(plots, None) # the header
    
    y_before = [0.0]*len(y_after)
    for row in plots:
        if row and row[0] in x:
            idx = x.index(row[0])
            y_before[idx] = float(row[1])

index = list(range(len(x)))
bar_width = 0.35

fig, ax = plt.subplots()
before = ax.bar(index, y_before, bar_width,
                label="Before")

winter = ax.bar([i+bar_width for i in index], y_after,
                 bar_width, label="After")

ax.set_xlabel('Query Numbers')
ax.set_ylabel('Execution Time')
ax.set_title('Optimized Queries, Scale 1')
ax.set_xticks([i+bar_width/2 for i in index])
ax.set_xticklabels(["Q"+q_n for q_n in x])
ax.legend()

# plt.show()
plt.savefig(args.outputfile, dpi=500, bbox_inches='tight')