# 2024 Zackary Savoie
# Script to print out the number of .class files in the <func_ID>/ folder of each .jar file in given directory

import zipfile
import os
import re

def show_jar_classes(directory):
    dir_list = os.listdir(directory)
    counts = {}
    for file in dir_list:
        if 'jar' in file:
            func_id = file.split('.')[0]
            counts[func_id] = 0
            zf = zipfile.ZipFile(directory+"/"+file, 'r')
            for zip_path in zf.namelist():
                regexp = re.compile(r'_[0-9]+/Hell')
                if regexp.search(zip_path):
                    counts[func_id] += 1
    more_than_one = 0
    for key in counts:
        print(str(key)+": "+str(counts[key]))
        if counts[key] > 1:
            more_than_one += 1
    
    print("Total: "+str(counts.__len__()))
    print("More than 1: "+str(more_than_one))

show_jar_classes("Stubber/StubFiles")