# 2024 Zackary Savoie
# Extract .class from zip file if only one present to subfolder, keeping track of function_ids which fail this test
# Use list of invalid function_ids to update the csvs for clones, nonclones, typeX files

# Sample run command:
# python .\3-extract_valid_class_and_remove_invalid_from_csv.py -o class_outputs_2 -j .\Stubber\StubFiles\ -c .\Toma\dataset\clone.csv,.\Toma\dataset\nonclone.csv,.\Toma\dataset\type-1.csv,.\Toma\dataset\type-2.csv,.\Toma\dataset\type-3.csv,.\Toma\dataset\type-4.csv,.\Toma\dataset\type-5.csv

import zipfile
import os
import re
import argparse
from pathlib import Path
from tqdm import tqdm


# Arg parsing
jar_path = None
output_path = "./extracted_classes"
csv_paths = None
removals_path = "./3-class_extraction_removals.log"

def list_of_strings(arg):
    return arg.split(',')

argParser = argparse.ArgumentParser()
argParser.add_argument("-c", type=list_of_strings, help="comma-delimited list of csv files to search and edit")
argParser.add_argument("-o", type=str, help="output directory to place <func_id>.class files in")
argParser.add_argument("-j", type=str, help="path to output of Stubber (.jar containing path)")
argParser.add_argument("-r", type=str, help="where to place log of removed IDs")

args = argParser.parse_args()

if args.c != None:
    csv_paths = args.c
    for path in csv_paths:
        if not Path(path).exists():
            raise Exception("Invalid CSV path provided: "+path)
else:
    print("No path to CSVs provided; will only extract valid class files.")

if args.o != None:
    output_path = args.o
    if not Path(output_path).exists():
            raise Exception("Invalid output path provided: "+output_path)
else:
    print("No output path specified to place extacted .class files into. Will use "+output_path)
    if not Path(output_path).exists():
         os.mkdir(output_path)

if args.j != None:
    jar_path = args.j
    if not Path(jar_path).exists():
            raise Exception("Invalid .jar path (Stubber output) provided: "+jar_path)
else:
    raise Exception("No path to .jar files (Stubber output) provided!")

if args.r != None:
    removals_path = args.r
else:
    print("No output path specified to place removal statistics log file. Will use "+removals_path)

print("Path to .jar files: "+jar_path)
print("Output directory: "+output_path)
print("CSVs to edit: "+str(csv_paths))
print("Removals log file: "+str(removals_path)+"\n\n----------------------------\n\n")


# Go through each .jar, copy .class file to output if it's a valid class to copy
invalid_ids = []

dir_list = os.listdir(jar_path)
counts = {}
print("Extracting .class files:")
for file in tqdm(dir_list, ncols=160):
    if 'jar' in file:
        func_id = file.split('.')[0]
        counts[func_id] = 0
        zf = zipfile.ZipFile(jar_path+"/"+file, 'r')

        for zip_path in zf.namelist():
            regexp = re.compile(r'_[0-9]+/Hell')
            if regexp.search(zip_path): # if this file in the .jar is _funcID/HelloWorld*.class
                counts[func_id] += 1

        if counts[func_id] > 1: # More than one _funcID/HelloWorld*.class -> anonymous inner classes (must remove these)
            invalid_ids.append(func_id)
        else: # only extract it if it's valid
            fullname = "_"+str(func_id)+"/HelloWorld.class"
            output_file = output_path+"\\"+func_id+".class"
            extracted_path = zf.extract(fullname)
            os.rename(extracted_path, output_file)
            Path("_"+str(func_id)).rmdir()

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
with open(removals_path, 'w') as file:
        file.writelines("Removals by file:\n"+str(csv_dict))
        file.writelines("\nRemovals by ID:\n"+str(badid_dict))
        count = 0
        for key in badid_dict:
             count += badid_dict[key]
        file.writelines("\nTotal lines removed:\n"+str(count))
