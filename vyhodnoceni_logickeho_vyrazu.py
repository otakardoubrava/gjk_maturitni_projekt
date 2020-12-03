import sys
pins = {1: 1, 2: 0, 3: 1, 4: 1}
known_characters = {"$", "&", "/", "(", ")"}
operators = {}
integer_operators = {"$"}


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
        self.v_ = int(v)

    def evaluate(self):
        if pins[self.v_] == 1:
            return True
        else:
            return False


def splice_expression(source_list, operators):
    i = 0
    number_of_brackets = 0
    spliced_expression = []

    if source_list[0] not in operators:
        print("syntax error")
        sys.exit()

    while i < len(source_list):
        element = ""
        if source_list[i] in operators:
            if source_list[i] == "(":
                spliced_expression.append("(")
                number_of_brackets = number_of_brackets + 1
            elif source_list[i] == ")":
                spliced_expression.append(")")
                number_of_brackets = number_of_brackets - 1
            else:
                element = element + source_list[i]
                i = i+1
                while i < len(source_list):
                    if source_list[i] in operators:
                        spliced_expression.append(element)
                        i = i - 1
                        break
                    elif i+1 == len(source_list):
                        element = element + source_list[i]
                        spliced_expression.append(element)
                        break
                    else:
                        element = element + source_list[i]
                        i = i + 1

        i = i+1

    if number_of_brackets != 0:
        print("err no end to ( " + str(i))
        sys.exit()
    return spliced_expression


#def check_for_syntax_error():


def assemble_tree(spliced_expression, beg, end):
    tree = []
    bracket_list = []
    for i in range(beg, end):
        if spliced_expression[i] == "(":
            bracket_list.append(i)
        elif spliced_expression[i] == ")":
            if len(bracket_list) > 1:
                bracket_list.pop(-1)
            elif len(bracket_list) == 1:
                tree.append(assemble_tree(spliced_expression, bracket_list[0] + 1, i))
                bracket_list.pop(-1)
        else:
            if len(bracket_list) == 0:
                tree.append(spliced_expression[i])
    return tree


def assemble_object_tree(tree):
    object_list = []
    for i in range(0, len(tree)):
        operator_test = list(tree[i])

        if type(tree[i]) == list:
            object_list.append(assemble_object_tree(tree[i]))

        elif operator_test[0] == "$":
            if len(operator_test) == 2:
                klass = Pin(operator_test[1])
            elif len(operator_test) > 3:
                print("syntax error")
                sys.exit()
            else:
                klass = Pin(operator_test[1]+operator_test[2])
            object_list.append(klass)

        else:
            object_list.append(tree[i])

        klass = compact_object_list(object_list)

        if klass != 0:
            object_list[0] = klass
            object_list.pop(1)
            if len(object_list) != 1:
                object_list.pop(1)

    if len(object_list) == 1:
        final_object = object_list[0]
    else:
        print("Exp err")
        print(object_list)
        sys.exit()
    return final_object


def compact_object_list(object_list):
    klass = 0

    if len(object_list) == 2:
        pass
    elif len(object_list) == 3:
        if object_list[1] == "&":
            klass = BinAnd(object_list[0], object_list[2])
        elif object_list[1] == "/":
            klass = BinOr(object_list[0], object_list[2])
    return klass


def solve_expression(final_object):
    return final_object.evaluate()


def main():
    source = input("> ")
    source_list = list(source)
    spliced_expression = splice_expression(source_list, operators)
    tree = assemble_tree(spliced_expression, 0, len(spliced_expression))
    final_object = assemble_object_tree(tree)

    print(solve_expression(final_object))


if __name__ == '__main__':
    main()
