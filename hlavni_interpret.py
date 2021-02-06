import sys
from Data import *
from provedeni_statementu import execute


def splice_to_statements(source_code_list):
    #seka z puvodniho stringu jednotlve statementy
    line = ""
    lines = []
    i = 0
    while i < len(source_code_list):

        if source_code_list[i] == ";":
            lines.append(line)
            line = ""
            if i+1 < len(source_code_list):
                if source_code_list[i+1] == " ":
                    source_code_list.pop(i+1)
        elif source_code_list[i] == "{":
            lines.append(line)
            line = ""
            lines.append("{")
        elif source_code_list[i] == "}":
            if line != "":
                lines.append(line)
            line = ""
            lines.append("}")
        else:
            line = line + source_code_list[i]

        i = i + 1

    return lines


def create_statement(line):
    #tvori statement typu 'COMMAND EXPRESION' a kontroluje jestli dava smysl
    line_list = list(line)
    statement = ""
    word = ""

    if line_list[0] == "{":
        statement = "{"
    elif line_list[0] == "}":
        statement = "}"
    else:

        for i in range(0, len(line_list)):

            if line_list[i] == " ":

                if word not in commands:
                    print("syntax err")
                    sys.exit()
                else:
                    a = ""
                    statement = word + " " + a.join(line_list[i+1:len(line_list)])
                    break

            elif line_list[i] == "=":
                a = ""
                word2 = a.join(line_list[i+1:len(line_list)])
                statement = "assign " + word + "~" + word2
                break


            else:
                word = word + line_list[i]

    return statement


def splice_statements(statements):
    statement_list = []

    for i in range(0, len(statements)):
        statement_list.append(create_statement(statements[i]))

    return statement_list

# tri funkce vys nahradit flex/ylecc


def assemble_tree(spliced_statements, beg, end):
    tree = []
    bracket_list = []

    for i in range(beg, end):
        if spliced_statements[i] == "{":
            bracket_list.append(i)

        elif spliced_statements[i] == "}":
            if len(bracket_list) > 1:
                bracket_list.pop(-1)
            elif len(bracket_list) == 1:
                tree.append(assemble_tree(spliced_statements, bracket_list[0]+1, i))
                bracket_list.pop(-1)

        else:
            if len(bracket_list) == 0:
                tree.append(spliced_statements[i])

    return tree


def parse_input():
    source_code = input("> ")
    source_code_list = list(source_code)

    line_list = splice_to_statements(source_code_list)

    spliced_statements = splice_statements(line_list)

    statement_list = assemble_tree(spliced_statements, 0, len(spliced_statements))
    return statement_list






if __name__ == "__main__":
    statement_list = parse_input()
    execute(statement_list)
