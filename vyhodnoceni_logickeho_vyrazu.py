import sys
pin = {1: 1, 2: 0, 23: 1}
#src = "$1an($23or$2)"
src = input("> ")
lssrc = list(src)



def solve_expression(instree, treeloc=0):
    val = False
    hval = 0
    if instree[treeloc+1] == "and":
        hval = pin[int(instree[treeloc])] + pin[int(instree[treeloc+2])]
        if hval == 2:
            val = True

    if instree[treeloc+1] == "or":
        hval = pin[int(instree[treeloc])] + pin[int(instree[treeloc + 2])]
        if hval != 0:
            val = True

    return val


def splice_expressioon(lssrc):
    i = 0
    splexp = []

    while i < len(lssrc):
        #print(i)
        #print(lssrc[i])

        if lssrc[i] == "$":
            pindigit = 2
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
                splexp.append(lssrc[i+1])
                i = i+1
            else:
                splexp.append(lssrc[i + 1] + lssrc[i + 2])
                i = i+2

        elif lssrc[i] == "a":
            if lssrc[i+1] != "n":
                print("syn err on pos " + str(i+1))
                sys.exit()
            else:
                splexp.append("and")
                i = i+1

        elif lssrc[i] == "o":
            if lssrc[i+1] != "r":
                print("syn err on pos " + str(i+1))
                sys.exit()
            else:
                splexp.append("or")
                i = i+1
        elif lssrc[i] == "(":
            splexp.append("(")
        elif lssrc[i] == ")":
            splexp.append(")")


        else:
            print("syn err on pos " + str(i))
            sys.exit()

        i = i+1
    return splexp

def assemble_tree(splexp, beg, end):
    tree=[]
    braklist=[]
    for i in range(beg, end):
        if splexp[i] == "(":
            braklist.append(i)
        elif splexp[i] == ")":
            if len(braklist)>1:
                braklist.pop(-1)
            elif len(braklist) == 1:
                tree.append(assemble_tree(splexp, braklist[0]+1, i))
                braklist.pop(-1)
        else:
            if len(braklist)==0:
                tree.append(splexp[i])
    return tree


splexp = splice_expressioon(lssrc)
tree = assemble_tree(splexp, 0, len(splexp))

print(tree)

#print(solve_expression(instree))
