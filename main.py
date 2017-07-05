# coding=utf-8

"""Archivo principal de lambdaCalc."""
from lambdaCalculus import parse
import sys

exp_str = ""
if len(sys.argv) == 1:
  exp_str = raw_input('lambdaCalc> ')
elif len(sys.argv) == 2:
  exp_str = sys.argv[1]
else:
  sys.stderr.write("El programa debe recibir a lo sumo una cadena (entre comillas dobles).")
  sys.exit(1)

res = parse(exp_str)
print(str(res.value()) + ':' + str(res.type()))
sys.exit(0)