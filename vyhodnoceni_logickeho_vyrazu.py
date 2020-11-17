import sys
pin = {1: 1, 2: 0, 23: 1}
#src = "$1an$23"
src = input("> ")
instree = []
lssrc = list(src)
i = 0


def solve_expression(instree, treeloc=0):
    val = 0
    hval = 0
    if instree[treeloc+1] == "and":
        hval = pin[int(instree[treeloc])] + pin[int(instree[treeloc+2])]
        if hval == 2:
            val = 1

    if instree[treeloc+1] == "or":
        hval = pin[int(instree[treeloc])] + pin[int(instree[treeloc + 2])]
        if hval != 0:
            val = 1

    return val


while i < len(lssrc):
    #print(i)
    #print(lssrc[i])
    pindigit = 2
    if lssrc[i] == "$":
        try:
            int(lssrc[i+1])
        except:
            print("syn err on pos " + str(i+1))
            sys.exit()
        else:
            try:
                int(lssrc[i+2])
            except:
                pindigit = 1

        if pindigit == 1:
            instree.append(lssrc[i+1])
            i=i+1
        else:
            instree.append(lssrc[i+1] + lssrc[i+2])
            i=i+2

    elif lssrc[i] == "a":
        if lssrc[i+1] != "n":
            print("syn err on pos " + str(i+1))
            sys.exit()
        else:
            instree.append("and")
            i = i+1

    elif lssrc[i] == "o":
        if lssrc[i+1] != "r":
            print("syn err on pos " + str(i+1))
            sys.exit()
        else:
            instree.append("or")
            i = i+1
    else:
        print("syn err on pos " + str(i))
        sys.exit()
    i = i+1

print(instree)

print(solve_expression(instree))
