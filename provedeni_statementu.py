"""@package provedeni_statementu.py
Modul pro vykonání jednotlivých statementů. Od modulu hlavni_interpret.py přejímá parsovaný vstup. Funkce execute
stále dokola spoušští funkci provedeni_statementu a předává jí jako argument vždy následující statement.
Execute je volána na vnořené seznamy funkcemi cyklů a podmínek.
"""


import sys
import time
from Data import *
from vyhodnoceni_vyrazu import vyhodnoceni_vyrazu
from GPIO_drive import GPIO_write

statement_list = []


def assign_variable(assign_string):
    """
    Funkce pro deklaraci a nastavení proměnné, tedy i GPIIO pinu. Přidá prvek s názvem do množiny
    názvů proměnných variable_names a vztvoří nový prvek slovníku hodnot proměnných variable_values
    pro nastavení GPIO pinu volá funkci GPIO_write a předkládá ji číslo požadovaného pinu.
    :param assign_string:
    """
    a = ""
    name = str(a.join(assign_string[0:assign_string.index("~")]))
    if set(name).isdisjoint(known_characters):
        value = vyhodnoceni_vyrazu(a.join(assign_string[assign_string.index("~")+1:len(assign_string)]))
        if "$" in set(name):
            name = list(name)
            name.pop(0)
            name = a.join(name)
            name = int(name)
            GPIO_write(name, value)
        else:
            variable_names.add(name)
            variable_values[name] = value
    else:
        print("var err")
        sys.exit()


def Print(expression):
    """
    Funkce pro tisk do python konzole, tiskne výsledek předloženého výrazu.
    :param expression:
    """
    print(vyhodnoceni_vyrazu(expression))


def If(statement_list, position, expression):
    """
    Funkce podmínky pokud, zavolá funkci execute na podmíněný kód, pokud je výraz pravdivý
    :param statement_list:
    :param position:
    :param expression:
    """
    if type(statement_list[position+1]) != list:
        print("syntax err")
        sys.exit()
    else:
        if vyhodnoceni_vyrazu(expression):
            execute(statement_list[position + 1])


def While(statement_list, position, expression):
    """
    Cyklus dokud, volá funkci execute na kód uzavřený do tohoto cyklu dokud platí platí výraz
    :param statement_list:
    :param position:
    :param expression:
    """
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


def loop(statement_list, position, expression):
    """
    Cyklus opakuj, volá funkci execute na pořazený kód tolikrát, kolik je hodnota zadaného výrazu. Do výrazu je možné vložit
    proměnnou, do které se ukládá číslo aktuálního opakování (forma: proměnná~čílo) nebo od kterého čísla do kterého
    se má proměnná zapisovat (forma: proměnná~čílo,větší číslo)
    :param statement_list:
    :param position:
    :param expression:
    """
    a = ""
    if type(statement_list[position+1]) != list:
        print("syntax err")
        sys.exit()
    else:
        if "~" in expression:
            expression = list(expression)
            variable_end = expression.index("~")
            variable = a.join(expression[0:variable_end])
            variable_names.add(variable)
            if "," in expression:
                first_end = expression.index(",")
                first = a.join(expression[variable_end+1:first_end])
                last = a.join(expression[first_end+1:len(expression)])

                for i in range(int(first), int(last)):
                    variable_values[variable] = i
                    execute(statement_list[position + 1])
            else:
                last = a.join(expression[variable_end + 1: len(expression)])
                for i in range(0, int(last)):
                    variable_values[variable] = i
                    execute(statement_list[position + 1])
        else:
            for i in range(0, int(expression)):
                execute(statement_list[position+1])


def Break(expression):
    """
    Funkce pro pauzu, jako argumnet si bere počet milisekund, kolik má čekat
    :param expression:
    """
    duration = int(expression)/1000
    time.sleep(duration)



def provedeni_stamentu(statement_list, position):
    """
    zjišťuje jaký je aktuální příkaz a předkládá výraz patřičné funkci
    :param statement_list:
    :param position:
    """
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

    elif command == "lp":
        loop(statement_list, position, expression)

    elif command == "brk":
        Break(expression)




         
def execute(statement_list):
    """
    prochází postupně předložený seznam statementů a předkládá je funkci provedeni_statementu
    :param statement_list:
    """
    i = 0
    while i < len(statement_list):
        if type(statement_list[i]) != list:
            provedeni_stamentu(statement_list, i)
        i = i+1


if __name__ == "__main__":
    provedeni_stamentu(statement_list, 0)

