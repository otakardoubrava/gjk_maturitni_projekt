import unittest
import os
from hlavni_interpret import *


class MyTestCase(unittest.TestCase):
    def test_splice_to_statements(self):
        test_file = open(os.getcwd() + "\\interpret_test_cases")
        lines = test_file.read().splitlines()
        for i in range(0, 10):
            a = ""
            if lines[i] != "":
                line = list(lines[i])
                coma_position = line.index(",")
                test_in = line[0: coma_position]
                test_out = a.join(line[coma_position + 1: len(line)])
                self.assertEqual(str(splice_to_statements(test_in)), test_out, "to st fail at " + str(i))
        test_file.close()


    def test_splice_statements(self):
        test_file = open(os.getcwd() + "\\interpret_test_cases")
        lines = test_file.read().splitlines()
        for i in range(11, 20):
            a = ""
            if lines[i] != "":
                line = lines[i]
                coma_position = line.index(",")
                test_in = line[0: coma_position]
                test_out = a.join(line[coma_position + 1: len(line)])
                self.assertEqual(str(splice_statements(splice_to_statements(test_in))), test_out, "sp st fail at " + str(i))

        test_file.close()

    def test_assemble_tree(self):
        test_file = open(os.getcwd() + "\\interpret_test_cases")
        lines = test_file.read().splitlines()
        for i in range(21, len(lines)):
            a = ""
            if lines[i] != "":
                line = lines[i]
                coma_position = line.index(",")
                test_in = line[0: coma_position]
                test_out = a.join(line[coma_position + 1: len(line)])
                self.assertEqual(str(assemble_tree(splice_statements(splice_to_statements(test_in)), 0, len(splice_statements(splice_to_statements(test_in))))), test_out, "as tr fail at " + str(i))

        test_file.close()


if __name__ == '__main__':
    unittest.main()
