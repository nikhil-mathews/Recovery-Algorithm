
import inspect
"""
This gives the undo and redo processes based on recovery algorithm in Database System Concepts textbook. The input is transaction log.txt
"""

def transaction_in(line):
    if line[1] != 'T':
        print("Error: Function ("+inspect.currentframe().f_code.co_name+") can only handle lines starting with T")
        exit()
    return line[1:3]

def transactions_in_checkpoint(line):
    if line[1] != 'C':
        print("Error: Function ("+inspect.currentframe().f_code.co_name+") can only handle lines starting with C")
        exit()
    r = line[line.find("{")+1:line.find("}")]
    r="".join(r.split())
    return r.split(',')

def data_item(line):
    if line.count(',')<2:
        return None
    line = line[line.find(',') + 1:]
    line = line[:line.find(',')]
    line = "".join(line.split())
    return line

def first_value(line):
    if data_item(line) is None:
        return None
    line = line[line.find(data_item(line)) + 2:]
    v=line.find(',')
    if v==-1:
        line = line[:line.find('>')]
    else:
        line = line[:line.find(',')]
    line = "".join(line.split())
    return line

def last_value(line):
    if data_item(line) is None:
        return None
    line = line[line.rfind(',')+1:line.rfind('>')]
    line = "".join(line.split())
    return line

def bottom_up_search(lines,s,start=None,end=0):      #searches from bottom to return index of line containing string "s".
    if start is None:                               # Note start > end
        start = len(lines) - 1
    while lines[start].find(s) == -1:
        start -= 1
        if end == start:
            return None
    return start

with open("transaction log.txt", "r") as f:
    lines = [line.rstrip() for line in f if line[0] =='<']

for i in range(len(lines)):
    lines[i]=lines[i].upper()


checkpointloc=bottom_up_search(lines,"CHECKPOINT")
L = set(transactions_in_checkpoint(lines[checkpointloc]))

# REDO PHASE
print("**********REDO PHASE************")
for i in range(checkpointloc + 1, len(lines)):
    #print(lines[i])
    if lines[i].find("START")!=-1:
        L.add(transaction_in(lines[i]))
        print("Adding "+transaction_in(lines[i])+" to L")
        print("L: "+str(L))
    elif lines[i].find("COMMIT")!=-1:
        L.remove(transaction_in(lines[i]))
        print("Removing " + transaction_in(lines[i]) + " from L")
        print("L: " + str(L))
    elif lines[i].find("ABORT")!=-1:
        L.remove(transaction_in(lines[i]))
        print("Removing " + transaction_in(lines[i]) + " from L")
        print("L: " + str(L))
    else:
        print("Set "+data_item(lines[i])+" to " +last_value(lines[i]))

# UNDO PHASE
print("\n\n**********UNDO PHASE************")
i=len(lines)-1
log=[]
Lcopy = L.copy()
while 1:
    for t in Lcopy:
        if t not in L:
            continue
        if lines[i].find(t) != -1:
            if lines[i].count(',')>1:
                print("Set "+data_item(lines[i])+" to " +first_value(lines[i]))
                log.append("<"+transaction_in(lines[i])+", "+data_item(lines[i])+", "+first_value(lines[i])+">")

            elif lines[i].find("START") != -1:
                L.remove(transaction_in(lines[i]))
                print("Removing "+(transaction_in(lines[i]))+" from L")
                log.append("<"+transaction_in(lines[i]) + " ABORT>")


            else:
                pass
    if len(L) == 0:
        print("\nUndo Complete")
        print("log is ")
        for i in log:
            print(i)
        exit()

    i-=1
    if i==0:
        print("Start for items in "+ str(L)+ " not found")
        exit()