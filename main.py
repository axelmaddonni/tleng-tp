"""Archivo principal de lambdaCalc."""
from lambdaCalculus import parse

while True:
    try:
        exp_str = raw_input('lambdaCalc> ')
    except EOFError:
        break
    res = parse(exp_str)
    print(str(res.value()) + ':' + str(res.type()))
