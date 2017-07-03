"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens

# precedence = [
#   #(tipoDeAsociatividad, ordenDePrecedencia)
#   ('left', 'MINUS'),
#   ('left', 'PLUS'),
#   ('left', 'TIMES'),
#   ('right', 'UMINUS'),
# ]

def p_term_base(p):
  '''term : n
          | BOOL
          | VAR '''
  p[0] = p[1]

def p_term_if(p):
  '''term : IF term THEN term ELSE term '''
  if p[2].type() == 'Bool' and p[4].type() == p[6].type():
    p[0] = p[2].ifThenElse(p[4], p[6])
  else:
    print("Error en un if. Los valores son p[2]:", p[2], "p[4]:", p[4], "p[6]:", p[6])
    parser.restart()

def p_term_abs(p):
  '''term : VAR ':' type '.' term '''
  p[0] = Abstraction(p[1], p[3], p[5])


def p_type(p):
  '''type : TBOOL
          | TNAT 
          | type TO type 
          | '(' type TO type ')' '''
  p[0] = p[1]

def p_n_num(p):
  'n : NUM'
  p[0] = p[1]

def p_n_unary(p):
  '''n : SUC '(' term ')'
       | PRED '(' term ')' '''
  if p[3].type() == 'Nat':
    if p[1] == 'suc':
      p[3].suc()
    else:
      p[3].pred()
    p[0] = p[3]
  else:
    print("El argumento debe ser de tipo Nat.")
    parser.restart()

def p_error(p):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)