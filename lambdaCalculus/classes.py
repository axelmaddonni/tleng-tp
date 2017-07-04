#! coding: utf-8

import traceback

### Definimos las clases para los tipos de términos ###

class Expression(object):
  def bindType(self, varName, varType):
    return self

  def bindValue(self, varName, varValue):
    return self

class Nat(Expression):
  def __init__(self, n):
    self._value = n

  def __repr__(self):
    return str(self._value)

  def value(self):
    return self
  
  def type(self):
    return Type(['Nat'])

  def suc(self):
    return Nat(self._value + 1)

  def pred(self):
    if self._value > 0:
      return Nat(self._value - 1)
    else:
      return Nat(0)

  def isZero(self):
    return Bool(self._value == 0)

class Bool(Expression):
  def __init__(self, b):
    self._value = b

  def __repr__(self):
    if self._value:
      return 'true'
    else:
      return 'false'

  def value(self):
    return self

  def type(self):
    return Type(['Bool'])

  def isTrue(self):
    if self._value:
      return True
    else:
      return False

class IfThenElse(Expression):
  def __init__(self, cond, ifTrue, ifFalse):
    self._cond = cond
    self._ifTrue = ifTrue
    self._ifFalse = ifFalse

  def __repr__(self):
    return 'if ' + str(self._cond) + ' then ' + str(self._ifTrue) + ' else ' + str(self._ifFalse)

  def value(self):
    if (not (self._ifTrue.type() == self._ifFalse.type())):
      print 'ERROR: Las dos opciones del if deben tener el mismo tipo'
      traceback.print_stack()
      exit()
    if (not (self._cond.type().typesArray() == ['Bool'])):
      print 'ERROR: La condicion del if debe ser de tipo Bool'
      traceback.print_stack()
      exit()
    if (self._cond.value().isTrue()):
      return self._ifTrue.value()
    else:
      return self._ifFalse.value()

  def type(self):
    if (not (self._ifTrue.type() == self._ifFalse.type())):
      print 'ERROR: Las dos opciones del if deben tener el mismo tipo'
      traceback.print_stack()
      exit()
    if (not (self._cond.type().typesArray() == ['Bool'])):
      print 'ERROR: La condicion del if debe ser de tipo Bool'
      traceback.print_stack()
      exit()
    return self._ifTrue.type()

  def bindValue(self, varName, value):
    self._cond = self._cond.bindValue(varName, value)
    self._ifTrue = self._ifTrue.bindValue(varName, value)
    self._ifFalse = self._ifFalse.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._cond = self._cond.bindType(varName, valueType)
    self._ifTrue = self._ifTrue.bindType(varName, valueType)
    self._ifFalse = self._ifFalse.bindType(varName, valueType)
    return self

class Var(Expression):
  def __init__(self, name):
    self._name  = name
    self._value = None
    self._type  = None

  def __repr__(self):
    return self._name

  def value(self):
    if self._value is not None:
      return self._value.value()
    else:
      print('ERROR: El término no es cerrado (' + self._name + ' está libre))')
      traceback.print_stack()
      exit()

  def type(self):
    if self._type is not None:
      return self._type
    else:
      print('ERROR: El término no es cerrado (' + self._name + ' está libre))')
      traceback.print_stack()
      exit()

  def bindValue(self, varName, value):
    if (str(self._name) == str(varName)):
      self._value = value
      self._type = value.type()
    return self

  def bindType(self, varName, valueType):
    if (str(self._name) == str(varName)):
      self._type = valueType
    return self

class Abstraction(Expression):
  def __init__(self, varname, vartype, body):
    self._var = varname
    self._type = Type([str(vartype)])
    self._body = body
    self._body.bindType(varname, self._type)

  def __repr__(self):
    return '\\' + str(self._var) + ':' + str(self._type) + '.' + str(self._body)

  def paramName(self):
    return self._var

  def paramType(self):
    return self._type

  def bodyType(self):
    return self._body.type()

  def apply(self, value):
    self._body.bindValue(self._var, value)
    return self._body.value()

  def type(self):
    return Type([self.paramType().typesArray(), self.bodyType().typesArray()])

  def value(self):
    return self

  def bindValue(self, varName, value):
    self._body = self._body.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._body = self._body.bindType(varName, valueType)
    return self

class Application:
  def __init__(self, absTerm, paramTerm):
    self._absTerm = absTerm
    self._paramTerm = paramTerm

  def value(self):
    if (isinstance(self._absTerm, Abstraction) and self._paramTerm.type() == self._absTerm.paramType()):
      return self._absTerm.apply(self._paramTerm)
    else:
      print 'ERROR: La parte izquierda de la aplicación (' + str(self._absTerm.value()) + ') no es una función con dominio en ' + str(self._paramTerm.type())
      traceback.print_stack()
      exit()

  def type(self):
    return self._absTerm.type().applyType(self._paramTerm.type())

# Problema: no esta definido el body del absTerm, pero queremos saber el tipo de la aplicacion
# Tenemos en el contexto el tipo de la abstraccion y el tipo del parametro y hay que calcular el tipo de la app

  def bindValue(self, varName, value):
    self._absTerm = self._absTerm.bindValue(varName, value)
    self._paramTerm = self._paramTerm.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._absTerm = self._absTerm.bindType(varName, valueType)
    self._paramTerm = self._paramTerm.bindType(varName, valueType)
    return self

class Suc(Expression):
  def __init__(self, exp):
    self._exp = exp

  def __repr__(self):
    return 'succ(' + str(self._exp) + ')'

  def value(self):
    if (not (self._exp.type().typesArray() == ['Nat'])):
      print ('ERROR succ espera un valor de tipo Nat')
      traceback.print_stack()
      exit()
    return self._exp.value().suc()

  def type(self):
    if (not (self._exp.type().typesArray() == ['Nat'])):
      print ('ERROR succ espera un valor de tipo Nat')
      traceback.print_stack()
      exit()
    return Type(['Nat'])

  def bindValue(self, varName, value):
    self._exp = self._exp.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._exp = self._exp.bindType(varName, valueType)
    return self

class Pred(Expression):
  def __init__(self, exp):
    self._exp = exp

  def __repr__(self):
    return 'pred(' + str(self._exp) + ')'

  def value(self):
    if (not (self._exp.type().typesArray() == ['Nat'])):
      print ('ERROR pred espera un valor de tipo Nat')
      traceback.print_stack()
      exit()
    return self._exp.value().pred()

  def type(self):
    if (not (self._exp.type().typesArray() == ['Nat'])):
      print ('ERROR pred espera un valor de tipo Nat')
      traceback.print_stack()
      exit()
    return Type(['Nat'])

  def bindValue(self, varName, value):
    self._exp = self._exp.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._exp = self._exp.bindType(varName, valueType)
    return self

class isZero(Expression):
  def __init__(self, exp):
    self._exp = exp

  def value(self):
    return Nat(self._exp.value()).isZero()

  def type(self):
    if (self._exp.type().typesArray() == ['Nat']):
      return Type(['Bool'])
    else:
      print ('ERROR isZero(x) x debe ser de tipo Nat')
      traceback.print_stack()
      exit()

  def bindValue(self, varName, value):
    self._exp = self._exp.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._exp = self._exp.bindType(varName, valueType)
    return self

class Type:
  def __init__(self, typesArray):
    self._typesArray = []
    for aType in typesArray:
      if (isinstance(aType, list) and len(aType) == 1):
        aType = aType.pop(0)
      self._typesArray.append(aType)

  def __repr__(self):
    if (len(self.typesArray()) > 1):
      return "->".join(map(str, self._typesArray))
    else:
      return str(self.typesArray().pop(0))

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self._typesArray == other._typesArray
    return False

  def typesArray(self):
    return self._typesArray

  def applyType(self, paramType):
    if (len(self.typesArray()) <= len(paramType.typesArray())):
      print ('ERROR no se puede aplicar para estos parametros')
      traceback.print_stack()
      exit()
    for otherType in paramType.typesArray():
      myType = self._typesArray.pop(0)
      if (myType != otherType):
        print ('ERROR no se puede aplicar para estos parametros')
        traceback.print_stack()
        exit()
    return self._typesArray

# TODO Corregir clase Type
