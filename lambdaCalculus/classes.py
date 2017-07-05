# coding=utf-8

import traceback
import sys

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
    start = ''
    end = ''
    for x in xrange(0,self._value):
      start += 'suc('
      end += ')'
    return start + str(0) + end

  def __eq__(self, other):
    return self._value == other._value

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
    return Bool(self.value() == Nat(0))

  def isFree(self):
    return False

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

  def isFree(self):
    return False

class Suc(Expression):
  def __init__(self, exp):
    self._exp = exp

  def __repr__(self):
    return 'succ(' + str(self._exp) + ')'

  def value(self):
    if (not (self._exp.type().typesArray() == ['Nat'])):
      sys.stderr.write('ERROR succ espera un valor de tipo Nat' + "\n")
      sys.exit(1)
    return self._exp.value().suc()

  def type(self):
    if (not (self._exp.type().typesArray() == ['Nat'])):
      sys.stderr.write('ERROR succ espera un valor de tipo Nat' + "\n")
      sys.exit(1)
    return Type(['Nat'])

  def bindValue(self, varName, value):
    self._exp = self._exp.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._exp = self._exp.bindType(varName, valueType)
    return self

  def isFree(self):
    return self._exp.isFree()

class Pred(Expression):
  def __init__(self, exp):
    self._exp = exp

  def __repr__(self):
    if (self.isFree()):
      return 'pred(' + str(self._exp) + ')'
    else:
      return str(self.value())

  def value(self):
    if (not (self._exp.type().typesArray() == ['Nat'])):
      sys.stderr.write('ERROR pred espera un valor de tipo Nat' + "\n")
      sys.exit(1)
    return self._exp.value().pred()

  def type(self):
    if (not (self._exp.type().typesArray() == ['Nat'])):
      sys.stderr.write('ERROR pred espera un valor de tipo Nat' + "\n")
      sys.exit(1)
    return Type(['Nat'])

  def bindValue(self, varName, value):
    self._exp = self._exp.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._exp = self._exp.bindType(varName, valueType)
    return self

  def isFree(self):
    return self._exp.isFree()

class IsZero(Expression):
  def __init__(self, exp):
    self._exp = exp

  def __repr__(self):
    if (self._exp.isFree()): 
      return 'isZero(' + str(self._exp) + ')'
    else:
      return str(self.value())

  def value(self):
    if (self._exp.type().typesArray() == ['Nat']):
      return self._exp.value().isZero()
    else:
      sys.stderr.write('ERROR isZero espera un valor de tipo Nat' + "\n")
      sys.exit(1)

  def type(self):
    if (self._exp.type().typesArray() == ['Nat']):
      return Type(['Bool'])
    else:
      sys.stderr.write('ERROR isZero espera un valor de tipo Nat' + "\n")
      sys.exit(1)

  def bindValue(self, varName, value):
    self._exp = self._exp.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._exp = self._exp.bindType(varName, valueType)
    return self

  def isFree(self):
    return self._exp.isFree()

class IfThenElse(Expression):
  def __init__(self, cond, ifTrue, ifFalse):
    self._cond = cond
    self._ifTrue = ifTrue
    self._ifFalse = ifFalse

  def __repr__(self):
    if (self._cond.isFree()):
      return 'if ' + str(self._cond) + ' then ' + str(self._ifTrue) + ' else ' + str(self._ifFalse)
    else:
      return str(self.value())

  def value(self):
    if (not (self._ifTrue.type() == self._ifFalse.type())):
      sys.stderr.write('ERROR: Las dos opciones del if deben tener el mismo tipo' + "\n")
      sys.exit(1)
    if (not (self._cond.type().typesArray() == ['Bool'])):
      sys.stderr.write('ERROR: La condicion del if debe ser de tipo Bool' + "\n")
      sys.exit(1)
    if (self._cond.value().isTrue()):
      return self._ifTrue.value()
    else:
      return self._ifFalse.value()

  def type(self):
    if (not (self._ifTrue.type() == self._ifFalse.type())):
      sys.stderr.write('ERROR: Las dos opciones del if deben tener el mismo tipo' + "\n")
      sys.exit(1)
    if (not (self._cond.type().typesArray() == ['Bool'])):
      sys.stderr.write('ERROR: La condicion del if debe ser de tipo Bool' + "\n")
      sys.exit(1)
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

  def isFree(self):
    return self._cond.isFree() or self._ifFalse.isFree() or self._ifTrue.isFree()

class Var(Expression):
  def __init__(self, name):
    self._name  = name
    self._value = None
    self._type  = None

  def __repr__(self):
    if (self.isFree()):
      return self._name
    else:
      return str(self.value())

  def value(self):
    if (self.isFree()):
      sys.stderr.write('ERROR: El término no es cerrado (' + self._name + ' está libre))' + "\n")
      sys.exit(1)
    else:
      return self._value.value()

  def type(self):
    if self._type is not None:
      return self._type
    else:
      sys.stderr.write('ERROR: El término no es cerrado (' + self._name + ' está libre))' + "\n")
      sys.exit(1)

  def bindValue(self, varName, value):
    if (str(self._name) == str(varName)):
      self._value = value
      self._type = value.type()
    return self

  def bindType(self, varName, valueType):
    if (str(self._name) == str(varName)):
      self._type = valueType
    return self

  def isFree(self):
    return self._value is None

class Abstraction(Expression):
  def __init__(self, varname, vartype, body):
    self._var = varname
    self._type = vartype
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

  def isFree(self):
    return True

class Application(Expression):
  def __init__(self, absTerm, paramTerm):
    self._absTerm = absTerm
    self._paramTerm = paramTerm

  def __repr__(self):
    if (self.isFree()):
      return str(self._absTerm) + ' ' + str(self._paramTerm)
    else:
      return str(self.value())

  def value(self):
    absTermValue = self._absTerm.value()
    paramTermValue = self._paramTerm
    if (isinstance(absTermValue, Abstraction) and
      paramTermValue.type() == absTermValue.paramType()):
      return absTermValue.apply(paramTermValue)
    else:
      sys.stderr.write('ERROR: La parte izquierda de la aplicación (' + str(self._absTerm.value()) + ') no es una función con dominio en ' + str(self._paramTerm.type()) + "\n")
      sys.exit(1)

  def type(self):
    return self._absTerm.type().applyType(self._paramTerm.type())

  def bindValue(self, varName, value):
    self._absTerm = self._absTerm.bindValue(varName, value)
    self._paramTerm = self._paramTerm.bindValue(varName, value)
    return self

  def bindType(self, varName, valueType):
    self._absTerm = self._absTerm.bindType(varName, valueType)
    self._paramTerm = self._paramTerm.bindType(varName, valueType)
    return self

  def isFree(self):
    return self._paramTerm.isFree()

class Type:
  def __init__(self, typesArray):
    while (len(typesArray) == 1 and isinstance(typesArray[0], list)):
      typesArray = typesArray[0]
    self._typesArray = []
    for aType in typesArray:
      if (isinstance(aType, list) and len(aType) == 1):
        aType = aType[0]
      self._typesArray.append(aType)

  def __repr__(self):
    if (len(self.typesArray()) > 1):
      return "->".join(map(lambda x:
        '(' + str(Type([x])) + ')' if isinstance(x, list) else str(Type([x]))
        , self._typesArray))
    else:
      elem = self.typesArray()[0]
      return str(elem)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      if (len(self._typesArray) == 1 and isinstance(self._typesArray[0], list)):
        myType = self._typesArray[0]
      else:
        myType = self._typesArray
      if (len(other._typesArray) == 1 and isinstance(other._typesArray[0], list)):
        otherType = other._typesArray[0]
      else:
        otherType = other._typesArray
      return myType == otherType
    return False

  def typesArray(self):
    return self._typesArray

  def applyType(self, paramType):
    if (len(self.typesArray()) == 1 and isinstance(self.typesArray()[0], list)):
      return Type(self.typesArray()[0]).applyType(paramType)

    if (len(paramType.typesArray()) == 1 and isinstance(paramType.typesArray()[0], list)):
      return self.applyType(paramType.typesArray()[0])

    absType = self.typesArray()

    if (absType[0] == paramType.typesArray() and len(absType) > 1):
      return Type(absType[1:len(absType)])

    if (len(absType) <= len(paramType.typesArray())):
      sys.stderr.write('ERROR de tipos en aplicacion, no se puede aplicar un termino de tipo ' + str(self) + ' a otro de tipo ' + str(paramType) + "\n")
      sys.exit(1)

    for i in xrange(0,len(paramType.typesArray())):
      myType = absType[i]
      otherType = paramType.typesArray()[i]
      if (myType != otherType):
        sys.stderr.write('ERROR de tipos en aplicacion, no se puede aplicar un termino de tipo ' + str(self) + ' a otro de tipo ' + str(paramType) + "\n")
        sys.exit(1)
    return Type(absType[len(paramType.typesArray()):len(absType)])