import sys
pins = {1: 1, 2: 0, 3: 1, 4: 1}
#src = "$1an$4an$3an$2"
src = input("> ")
lssrc = list(src)


class BinAnd:
    a_ = True
    b_ = True

    def __init__(self, a, b):
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        return self.a_.evaluate() and self.b_.evaluate()


class BinOr:
    a_ = True
    b_ = True

    def __init__(self, a, b):
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        return self.a_.evaluate() or self.b_.evaluate()


class Pin:
    v_ = 0

    def __init__(self, v):
        self.v_ = v

    def evaluate(self):
        if pins[self.v_] == 1:
            return True
        else:
            return False


def splice_expression(lssrc):
    i = 0
    number_of_brackets = 0
    splexp = []

    while i < len(lssrc):

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
                splexp.append(lssrc[i] + lssrc[i+1])
                i = i+1
            else:
                splexp.append(lssrc[i] + lssrc[i + 1] + lssrc[i + 2])
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
            number_of_brackets = number_of_brackets + 1

        elif lssrc[i] == ")":
            splexp.append(")")
            number_of_brackets = number_of_brackets - 1

        else:
            print("syn err on pos " + str(i))
            sys.exit()

        i = i+1
    if number_of_brackets != 0:
        print("err no end to ( " + str(i))
        sys.exit()
    return splexp


def assemble_tree(splexp, beg, end):
    tree = []
    braklist = []
    for i in range(beg, end):
        if splexp[i] == "(":
            braklist.append(i)
        elif splexp[i] == ")":
            if len(braklist) > 1:
                braklist.pop(-1)
            elif len(braklist) == 1:
                tree.append(assemble_tree(splexp, braklist[0]+1, i))
                braklist.pop(-1)
        else:
            if len(braklist) == 0:
                tree.append(splexp[i])
    return tree


def assemble_class_tree(tree):
    class_list = []
    for i in range(0, len(tree)):
        optest = list(tree[i])


        if type(tree[i]) == list:
            class_list.append(assemble_class_tree(tree[i]))

        elif optest[0] == "$":
            if len(optest) == 2:
                clss = Pin(int(optest[1]))
            else:
                clss = Pin(int(optest[1]+optest[2]))
            class_list.append(clss)

        else:
            class_list.append(tree[i])

        clss = compact_class_list(class_list)

        if clss != 0:
            class_list[0] = clss
            class_list.pop(1)
            if len(class_list) != 1:
                class_list.pop(1)

    if len(class_list) == 1:
        cl = class_list[0]
    else:
        print("Exp err")
        print(class_list)
        sys.exit()
    return cl


def compact_class_list(class_list):
    clss=0

    if len(class_list) == 2:
        pass
    elif len(class_list) == 3:
        if type(class_list[2]) == "list":
            class_list[2] = assemble_class_tree(class_list[2])
        if class_list[1] == "and":
            clss = BinAnd(class_list[0], class_list[2])
        elif class_list[1] == "or":
            clss = BinOr(class_list[0], class_list[2])
    return clss


def solve_expression(cl):
    return cl.evaluate()


splexp = splice_expression(lssrc)
tree = assemble_tree(splexp, 0, len(splexp))
cl = assemble_class_tree(tree)

print(solve_expression(cl))
