# Run from SourcererCC folder!

# steps:
# copy correct blocks.file to clone detector input directory
# configure threshold value in runnodes.sh
# delete existing output in clone-detector folder
# run with detection with: python3 controller.py
# merge results from nodes
# convert from fileid to function id
# write out results

import time
import os
from tqdm import tqdm
import shutil
import re

runs = ["T1", "T2", "T3", "T4", "T5", "s_T1", "s_T2", "s_T3", "s_T4", "s_T5"]
# runs = ["s_T5"]

for run in tqdm(runs, ncols=100):
    print("\n\n=====================================================================\n\n")
    
    block_file = run+"_blocks.file"
    threshold = "{3:-9}"

    shutil.copyfile("./tokenizers/file-level/"+block_file, "./clone-detector/input/dataset/blocks.file")
    print("Copy ./tokenizers/file-level/"+block_file+" to ./clone-detector/input/dataset/blocks.file")
    
    if "s_" in block_file:
        threshold = "{3:-7}"
    
    with open("./clone-detector/runnodes.sh", "r") as file:
        lines = file.readlines()
    with open("./clone-detector/runnodes.sh", "w") as file:
        for line in lines:
            file.write(re.sub(r'\{3:-[0-9]\}', threshold, line))

    try:
        os.remove("clone-detector/Log_backup_gtpm.err")
        os.remove("clone-detector/Log_backup_gtpm.out")
        os.remove("clone-detector/Log_execute_1.err")
        os.remove("clone-detector/Log_execute_1.out")
        os.remove("clone-detector/Log_execute_2.err")
        os.remove("clone-detector/Log_execute_2.out")
        os.remove("clone-detector/Log_index.err")
        os.remove("clone-detector/Log_index.out")
        os.remove("clone-detector/Log_init.err")
        os.remove("clone-detector/Log_init.out")
        os.remove("clone-detector/Log_move_index.err")
        os.remove("clone-detector/Log_move_index.out")
        os.remove("clone-detector/Log_search.err")
        os.remove("clone-detector/Log_search.out")

        os.remove("clone-detector/scriptinator_metadata.scc")
        os.remove("clone-detector/run_metadata.scc")

        shutil.rmtree("clone-detector/SCC_LOGS")
        shutil.rmtree("clone-detector/NODE_1")
        shutil.rmtree("clone-detector/NODE_2")
        shutil.rmtree("clone-detector/index")
        shutil.rmtree("clone-detector/gtpmindex")
        shutil.rmtree("clone-detector/fwdindex")
        shutil.rmtree("clone-detector/dist")
        shutil.rmtree("clone-detector/build")
        shutil.rmtree("clone-detector/backup_gtpm")
        shutil.rmtree("clone-detector/backup_output")
    except:
        print("Failed to delete folders. Continuing.")

    start = time.time()
    command = "cd clone-detector; python3 controller.py" 
    print("Return: "+str(os.system(command)))
    end = time.time()
    print("SourcererCC runtime: "+str(end - start))

    # continue
          
    command = "cat clone-detector/NODE_*/output*/query_* > "+run+"_results.pairs" 
    print("Return: "+str(os.system(command)))

    command = "python3 ../../XXX-sourcerer_results_to_func_ID_list.py -o "+run+"_converted -r "+run+"_results.pairs -m tokenizers/file-level/"+run+"_outputs/files_stats/files-stats-0.stats"
    print("Return: "+str(os.system(command)))

    command = "python3 ../../XXX-compute_results.py -c ../../Toma/dataset/type-"+run[-1]+".csv -r "+run+"_converted -o "+run+"_metrics.txt" 
    print("Return: "+str(os.system(command)))