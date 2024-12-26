base = "/mnt/c/876/newSourcererCC/SourcererCC/tokenizers/file-level/linecounting/"

# average total
names = ["T1", "T2", "T3", "T4", "T5"]
total_tokens = 0
total_len = 0
for name in names:
    filename = base+name+"_total"
    lines = []

    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        total_tokens += int(line.rstrip())
    total_len += len(lines)

print("Average total (bytecode): "+str(total_tokens/total_len))


# average total
names = ["s_T1", "s_T2", "s_T3", "s_T4", "s_T5"]
total_tokens = 0
total_len = 0
for name in names:
    filename = base+name+"_total"
    lines = []

    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        total_tokens += int(line.rstrip())
    total_len += len(lines)

print("Average total (sourcecode): "+str(total_tokens/total_len))

# average uniq
names = ["T1", "T2", "T3", "T4", "T5"]
total_tokens = 0
total_len = 0
for name in names:
    filename = base+name+"_uniq"
    lines = []

    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        total_tokens += int(line.rstrip())
    total_len += len(lines)

print("Average uniq (bytecode): "+str(total_tokens/total_len))


# average uniq
names = ["s_T1", "s_T2", "s_T3", "s_T4", "s_T5"]
total_tokens = 0
total_len = 0
for name in names:
    filename = base+name+"_uniq"
    lines = []

    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        total_tokens += int(line.rstrip())
    total_len += len(lines)

print("Average uniq (sourcecode): "+str(total_tokens/total_len))