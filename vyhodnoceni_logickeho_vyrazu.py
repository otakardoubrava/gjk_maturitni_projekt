import sys
pins = {1: 1, 2: 0, 3: 1, 4: 1}
variables = {"a": 23}
known_characters = {"&", "|", "(", ")", "!"}
operators = {"&&", "||", "!"}


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


class Negate:
    a_ = True

    def __init__(self, a):
        self.a_ = a

    def evaluate(self):
        return not self.a_.evaluate()


class Pin:
    v_ = 0

    def __init__(self, v):
        self.v_ = v
        try:
            int(self.v_)
        except:
            print("type error")
        else:
            self.v_ = int(self.v_)
        if self.v_ > 40:
            print("no such pin")
            sys.exit()

    def evaluate(self):
        if pins[self.v_] == 1:
            return True
        else:
            return False


def splice_expression(source_list, known_characters):
    i = 0
    word = ""
    number_of_brackets = 0
    spliced_expression = []

    while i < len(source_list):
        if source_list[i] in known_characters:
            if source_list[i] == "(":
                spliced_expression.append("(")
                number_of_brackets = number_of_brackets + 1

            elif source_list[i] == ")":
                if number_of_brackets < 1:
                    print("syntax error")
                    sys.exit()

                if word != "":
                    spliced_expression.append(word)
                    word = ""
                spliced_expression.append(")")
                number_of_brackets = number_of_brackets - 1

            else:
                if word != "":
                    spliced_expression.append(word)
                    spliced_expression.append(source_list[i])
                    word = ""
                else:
                    spliced_expression.append(source_list[i])

        else:
            word = word + source_list[i]

        i = i + 1

    if word != "":
        spliced_expression.append(word)

    if number_of_brackets != 0:
        print("err no end to ( " + str(i))
        sys.exit()

    return spliced_expression


def check_spliced_expression(spliced_expression, known_characters, operators, varibles):
    word = ""
    i = 0

    while i < len(spliced_expression):
        if spliced_expression[i] in known_characters:
            word = spliced_expression[i] + spliced_expression[i + 1]

            if word in operators:
                spliced_expression[i] = word
                spliced_expression.pop(i + 1)

        i = i + 1

    for i in range(0, len(spliced_expression)):
        if spliced_expression[i] not in operators:

            if "$" not in set(spliced_expression[i]):
                print("syntax error")
                sys.exit()

    return spliced_expression


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
                klass = Pin(operator_test[1] + operator_test[2])
            object_list.append(klass)

        else:
            object_list.append(tree[i])

        klass = compact_object_list(object_list)

        if klass != 0:
            object_list[0] = klass
            object_list.pop(1)

            if len(object_list) != 1:
                object_list.pop(1)
        print(object_list)

    if len(object_list) == 1:
        final_object = object_list[0]
    else:
        print("Exp err")
        print(object_list)
        sys.exit()

    return final_object


def compact_object_list(object_list):
    klass = 0

    if "!" in object_list:
        position_of_negation = object_list.index("!")
        if position_of_negation + 1 != len(object_list):
            klass = Negate(object_list[position_of_negation + 1])
            object_list[position_of_negation] = klass
            object_list.pop(position_of_negation + 1)

    if len(object_list) == 3 and "!" not in object_list:
        if object_list[1] == "&&":
            klass = BinAnd(object_list[0], object_list[2])
        elif object_list[1] == "||":
            klass = BinOr(object_list[0], object_list[2])

    return klass


def solve_expression(final_object):
    return final_object.evaluate()


def main():
    source = input("> ")
    source_list = list(source)
    spliced_expression = splice_expression(source_list, known_characters)
    spliced_expression = check_spliced_expression(spliced_expression, known_characters, operators, variables)
    print(spliced_expression)
    tree = assemble_tree(spliced_expression, 0, len(spliced_expression))
    final_object = assemble_object_tree(tree)
    print(solve_expression(final_object))


if __name__ == '__main__':
    main()
