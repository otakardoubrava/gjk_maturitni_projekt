import sys
from Data import *
from vyhodnoceni_logickeho_vyrazu import vyhodnoceni_vyrazu

statement_list = []


def assign_variable(assign_string):
    a = ""
    name = str(a.join(assign_string[0:assign_string.index("~")]))
    if set(name).isdisjoint(known_characters):
        value = vyhodnoceni_vyrazu(a.join(assign_string[assign_string.index("~")+1:len(assign_string)]))
        variable_names.add(name)
        variable_values[name] = value
    else:
        print("var err")
        sys.exit()


def Print(expression):
    print(vyhodnoceni_vyrazu(expression))


def If(statement_list, position, expression):
    if type(statement_list[position+1]) != list:
        print("syntax err")
        sys.exit()
    else:
        if vyhodnoceni_vyrazu(expression):
            execute(statement_list[position + 1])


def While(statement_list, position, expression):
    if type(statement_list[position+1]) != list:
        print("syntax err")
        sys.exit()
    else:
        i = position + 1
        while vyhodnoceni_vyrazu(expression):
            execute(statement_list[i])
            i = i+1
            if i == len(statement_list):
                i = position + 1


def provedeni_stamentu(statement_list, position):
    a = ""
    statement = list(statement_list[position])
    command = a.join(statement[0:statement.index(" ")])
    expression = a.join(statement[statement.index(" ")+1:len(statement)])

    if command == "assign":
        assign_variable(expression)
    elif command == "if":
        If(statement_list, position, expression)
    elif command == "whl":
        While(statement_list, position, expression)
    elif command == "pt":
        Print(expression)


def execute(statement_list):
    i = 0
    while i < len(statement_list):
        if type(statement_list[i]) != list:
            provedeni_stamentu(statement_list, i)
        i = i+1



if __name__ == "__main__":
    provedeni_stamentu(statement_list, 0)

