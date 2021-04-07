import unittest
import os
from vyhodnoceni_vyrazu import *





def tested_input(line):
    tsin = ""
    a = list(line)
    end = a.index(",")
    tsinput = a[0:end]
    for i in tsinput:
        tsin = tsin + tsinput[i]

    return tsin

def test_output(line):
    expout = ""
    a = list(line)
    start = a.index(",")
    expectout = a[start:-1]
    for i in expectout:
        expout = expout + expectout[i]

    return expout


def main():
    test_file = open(os.getcwd() + "\\test_cases.txt")
    i = 0
    lines = test_file.readlines()
    while True:
        line = lines[i]
        test_input = tested_input(line)
        test_input = splice_expression(test_input)
        print(test_input)
        expect_output = test_output(line)
        print(expect_output)

        i = i+1



if __name__ == '__main__':
    unittest.main()
