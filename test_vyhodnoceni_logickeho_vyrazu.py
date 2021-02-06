import unittest
import os
from vyhodnoceni_logickeho_vyrazu import *


class TestVyhodnoceni(unittest.TestCase):

    def test_splice_expression(self):
        test_file = open(os.getcwd() + "\\interpret_test_cases")
        lines = test_file.read().splitlines()
        for i in range(0, len(lines)):
            a = ""
            line = list(lines[i])
            coma_position = line.index(",")
            test_in = a.join(line[0: coma_position])
            test_out = a.join(line[coma_position+1: len(line)])
            self.assertEqual(str(splice_expression(test_in, known_characters)), test_out, "fail at" + str(i))
        test_file.close()

    def test_check_spliced_expression(self):
        test_file = open(os.getcwd() + "\\test_chck_splice_exp")
        lines = test_file.readlines()
        for i in range(0, len(lines)):
            a = ""
            line = list(lines[i])
            coma_position = line.index(",")
            test_in = a.join(line[0: coma_position])
            test_out = a.join(line[coma_position+1: len(line)])
            self.assertEqual(str(check_spliced_expression(test_in, known_characters, operators, variable_names)), test_out)
        test_file.close()


if __name__ == '__main__':
    unittest.main()
