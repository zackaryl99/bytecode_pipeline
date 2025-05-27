# Source code compilation pipeline for use in pre-proessing of code clone datasets to test performance on new input type

Along with this repository, STUBBER, Toma and SourcererCC should be cloned using the following links:

https://github.com/andre-schaefer-94/Stubber
https://github.com/CGCL-codes/Toma
https://github.com/Mondego/SourcererCC

This readme file lays out how to execute the scripts which comprise the compilation pipeline, how to configure and use Toma and SourcererCC and how to evaluate sourcererCC's results.

For a copy of the paper written for this project, please contact me using 19zs51@queensu.ca

## Prepare Data (pipeline)

-First make a copy of the Toma dataset folder in main directory

-Run Script 1 on it to append class definition and replace private/protected with public

-Copy modified dataset into BigCloneBenchFiles folder in Stubber

-Run Stubber using: ./gradlew -Dorg.gradle.java.home=/usr/lib/jvm/java-17-openjdk-amd64 run -PmainClass=Stubber --args="-s -t=20"

-Run Script 2 to remove the files Stubber failed to compile from the CSVs

-Run Script 3 to extract valid .class files from Stubber's outputted .jars and update CSVs

-Run Script 4 to generate opcode lists and update CSVs

-Run Script 5 to generate folders containing the opcodes for a given CSV (clone type)
    -python3 5-sourcerer_dataset_splitter.py -c ./Toma/dataset/type-2.csv -i ./extracted_opcodes_2 -o output_folder_name


## Run SourcererCC

-Edit config.ini in the file-level tokenizer folder

    -supply a list of paths to .zip folder to FILE_projects_list 

        -should be zip of a given CSV's opcodes 

    -Place the four output files in a separate "outputs" folder

    -Configure Language-specific parameters


-Run tokenizer in WSL with "python3 tokenizer.py"


-Make a copy of file stats with 

    -cat outputs/files_tokens/* > blocks.file

    -cp blocks.file ../../clone-detector/input/dataset/blocks.file


-Configure min/max tokens in sourcerer-cc.properties of clone-detector folder

-Configure threshold in runnodes.sh

    -threshold="${3:-8}" controllts threshold and "8" means 80%, "7" 70%, etc.


-Run sourcererCC:

    -"python3 controller.py"

    -if log_init.err indicates build.xml failed to build, change C:\876\newSourcererCC\SourcererCC\clone-detector\build.xml:31 to 1.8 instead of 1.7

    =if log_execute1.err indicates it can't find python, edit C:\876\newSourcererCC\SourcererCC\clone-detector\execute.sh:11 to be python3


-Merge results from nodes

    -cat clone-detector/NODE_*/output*/query_* > results.pairs


## Run Toma

-Modify tokenizer script

    -Configure "inputcsv" variable to be path to CSVs

    -Modify "pairs = pd.read_csv(inputcsv, header=None)" in main to include a ", usecols=[0, 1]" option

    -Modify "inputpath" variable in "get_sim" function to point to opcode folder instead of dataset folder

    -Modify "sourcefile1" and "sourcefile2" in "get_sim" function to use ".opcodes" instead of ".java"

    -Remove "logfile.writelines(log)" lines which may cause issues

    -Remove printing of similarity scores from "get_sim" function for speed's sake

    -Include this parser function alongside the similarly named ones:

        def getCodeBlock_bytecode(file_path):  #Z: this will return token sequence from bytecode opcodes. No use of javalang tokenizer
            block = []
            with open(file_path, 'r') as temp_file:
                block = [line.strip() for line in temp_file.readlines()]
            return block

    -Modify reference to "getCodeBlock_type" function in "runner" function to point to newly created "getCodeBlock_bytecode" function instead 

-Run tokenizer script as above for each CSV to get corresponding CSV of similairty scores for each

-Run classifier script


## Evaluate SorcererCC

-Convert from Sourcerer's fileID results to funcID results (same as used in CSVs) using files-stats-0.stats mapping file from Sourcerer's tokenizer's output folder

    -python3 ./XXX-sourcerer_results_to_func_ID_list.py -o converted_results_T2_t7.list -r ./newSourcererCC/SourcererCC/T2_t7_results.pairs -m ./newSourcererCC/SourcererCC/tokenizers/file-level/T2_outputs/files_stats/files-stats-0.stats

-Compute results by comparing funcID results list to ground truth CSV for that clone type

    -python3 XXX-compute_results.py -c Toma/dataset/type-2.csv -r ./newSourcererCC/SourcererCC/converted_results_T2_t7.list
