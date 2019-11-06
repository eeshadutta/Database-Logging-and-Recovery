import sys
import re

db = {}
end_ckpt_first = False
completed_transactions = []


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: recovery.py <log_file>")
        exit(1)

    lines = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            line = re.sub(" ?(,|\\(|\\)) ?", " \\1 ", line)
            line = re.sub(' +', ' ', line)
            line = line.strip("\n").strip(" ").strip("<").strip(">")
            lines.append(line)

    db_elements = lines[0].split(" ")
    for i in range(0, len(db_elements), 2):
        db[db_elements[i]] = int(db_elements[i+1])

    lines.reverse()
    lines.pop()
    lines.pop()

    for line in lines:
        ins = line.split(" ")
        if ins[0].lower() == 'end':
            end_ckpt_first = True
        elif ins[0].lower() == 'start' and ins[1].lower() == 'ckpt':
            if end_ckpt_first == True:
                break
        else:
            if ins[0].lower() == 'commit':
                completed_transactions.append(ins[1])
            elif ins[0].lower() != 'start':
                if ins[0] not in completed_transactions:
                    var = ins[2]
                    val = ins[4]
                    db[var] = val

    sorted_db = sorted(db)
    num_d = len(sorted_db)
    for i in range(num_d):
        if i == num_d - 1:
            print(sorted_db[i], db[sorted_db[i]], end="")
        else:
            print(sorted_db[i], db[sorted_db[i]], end=" ")
    print()
