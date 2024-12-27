# 2024 Zackary Savoie
# Map the file names and numbers in files-stats-#.stats output of SourcererCC to funcID number used in CSVs

import argparse
import os.path

# to deal with windows and linux paths
delimiter = ""

# Arg parsing
mapping_path = None
results_path = None
output_path = None

argParser = argparse.ArgumentParser()
argParser.add_argument("-m", type=str, help="path to files-stats-#.stats output of SorcererCC tokenizer")
argParser.add_argument("-r", type=str, help="path to results.pair output of SorcererCC")
argParser.add_argument("-o", type=str, help="where to put outputted list of clone pairs")

args = argParser.parse_args()

if args.m != None and os.path.isfile(args.m):
    mapping_path = args.m
else:
    print("No path (or invalid path) to files-stats-#.stats file provided")
    exit()

if args.r != None and os.path.isfile(args.r):
    results_path = args.r
else:
    print("No path (or invalid path) to results.pair file provided")
    exit()

if args.o != None:
    output_path = args.o
else:
    print("No path to output provided")
    exit()

print("Path to files-stats-#.stats: "+mapping_path)
print("Output path: "+output_path)
print("Path to results.pair: "+results_path+"\n\n----------------------------\n")

lines = []
results = []
flipped_results = []

# Extract SourcererCC's mapping
mapping = {} # maps file_number -> funcID
with open(mapping_path, 'r') as file:
    lines = file.readlines()
    if "/" in lines[1]:
        delimiter = "/"
    else:
        delimiter = "\\"
for line in lines:
    #1,8,"/mnt/c/876/extracted_opcodes.zip/extracted_opcodes_2/10001403.opcodes",...
    mapping[((line.split(','))[1])] = (((((line.split(','))[2]).split(delimiter))[-1]).split('.'))[0]

#Convert results to funcID results
with open(results_path, 'r') as file:
    lines = file.readlines()
for line in lines:
    # 1,44,1,26
    results.append(str(mapping[(line.split(","))[1]])+","+str(mapping[(line.rstrip().split(","))[3]]))

#Write outputs
file = open(output_path, 'w')
for line in results:
    file.write(line+"\n")

print("Done")