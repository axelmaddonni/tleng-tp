
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "IF THEN ELSE TO BOOL VAR NUM SUC PRED IS_ZERO TBOOL TNATn : NUMn : SUC '(' n ')' \n       | PRED '(' n ')' b : BOOLterm : n\n          | b term : IF  BOOL  THEN  term  ELSE  term"
    
_lr_action_items = {'$end':([1,2,9,10,],[-1,0,-3,-2,]),'NUM':([0,5,6,],[1,1,1,]),'(':([3,4,],[5,6,]),')':([1,7,8,9,10,],[-1,9,10,-3,-2,]),'PRED':([0,5,6,],[3,3,3,]),'SUC':([0,5,6,],[4,4,4,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'n':([0,5,6,],[2,7,8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> n","S'",1,None,None,None),
  ('n -> NUM','n',1,'p_n_zero','parser.py',17),
  ('n -> SUC ( n )','n',4,'p_n_unary','parser.py',21),
  ('n -> PRED ( n )','n',4,'p_n_unary','parser.py',22),
  ('b -> BOOL','b',1,'p_b_const','parser.py',30),
  ('term -> n','term',1,'p_term_base','parser.py',34),
  ('term -> b','term',1,'p_term_base','parser.py',35),
  ('term -> IF BOOL THEN term ELSE term','term',6,'p_term_bool_if','parser.py',38),
]
