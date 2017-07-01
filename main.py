"""Archivo principal de calculadora."""
from lambdaCalculus import parse

while True:
    try:
        exp_str = raw_input('lambdaCalc> ')
    except EOFError:
        break
    print(parse(exp_str))
