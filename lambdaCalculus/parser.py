# coding=utf-8

"""Parser LALR de lambdaCalc."""
import ply.yacc as yacc
from .lexer import tokens
from classes import *

def p_exp_app(p):
  '''exp : app '''
  p[0] = p[1]

def p_exp_if(p):
  '''exp : IF exp THEN exp ELSE exp '''
  p[0] = IfThenElse(p[2], p[4], p[6])

def p_exp_abs(p):
  '''exp : LAMBDA VAR ':' type '.' exp '''
  p[0] = Abstraction(p[2], p[4], p[6])

def p_app(p):
  '''app : app term '''
  p[0] = Application(p[1], p[2])

def p_app_term(p):
  '''app : term '''
  p[0] = p[1]

def p_term_base(p):
  '''term : nat
          | bool
          | VAR '''
  p[0] = p[1]

def p_nat_zero(p):
  '''nat : ZERO'''
  p[0] = p[1]

def p_nat_suc(p):
  '''nat : SUC '(' exp ')' '''
  p[0] = Suc(p[3])

def p_nat_pred(p):
  '''nat : PRED '(' exp ')' '''
  p[0] = Pred(p[3])

def p_bool(p):
  '''bool : BOOL'''
  p[0] = p[1]

def p_bool_iszero(p):
  '''bool : IS_ZERO '(' exp ')' '''
  p[0] = IsZero(p[3])

def p_term_exp(p):
  '''term : '(' exp ')' '''
  p[0] = p[2]

def p_type_atype(p):
  '''type : atype '''
  p[0] = p[1]

def p_type_to(p):
  '''type : atype TO type '''
  p[0] = Type([p[1].typesArray(), p[3].typesArray()])

def p_atype_base(p):
  '''atype : TBOOL
           | TNAT '''
  p[0] = Type([p[1]])

def p_atype_type(p):
  '''atype : '(' type ')' '''
  p[0] = Type(p[2].typesArray())

def p_error(p):
    sys.stderr.write("Syntax Error. Asegúrese que la cadena se ingresó entre commilas dobles.\n")
    sys.exit(1)

# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)