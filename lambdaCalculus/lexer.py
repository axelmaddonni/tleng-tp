#! coding: utf-8
import ply.lex as lex
from classes import *

### Definimos tokens literales ###
literals = ['(', ')', ':', '.']

### Definimos el resto de los tokens ###
tokens = [
  'IF',
  'THEN',
  'ELSE',
  'TO',
  'BOOL',
  'VAR',
  'ZERO',
  'SUC',
  'PRED',
  'IS_ZERO',
  'TBOOL',
  'TNAT',
  'LAMBDA'
]

t_ignore = ' '

def t_ZERO(t):
  r'0'
  t.value = Nat(0)
  return t

def t_SUC(t):
  r'succ'
  return t

def t_PRED(t):
  r'pred'
  return t

def t_BOOL(t):
  r'true|false'
  t.value = Bool(t.value == 'true')
  return t

def t_IS_ZERO(t):
  r'isZero'
  return t

def t_IF(t):
  r'if'
  return t

def t_THEN(t):
  r'then'
  return t

def t_ELSE(t):
  r'else'
  return t

def t_TO(t):
  r'\->'
  return t

def t_TBOOL(t):
  r'Bool'
  return t

def t_TNAT(t):
  r'Nat'
  return t

def t_VAR(t):
  r'[a-z]'
  t.value = Var(t.value)
  return t

def t_LAMBDA(t):
  r'\\'
  return t

# Error handling rule
def t_error(t):
    sys.stderr.write("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
