# 2024 Zackary Savoie
# go through folder of .class files, run javap -c on them, extract opcodes and spit out files containing one opcode per line
# also go through CSVs to remove any invalid functions (0 opcodes, or failed to disassemble completely)

# Sample run command:
# python .\4-disassemble_class_extract_opcodes.py -i .\class_outputs_2\  -o .\extracted_opcodes_2 -c ./Toma\dataset\type-1.csv,./Toma\dataset\type-2.csv,./Toma\dataset\type-3.csv,./Toma\dataset\type-4.csv,./Toma\dataset\type-5.csv,./Toma\dataset\clones.csv,./Toma\dataset\nonclone.csv

import os
import argparse
from pathlib import Path
from tqdm import tqdm
import re

# Arg parsing
class_path = None
output_path = "./extracted_opcodes"
statistics_path = "./4-opcode_extraction_statistics.log"
csv_paths = None

def list_of_strings(arg):
    return arg.split(',')

argParser = argparse.ArgumentParser()
argParser.add_argument("-o", type=str, help="output directory to place <func_id>.opcodes files in")
argParser.add_argument("-i", type=str, help="path to output of class extraction folder (contains all valid .class files to extract opcodes from)")
argParser.add_argument("-l", type=str, help="where to place logs")
argParser.add_argument("-c", type=list_of_strings, help="comma-delimited list of csv files to search and edit")

args = argParser.parse_args()


if args.c != None:
    csv_paths = args.c
    for path in csv_paths:
        if not Path(path).exists():
            raise Exception("Invalid CSV path provided: "+path)
else:
    raise Exception("No path(s) to CSVs provided!")

if args.o != None:
    output_path = args.o
    if not Path(output_path).exists():
            raise Exception("Invalid output path provided: "+output_path)
else:
    print("No output path specified to place extacted opcodes into. Will use "+output_path)
    if not Path(output_path).exists():
         os.mkdir(output_path)

if args.i != None:
    class_path = args.i
    if not Path(class_path).exists():
            raise Exception("Invalid .class folder path provided: "+class_path)
else:
    raise Exception("No path to .class files provided!")

if args.l != None:
    statistics_path = args.l
else:
    print("No output path specified to place statistics file. Will use "+statistics_path)

print("Path to .class files: "+class_path)
print("Output directory: "+output_path)
print("Statistics log file: "+str(statistics_path)+"\n\n----------------------------\n\n")


# Compile files and extract opcodes
dir_list = os.listdir(class_path)

invalid_ids = []
statistics = {}

print("Disassembling and parsing .class files: ")
t = tqdm(dir_list, ncols=120)
for file in t:
    t.set_description("Successful: "+str(len(statistics)-len(invalid_ids))+"\tFailures: "+str(len(invalid_ids))+"\tTotal: "+str(len(statistics)), refresh=True)
    
    # Disassemble
    func_id = file.split('.')[0]
    command = "javap -c "+str(class_path)+"/"+str(file)+" > "+str(output_path)+"/"+str(func_id)+".disassembly" 
    
    # Check success of disassembly
    if not os.system(command) == 0:
        print("Error: "+str(output_path)+"/"+str(func_id)+".disassembly")
        statistics[func_id] = "Failed to disassemble!"
        continue

    # Used to parse output
    raw_lines = []
    opcodes = []
    count = 0

    # Patterns used to detect start and end of opcode section of interest
    pattern1 = re.compile(r"\);$")
    pattern2 = re.compile(r"\s+Code:$")
    pattern3 = re.compile(r"\s+[0-9]+:\s+[a-zA-Z]")

    # Read in 
    with open(str(output_path)+"/"+str(func_id)+".disassembly", 'r') as handle:
            raw_lines = handle.readlines()

    for line in raw_lines:
        # Don't start capturing until we're in the function of this file
        if (re.search(pattern1, line) or re.search(pattern2, line)):
            count += 1
            continue
        
        if count < 4:
            continue

        # Stop if we've hit the end of opcode sequence
        if not re.search(pattern3, line):
            opcodes[-1] = opcodes[-1].strip()
            break

        # Must be in opcodes
        opcodes.append((((line.split(": "))[1]).split())[0]+"\n")

    # Make sure the output actually has opcodes in it. Only write if it does
    if len(opcodes) > 1:
        statistics[func_id] = len(opcodes)

        # Write out opcode sequence
        with open(str(output_path)+"/"+str(func_id)+".opcodes", 'w') as output_file:
            output_file.writelines(opcodes)
    else:
        statistics[func_id] = "Failed to parse!"
        invalid_ids.append(func_id)
    
# Write statistics
with open(statistics_path, 'w') as statistics_file:
    statistics_file.writelines("FUNC_ID : # OF OPCODES\n\n")
    for key in statistics:
        statistics_file.writelines(str(key)+": "+str(statistics[key])+"\n")

# Edit CSVs to remove problemaic func_ids

# Go through each csv and remove lines that refer to removed IDs
csv_dict = {} # Will map [csv file path][ID] -> number of removals of that ID from that CSV
badid_dict = {} # Will map [ID] -> number of removals of that ID across ALL CSVs

print("\nRemoving problematic entries from .csv files ("+str(len(invalid_ids))+" problematic IDs): ")
for csv_of_interest in tqdm(csv_paths, ncols=100):
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
with open(statistics_path, 'w') as file:
        file.writelines("Removals by file:\n"+str(csv_dict))
        file.writelines("\nRemovals by ID:\n"+str(badid_dict))
        count = 0
        for key in badid_dict:
             count += badid_dict[key]
        file.writelines("\nTotal lines removed:\n"+str(count))
