# 2024 Zackary Savoie
# Parse "errorFiles" output of STUBBER to get list of IDs which failed to compile
# Parse dataset CSVs to remove these IDs

#S ample run command:
# python .\2-RemoveFAiledSTUBBERFiles.py -e .\Stubber\errorFiles -c Toma\dataset\type-1.csv,Toma\dataset\type-2.csv,Toma\dataset\type-3.csv,Toma\dataset\type-4.csv,Toma\dataset\type-5.csv,Toma\dataset\clone.csv,Toma\dataset\nonclone.csv

import re
import argparse
from pathlib import Path
from tqdm import tqdm

# Arg parsing
error_path = None
csv_paths = None

def list_of_strings(arg):
    return arg.split(',')

argParser = argparse.ArgumentParser()
argParser.add_argument("-c", type=list_of_strings, help="comma-delimited list of csv files to search and edit")
argParser.add_argument("-e", type=str, help="path to errorFiles ile outputted by Stubber")

args = argParser.parse_args()

if args.c != None:
    csv_paths = args.c
    for path in csv_paths:
        if not Path(path).exists():
            raise Exception("Invalid CSV path provided: "+path)
else:
    print("No path to CSVs provided")
    exit()

if args.e != None:
    error_path = args.e
else:
    print("No path to errorFiles provided")
    exit()

print("errorFiles path: "+error_path)
print("CSVs to edit: "+str(csv_paths)+"\n\n----------------------------\n\n")


# Extract list of failed IDs
invalid_ids = []
with open(error_path, 'r') as file:
    lines = file.readlines()
for line in lines:
    invalid_ids.append((((line.split(','))[1]).split('.'))[0])

# Go through each csv and remove lines that refer to removed IDs
csv_dict = {} # Will map [csv file path][ID] -> number of removals of that ID from that CSV
badid_dict = {} # Will map [ID] -> number of removals of that ID across ALL CSVs

print("Removing entries from .csv files:")
for csv_of_interest in tqdm(csv_paths, ncols=160):
    total_removed_lines = 0
    # print(csv_of_interest+":")
    with open(csv_of_interest, 'r') as file:
        lines = file.readlines()
    csv_dict[csv_of_interest] = {}
    for badid in invalid_ids:
        regexp1 = re.compile(r"," + re.escape(badid) + r",")
        regexp2 = re.compile(r"^" + re.escape(badid) + r",")
        regexp3 = re.compile(r"," + re.escape(badid) + r"$")

        filtered_lines = [line for line in lines if not (re.search(regexp1, line) or re.search(regexp2, line) or re.search(regexp3, line))]
        removed_lines = (len(lines)-len(filtered_lines))

        lines = filtered_lines

        # Accounting 
        total_removed_lines += removed_lines
        csv_dict[csv_of_interest][badid] = removed_lines 

        if not badid in badid_dict:
            badid_dict[badid] = removed_lines
        else:
             badid_dict[badid] += removed_lines

    # Overwrite CSV with entries removed
    with open(csv_of_interest, 'w') as file:
        file.writelines(filtered_lines)

# Write out stats for funcIDs and CSVs
with open("2-stubber_removals.log", 'w') as file:
        file.writelines("Removals by file:\n"+str(csv_dict))
        file.writelines("\nRemovals by ID:\n"+str(badid_dict))
        count = 0
        for key in badid_dict:
             count += badid_dict[key]
        file.writelines("\nTotal lines removed:\n"+str(count))
