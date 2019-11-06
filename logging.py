import sys
import re
import itertools

variables = {}
memory = {}
disk = {}


def print_var():
    sorted_memory = sorted(memory)
    sorted_disk = sorted(disk)
    num_m = len(sorted_memory)
    num_d = len(sorted_disk)
    for i in range(num_m):
        if i == num_m - 1:
            print(sorted_memory[i], memory[sorted_memory[i]], end="")
        else:
            print(sorted_memory[i], memory[sorted_memory[i]], end=" ")
    print()
    for i in range(num_d):
        if i == num_d - 1:
            print(sorted_disk[i], disk[sorted_disk[i]], end="")
        else:
            print(sorted_disk[i], disk[sorted_disk[i]], end=" ")
    print()


def process_ins(ins, transaction):
    ins = ins.split(" ")
    if ins[0].lower() == 'read':
        el = ins[2]
        var = ins[4]
        if el not in memory:
            memory[el] = disk[el]
        variables[var] = memory[el]
    elif ins[0].lower() == 'write':
        el = ins[2]
        var = ins[4]
        print("<" + transaction + ", " + el + ", " + str(memory[el]) + ">")
        memory[el] = variables[var]
        print_var()
    elif ins[0].lower() == 'output':
        el = ins[2]
        disk[el] = memory[el]
    else:
        var1 = ins[0]
        var2 = ins[2]
        oper = ins[3]
        val = int(ins[4])
        if oper == '+':
            variables[var1] = variables[var2] + val
        elif oper == '-':
            variables[var1] = variables[var2] - val
        elif oper == '*':
            variables[var1] = variables[var2] * val
        elif oper == '/':
            variables[var1] = variables[var2] / val


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: logging.py <transactions_file> <num_actions>")
        exit(1)

    lines = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            line = re.sub(':=', '=', line)
            line = re.sub(" ?(=|,|\\(|\\)|\\+|\\*|\\-|/) ?", " \\1 ", line)
            line = re.sub(' +', ' ', line)
            line = line.strip("\n").strip(" ")
            lines.append(line)
    x = int(sys.argv[2])

    transactions = []
    for k, group in itertools.groupby(lines, lambda x: x == ''):
        if k == False:
            transactions.append(list(group))
    num_transantions = len(transactions)

    db_elements = transactions[0][0].split(" ")
    for i in range(0, len(db_elements), 2):
        disk[db_elements[i]] = int(db_elements[i+1])
    num_elements = len(disk)

    tdone = 1
    ins_done = [0 for i in range(num_transantions)]
    is_complete = [False for i in range(num_transantions)]
    tname = [None for i in range(num_transantions)]
    num_ins = [0 for i in range(num_transantions)]
    curr_t = 1

    while(True):
        if tdone == num_transantions:
            break
        if is_complete[curr_t]:
            curr_t = ((curr_t + 1) % num_transantions)
            if curr_t == 0:
                curr_t = 1
            continue
        if ins_done[curr_t] == 0:
            line = transactions[curr_t][0].split(" ")
            tname[curr_t] = line[0]
            num_ins[curr_t] = int(line[1])
            print('<START ' + tname[curr_t] + '>')
            print_var()
            ins_done[curr_t] += 1
        for i in range(x):
            ins = transactions[curr_t][ins_done[curr_t]]
            process_ins(ins, tname[curr_t])
            ins_done[curr_t] += 1
            if ins_done[curr_t] > num_ins[curr_t]:
                print('<COMMIT ' + tname[curr_t] + '>')
                print_var()
                is_complete[curr_t] = True
                tdone += 1
                break

        curr_t = ((curr_t + 1) % num_transantions)
        if curr_t == 0:
            curr_t = 1
