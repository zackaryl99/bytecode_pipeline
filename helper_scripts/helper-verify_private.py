# 2024 Zackary Savoie
# Script to print out private lines in java source 

import os 

java_path = "Toma/dataset/id2sourcecode/"
log_path = "opcode_extraction_statistics.log"

# # Compile files and extract opcodes
# dir_list = os.listdir(class_path)

raw_lines = []

with open(log_path, 'r') as handle:
    raw_lines = handle.readlines()

for line in raw_lines:
    func_id = line.split(':')[0]
    if "Failed" in line:
        with open(java_path+"/"+str(func_id)+".java", 'r') as handle:
            print(handle.readline())