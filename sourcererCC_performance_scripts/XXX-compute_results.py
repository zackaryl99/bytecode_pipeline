# Compute precision, recall and F1 scores given the ground truth CSV for a given clone type and the output of sorcererCC (with fileIDs swapped for funcIDs using provided script)

import argparse
import os.path
from tqdm import tqdm
import shutil

# Arg parsing
csv_path = None
results_path = None
output_path = None

argParser = argparse.ArgumentParser()
argParser.add_argument("-c", type=str, help="path CSV")
argParser.add_argument("-r", type=str, help="path funcID pair results of sorcererCC")
argParser.add_argument("-o", type=str, help="output path")

args = argParser.parse_args()

if args.c != None and os.path.isfile(args.c):
    csv_path = args.c
else:
    print("No path (or invalid path) to CSV provided!")
    exit()

if args.r != None and os.path.isfile(args.r):
    results_path = args.r
else:
    print("No path (or invalid path) to SorcererCC's results provided!")
    exit()

if args.o != None:
    output_path = args.o

print("Path to CSV: "+csv_path)
print("Output path: "+output_path)
print("Path to SorcererCC's results: "+results_path+"\n\n----------------------------\n\n")

# Main
ground_truth_lines = []
results_lines = []

# Metrics
true_positives = 0 # Present in results, present in GT (# lines present in both)
false_positives = 0 # Present in results, not present in GT (# results - # TP)
false_negatives = 0 # Not present in results, present in GT (# GT - # TP)

recall = 0 # TP / (TP + FN)
precision = 0 # TP / (TP + FP)
f1 = 0 # (2 * precision * recall) / (precision + recall)


# Read in ground truth CSV
with open(csv_path, 'r') as file:
    ground_truth_lines = file.readlines()

# [[f1, f2], [f3, f4], ...]
ground_truth_lines = [[line.split(",")[0], line.split(",")[1]] for line in ground_truth_lines]


# Read in results
with open(results_path, 'r') as file:
    results_lines = file.readlines()
results_lines = [line.rstrip() for line in results_lines]


# Lets look for matches using linear search! 
for pair in tqdm(ground_truth_lines, ncols=50):
    if str(pair[0]+","+pair[1]) in results_lines or str(pair[1]+","+pair[0]) in results_lines:
        true_positives += 1

false_positives = len(results_lines) - true_positives 
false_negatives = len(ground_truth_lines) - true_positives

recall = true_positives / (true_positives + false_negatives) 
precision = true_positives / (true_positives + false_positives) 
f1 = (2 * precision * recall) / (precision + recall) 

print("TP: "+str(true_positives))
print("FP: "+str(false_positives))
print("FN: "+str(false_negatives))

print("Recall: "+str(recall))
print("Precision: "+str(precision))
print("F1: "+str(f1))

print("Writing to: "+str(output_path))

file = open(output_path, 'w')
file.write(("TP: "+str(true_positives))+"\n")
file.write(("FP: "+str(false_positives))+"\n")
file.write(("FN: "+str(false_negatives))+"\n")
file.write(("Recall: "+str(recall))+"\n")
file.write(("Precision: "+str(precision))+"\n")
file.write(("F1: "+str(f1))+"\n")

print("Done")