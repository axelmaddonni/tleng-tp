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
### Definimos tokens literales ###
literals = ['\\', '(', ')', ':', '.']

### Definimos el resto de los tokens ###
tokens = [
  'IF',
  'THEN',
  'ELSE',
  'TO',
  'BOOL',
  'VAR',
  'NUM',
  'SUC',
  'PRED',
  'IS_ZERO',
  'TBOOL',
  'TNAT'
]

t_ignore = ' ' # No estoy seguro de que a futuro podamos seguir ignorando espacios

### Definimos las clases ###
class Nat:
  def __init__(self, n):
    self._value = n

  def __repr__(self):
    return str(self._value) + ':Nat'

  def suc(self):
    self._value = self._value + 1

  def pred(self):
    if self._value != 0:
      self._value = self._value - 1

  def isZero(self):
    return Bool(self._value == 0)

  def value(self):
    return self._value
  
  def type(self):
    return 'Nat'

class Bool:
  def __init__(self, b):
    self._value = b

  def __repr__(self):
    if self._value:
      return 'true:Bool'
    else:
      return 'false:Bool'

  def ifThenElse(self, ifTrue, ifFalse):
    if self._value:
      return ifTrue
    else:
      return ifFalse

  def type(self):
    return 'Bool'

class Var:
  def __init__(self, name):
    self._name = name
    self._value = None
    self._type = None

  def __repr__(self):
    return self._name

  def isFree(self):
    return self._value == None

  def bind(self, value):
    if self.isFree():
      self._value = value
      self._type = value.type()

class Abstraction:
  def __init__(self, varname, vartype, body):
    self._var = varname
    self._type = vartype
    self._body = body

  def __repr__(self):
    return '\\' + self._var + ':' + self._type + '.' + self._body
### Definimos las regex que matchean para cada token. Notar que el orden en que están definidas importa, de lo contrario VAR se comería suc, pred, etc ###
def t_NUM(t):
  r'\d+'
  t.value = Nat(int(t.value))
  return t

def t_SUC(t):
  r'suc'
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
  return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
