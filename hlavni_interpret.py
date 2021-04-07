"""@package hlavni_interpret.py
Hlavní modul celého interpreteru. Parsuje vstupní řetězec jednotlivé statementy, které ukládá postupně do seznamu
(statement_list). Skript dále hledá podmíněné části kódu (části pod podmínkou, nebo
cyklem) a tvoří z nich seznam vnořený do statement_list.
Modul kontroluje jestli statementy dávají smyls.
Konečný sezanm statement_list na konci předává modulu provedeni_statementu.py

"""

import sys
from Data import *
from provedeni_statementu import execute


def splice_to_statements(source_code_list):
    """
    funkce pro parsování vstupního řetězce na statementy
    :param source_code_list:
    :return lines:
    """
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
    """
    funkce pro tvorbu statementu typu 'COMMAND EXPRESION' a kontrolu, jestli statement dává smysl
    pokud statement smysl nedává, vytiskne do konsole 'syntax err' a ukončí skript
    :param line:
    :return statement:
    """
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
    """
    dodatečná funkce pro tvorbu statementů, stále dokola spouští funkci create_statement a předkládá jí další z prvků
    seznamu statementů
    :param statements:
    :return statement_list:
    """
    statement_list = []

    for i in range(0, len(statements)):
        statement_list.append(create_statement(statements[i]))

    return statement_list

# tri funkce vys nahradit flex/ylecc


def assemble_tree(spliced_statements, beg, end):
    """
    Funkce tvoří ze statementů mezi závorkami vnořený seznam, pokud se v kódu vyskytují závorky vnořené,
    funkce se spustí rekurzivně ppouze na vnořený kus kódu.
    :param spliced_statements:
    :param beg:
    :param end:
    :return tree:
    """
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


def parse_input(source_code):
    """
    Stará se o spouštění parsovacích funkcí ve správném pořadí
    vrací konečný seznam příkazů. jako argumnet si bere vstupní řetězec
    :param source_code:
    :return statement_list:
    """
    source_code_list = list(source_code)

    line_list = splice_to_statements(source_code_list)

    spliced_statements = splice_statements(line_list)

    statement_list = assemble_tree(spliced_statements, 0, len(spliced_statements))
    return statement_list


def main(instructions):
    """
    hlavní funkce, předává vstupní řetězec funkci parse_input a výsledný seznam příkazů předává funkci execute z modulu
    provedeni_statementu.py
    :param instructions:
    """
    statement_list = parse_input(instructions)
    execute(statement_list)


if __name__ == "__main__":
    instructions = input("> ")
    main(instructions)
