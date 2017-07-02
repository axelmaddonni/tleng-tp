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

### Habria que agregar una produccion nueva de tal
### manera que en ese paso se devuelva el valor + tipo (de ser posible)

def p_n_zero(p):
  'n : NUM'
  p[0] = p[1]

def p_n_unary(p):
  '''n : SUC '(' n ')' 
       | PRED '(' n ')' '''
  if p[1] == 'suc':
    p[3].suc()
  else:
    p[3].pred()
  p[0] = p[3]

def p_b_const(p):
  'b : BOOL'
  p[0] = p[1]

def p_term_base(p):
  '''term : n
          | b '''

def p_term_bool_if(p):
  'term : IF ' ' BOOL ' ' THEN ' ' term ' ' ELSE ' ' term'
  if p[7].type() == p[11].type():
    p[0] = p[3].ifThenElse(p[7], p[11])

# def p_expression_minus(p):
#     'expression : expression MINUS expression'
#     p[0] = p[1] - p[3]

# def p_expression_uminus(p):
#     'expression : MINUS expression %prec UMINUS'
#     p[0] = -p[2]

# def p_expression_times(p):
#     'expression : expression TIMES expression'
#     p[0] = p[1] * p[3]

# def p_expression_number(p):
#     'expression : NUMBER'
#     p[0] = p[1]

def p_error(p):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)