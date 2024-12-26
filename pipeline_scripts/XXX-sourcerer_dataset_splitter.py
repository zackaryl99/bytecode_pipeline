# Copy all functions present in a given CSV list to a specified output folder for the purpose of dividing the inputs for running sorcererCC
# Can also be used to copy .java if the extension is changed (useful for testing tools on the same reduced datasets with uncompilable files removed)

import argparse
import os.path
from tqdm import tqdm
import shutil

# Arg parsing
csv_path = None
opcodes_path = None
output_path = None

argParser = argparse.ArgumentParser()
argParser.add_argument("-c", type=str, help="path CSV")
argParser.add_argument("-i", type=str, help="path to folder containing all opcode sequences")
argParser.add_argument("-o", type=str, help="where to put the copied code fragments")

args = argParser.parse_args()

if args.c != None and os.path.isfile(args.c):
    csv_path = args.c
else:
    print("No path (or invalid path) to CSV provided!")
    exit()

if args.i != None:
    if "/" in args.i and not args.i[-1] == "/":
        opcodes_path = args.i+"/"
    elif "\\" in args.i and not args.i[-1] == "\\":
        opcodes_path = args.i+"\\"
    else:
        opcodes_path = args.i
else:
    print("No path to opcodes provided!")
    exit()

if args.o != None:
    if "/" in args.o and not args.o[-1] == "/":
        output_path = args.o+"/"
    elif "\\" in args.o and not args.o[-1] == "\\":
        output_path = args.o+"\\"
    else:
        output_path = args.o
else:
    print("No path to output provided!")
    exit()

print("Path to CSV: "+csv_path)
print("Path to opcodes: "+opcodes_path)
print("Path to output: "+output_path+"\n\n----------------------------\n\n")

lines = []
funcIDs = {}

# generate unique list of files
with open(csv_path, 'r') as file:
    lines = file.readlines()
for line in lines:
    if not ((line.split(","))[0]).rstrip() in funcIDs:
        funcIDs[((line.split(","))[0]).rstrip()] = 1
    if not (line.split(","))[1] in funcIDs:
        funcIDs[((line.split(","))[1]).rstrip()] = 1

# copy files
print("Copying files...")
for key in tqdm(funcIDs.keys(), ncols=50):
    src = opcodes_path+str(key)+".java"#".opcodes"
    dst = output_path+str(key)+".java"
    try:
        shutil.copyfile(src, dst)
    except:
        print("Failed to copy "+str(src)+"\tcontinuing...")

# done
print(str(len(funcIDs.keys()))+" files copied!")