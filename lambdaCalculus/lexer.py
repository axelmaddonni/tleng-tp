#! coding: utf-8
import ply.lex as lex

"""
Lista de tokens

El analizador léxico de PLY (al llamar al método lex.lex()) va a buscar
para cada uno de estos tokens una variable "t_TOKEN" en el módulo actual.

Sí, es súper nigromántico pero es lo que hay.

t_TOKEN puede ser:

- Una expresión regular
- Una función cuyo docstring sea una expresión regular (bizarro).

En el segundo caso, podemos hacer algunas cosas "extras", como se
muestra aquí abajo.

"""
reserved = {
  'if': 'IF',
  'then': 'THEN',
  'else': 'ELSE',
  '\\': 'ABS',
  '(' : '(',
  ')' : ')',
  ':': ':',
  '.': '.',
  '->': '->',
  'Bool': 'BOOL',
  'Nat': 'NAT'
}

tokens = (
  'VAR',
  'TRUE',
  'FALSE',
  'ZERO',
  'NUM',
  'SUC',
  'PRED',
  'IS_ZERO'
)

t_SUC = r'suc(.+)'
t_PRED = r'pred(.+)'
t_IS_ZERO = r'isZero(.+)'

def t_VAR(t):
  r'[a-z]'
  return t

def t_TRUE(t):
  r'true'
  t.value = True
  return t

def t_FALSE(t):
  r'false'
  t.value = False
  return t

def t_ZERO(t):
  r'0'
  t.value = 0
  return t

def t_NUM(t):
  r'\d+'
  t.value = int(t.value)
  return t

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
