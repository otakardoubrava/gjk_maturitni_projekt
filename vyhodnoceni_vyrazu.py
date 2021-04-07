"""@package vyhodnoceni_vyrazu.py
Tento modul slouží pro rozhodnutí, zda daný logický výraz platí, nebo neplatí.
Modul tvoří jednotlivé hodnoty odvozením objektu od požadované třídy operátoru nebo operandu. Pokud je hodnot více,
tvoří strom objektů.Každá třída má vlastní metodu EVALUATE.
Závěrečné vyhodnocení probíhá zavoláním metody EVALUATE nejvyššího objektu.
"""

import sys
from Data import *
from GPIO_drive import GPIO_read

"""V následující části jsou deklárovány třídy operátorů a operandů."""

"""Třídy operátorů."""

"""binarni"""


class BinAnd:
    """Binární operace AND.
    Vrací TRUE, pokud oba vstupy jsou též TRUE.

    """
    a_ = True
    b_ = True

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací výsledek operace AND mezi výsledky funkcí EVALUATE členů objektu.
        :return:
        """
        return self.a_.evaluate() and self.b_.evaluate()


class BinOr:
    """Binární operace OR.
    Vrací TRUE, pokud alespoň jeden vstup je TRUE.
    """
    a_ = True
    b_ = True

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací výsledek operace OR mezi výsledky funkcí EVALUATE členů objektu.
        :return:
        """
        return self.a_.evaluate() or self.b_.evaluate()


class Not:
    """ Operace NOT.
    Vrací TRUE pokud vstup je FALSE a naopak.
    """
    a_ = True

    def __init__(self, a):
        """
        Konstruktor. Jako argumenty si bere další objekt.
        :param a:
        """
        self.a_ = a

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací opačnou hodnotu funkce EVALUTE členu.
        :return:
        """
        return not self.a_.evaluate()


class BinXor:
    """ Operace XOR.
    Vrací TRUE pokud pouze jeden vstup je TRUE.
    """
    a_ = True
    b_ = True

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací výsledek operace XOR mezi výsledky funkcí EVALUATE členů objektu.
        :return:
        """
        if self.a_.evaluate() or self.b_.evaluate():

            if self.a_.evaluate() and self.b_.evaluate():
                return False
            else:
                return True


class BinNand:
    """ Operace NAND.
    Je přesným opakem operace AND.
    """
    a_ = True
    b_ = True

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací výsledek operace NAND mezi výsledky funkcí EVALUATE členů objektu.
        :return:
        """
        if self.a_.evaluate() and self.b_.evaluate():
            return False
        else:
            return True


class BinNor:
    """
    Operace NOR.
    Je přesným opakem operace OR.
    """
    a_ = True
    b_ = True

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací výsledek operace NOR mezi výsledky funkcí EVALUATE členů objektu.
        :return:
        """
        if self.a_.evaluate() or self.b_.evaluate():
            return False
        else:
            return True


"""ciselne"""


class Equal:
    """
    rovná se
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vrací výsledek porovnání výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        if self.a_.evaluate() == self.b_.evaluate():
            return True
        else:
            return False


class NotEqual:
    """
    nerovná se
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vrací výsledek porovnání výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        if self.a_.evaluate() == self.b_.evaluate():
            return False
        else:
            return True


class LessThan:
    """
    méně než
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vrací výsledek porovnání výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        if self.a_.evaluate() < self.b_.evaluate():
            return True
        else:
            return False


class GreaterThan:
    """
    více než
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vrací výsledek porovnání výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        if self.a_.evaluate() > self.b_.evaluate():
            return True
        else:
            return False


class LessEqual:
    """
    menší než rovno
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vrací výsledek porovnání výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        if self.a_.evaluate() <= self.b_.evaluate():
            return True
        else:
            return False


class GreaterEqual:
    """
    větší než rovno
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vrací výsledek porovnání výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        if self.a_.evaluate() >= self.b_.evaluate():
            return True
        else:
            return False


class Add:
    """
    sčítání
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací výsledek operace sečtení výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        return self.a_.evaluate() + self.b_.evaluate()


class Subtract:
    """
    odčítaní
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací výsledek operace odečtení výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        return self.a_.evaluate() - self.b_.evaluate()


class Multiply:
    """
    násobení
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací výsledek operace násobení výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        return self.a_.evaluate() * self.b_.evaluate()


class Divide:
    """
    dělění
    """
    a_ = ""
    b_ = ""

    def __init__(self, a, b):
        """
        Konstruktor. Jako argumenty si bere dva další objekty.
        :param a:
        :param b:
        """
        self.a_ = a
        self.b_ = b

    def evaluate(self):
        """
        Vyhodnocení. Funkce vrací výsledek operace dělení výsledků funkcí EVALUATE členů objektu.
        :return:
        """
        return self.a_.evaluate() / self.b_.evaluate()


"""Třídy oprandů."""


class Pin:
    """
    Třída logický pin.
    """
    v_ = 0

    def __init__(self, v):
        """
        jako paremetr si bere číslo požadovaného pinu, kontroluje, zda se opravdu jedná o číslo a jestli
        pin skutečně existuje.
        :param v:
        """
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
        """
        volá funkci GPIO_read z modulu GPIO_drive.py a vrací její výsledek
        :return:
        """

        value = GPIO_read(self.v_)
        return value
       

class Variable:
    """
    třída proměnná
    """
    v_ = ""

    def __init__(self, v):
        """
        jako parametr si bere název proměnné
        :param v:
        """
        self.v_ = v

    def evaluate(self):
        """
        vrací hodnotu odpovídající názvu ze slovníku variable_values obsaženého v modulu Data.py
        jestli proměnná existuje je řešeno již při parsování výrazu
        :return:
        """
        return variable_values[self.v_]


class Constant:
    """
    třída konstanta
    """
    v_ = ""

    def __init__(self, v):
        """
        jako parametr si bere hodnotu číselné konstanty
        :param v:
        """
        self.v_ = int(v)

    def evaluate(self):
        """
        pouze vrací hodnotu parametru
        :return:
        """
        return self.v_


def splice_expression(source, known_characters):
    """
     Dělí vstupní string na jednotlivá slova.
    Slova vrací v poli. Zároveň kontroluje párovost závorek.
    :param source:
    :param known_characters:
    :return spliced_expression:
    """
    source_list = list(source)

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


def check_spliced_expression(spliced_expression, known_characters, operators, varible_names):
    """
    Kontroluje, jestli všechna slova dávají smysl
    :param spliced_expression:
    :param known_characters:
    :param operators:
    :param varible_names:
    :return spliced_expression:
    """
    word = ""
    i = 0

    while i < len(spliced_expression):
        """Tento cyklus kontroluje, jestli dva posobě jdoucí prvky pole nejsou jeden operátor.
         Pokud takové prvky najde, spojí je do jednoho.
         """
        if spliced_expression[i] in known_characters and i + 1 != len(spliced_expression):
            word = spliced_expression[i] + spliced_expression[i + 1]

            if word in operators:
                spliced_expression[i] = word
                spliced_expression.pop(i + 1)

        i = i + 1

    for i in range(0, len(spliced_expression)):
        """Samotná kontrola."""
        if spliced_expression[i] not in operators:

            if "$" not in set(spliced_expression[i]):

                if spliced_expression[i] not in known_characters:

                    if spliced_expression[i] not in variable_names:

                        if "#" not in set(spliced_expression[i]):
                            try:
                                int(spliced_expression[i])
                            except:
                                print("syntax error")
                                sys.exit()

    return spliced_expression


def assemble_tree(spliced_expression, beg, end):
    """
    Hledá závorky patřící k sobě.
    Z prvků mezi nimi tvoří vnořené pole.
    Pokud jsou ve výraze vnořené závorky '(())', funkce se spouští rekurzvně.
    :param spliced_expression:
    :param beg:
    :param end:
    :return tree:
    """
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
    """
    Společně s funkcí compact_object_list sestavuje strom z objektů.
    Tato funkce tvoří základní objekty (GPIO piny, proměnné) a společně s operátory je předává dále.
    Pokud nalezne prioritizovanou operaci, spouští se rekurzivně. Pokud je před vrácením finálnho objektu objektů více,
    než jeden, vyhazuje chybu.
    :param tree:
    :return final_object:
    """
    object_list = []

    for i in range(0, len(tree)):
        operator_test = list(tree[i])

        if type(tree[i]) == list:
            """rekurzivní spuštění"""
            object_list.append(assemble_object_tree(tree[i]))

        elif operator_test[0] == "$":
            """tvorba objektu PIN"""
            if len(operator_test) == 2:
                klass = Pin(operator_test[1])
            elif len(operator_test) > 3:
                print("syntax error")
                sys.exit()
            else:
                klass = Pin(operator_test[1] + operator_test[2])
            object_list.append(klass)

        elif tree[i] in variable_names:
            """tvorba objektu proměnné"""
            klass = Variable(tree[i])
            object_list.append(klass)
        elif tree[i] not in operators:
            if "#" not in set(tree[i]):   #text take konstanta, nutno dodelat
                klass = Constant(tree[i])
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

        sys.exit()

    return final_object


def compact_object_list(object_list):
    """
    Tato funkce tvoří objekty operací a vrací je funkci assemble_object_tree
    :param object_list:
    :return klass:
    """
    klass = 0

    if "!" in object_list:
        """tvorba objektu negace"""
        position_of_negation = object_list.index("!")
        if position_of_negation + 1 != len(object_list):
            klass = Not(object_list[position_of_negation + 1])
            object_list[position_of_negation] = klass
            object_list.pop(position_of_negation + 1)
            klass = 0

    if len(object_list) == 3 and "!" not in object_list:
        """tvorba objektů binárních a číselných operátorů"""

        # binarni

        if object_list[1] == "&":
            klass = BinAnd(object_list[0], object_list[2])

        elif object_list[1] == "|":
            klass = BinOr(object_list[0], object_list[2])

        elif object_list[1] == "||":
            klass = BinXor(object_list[0], object_list[2])

        elif object_list[1] == "!&":
            klass = BinNand(object_list[0], object_list[2])

        elif object_list[1] == "!|":
            klass = BinNor(object_list[0], object_list[2])

        # ciselne

        elif object_list[1] == "=":
            klass = Equal(object_list[0], object_list[2])

        elif object_list[1] == "!=":
            klass = NotEqual(object_list[0], object_list[2])

        elif object_list[1] == "<":
            klass = LessThan(object_list[0], object_list[2])

        elif object_list[1] == ">":
            klass = GreaterThan(object_list[0], object_list[2])

        elif object_list[1] == "<=":
            klass = LessEqual(object_list[0], object_list[2])

        elif object_list[1] == ">=":
            klass = GreaterEqual(object_list[0], object_list[2])

        elif object_list[1] == "+":
            klass = Add(object_list[0], object_list[2])

        elif object_list[1] == "-":
            klass = Subtract(object_list[0], object_list[2])

        elif object_list[1] == "*":
            klass = Multiply(object_list[0], object_list[2])

        elif object_list[1] == "/":
            klass = Divide(object_list[0], object_list[2])

    return klass


def solve_expression(final_object):
    """
    Funkce volání metody EVALUIATE nejvyššího objektu.
    :param final_object:
    :return final_object.evaluate():
    """
    return final_object.evaluate()


def vyhodnoceni_vyrazu(source):
    """
    Hlavní funkce.
    Spouští ostatní funkce ve správném pořadí.
    :param source:
    :return solve_expression(final_object):
    """
    spliced_expression = splice_expression(source, known_characters)
    spliced_expression = check_spliced_expression(spliced_expression, known_characters, operators, variable_names)
    tree = assemble_tree(spliced_expression, 0, len(spliced_expression))
    final_object = assemble_object_tree(tree)

    return solve_expression(final_object)


if __name__ == '__main__':
    """
    Zabraňuje spuštění modulu při importování do jiného skriptu.
    """
    source = input("> ")
    print(vyhodnoceni_vyrazu(source))
