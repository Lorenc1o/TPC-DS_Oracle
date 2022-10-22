import matplotlib.pyplot as plt
import argparse
import csv

parser = argparse.ArgumentParser(description='Extracting Execution Time from the Query Outputs')
parser.add_argument('-E', '--execfile', help='UNC path of the csv file of execution times', required=True)
args = parser.parse_args()

if not args.execfile:
    parser.print_help()
    exit(1)

# loading the exec times
x=[]
y=[]
with open(args.execfile,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
    
    for row in plots:
        x.append(row[0])
        y.append(row[1])
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(x, y, color ='maroon',
        width = 0.4)
 
plt.xlabel("Query Number")
plt.ylabel("Execution Time")
plt.title("Scale=1 Performance")
plt.show()