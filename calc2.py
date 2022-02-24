# -----------------------------------------------------------------------------

# calc.py

#

# A savoir : Une expression ca peut être un nombre, True, False ou une déclaration (a+ 5 ou 2+2)

# Expressions arithmétiques sans variables

# -----------------------------------------------------------------------------



reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'while': 'WHILE',
    'else': 'ELSE',
    'for': 'FOR',
    'fonction': 'FONCTION'
    # print en minuscule reconnu dans calc
}

# Lexique pour grammaire

tokens = [
             'NUMBER', 'MINUS',
             'PLUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN', 'AND', 'OR', 'TRUE', 'FALSE', 'SEMICOLON', 'NAME', 'AFFECT', 'INFTO', 'SUPTO', 'SAME',
             'LACOL', 'RACOL', 'VIRG', 'FUNCNAME'

         ] + list(reserved.values())

# Tokens (ce qui est marqué sur ta console )

t_SEMICOLON = r'\;'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_AND = r'\&'
t_OR = r'\|'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_TRUE = r'T'
t_FALSE = r'F'
t_AFFECT = r'='
t_INFTO = r'\<'
t_SUPTO = r'\>'
t_SAME = r'=='
t_LACOL = r'\{'
t_RACOL = r'\}'
t_VIRG = r','

functions = {'carre':'print(2)'}
names = {}


def t_TYPE(t):
    r"""int | float | void"""


def t_FUNCNAME(t):
    r"""[a-zA-Z_0-9]+"""
    return t

def t_NAME(t):
    r"""_[a-zA-Z_0-9]+ | [a-zA-Z][a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer

import ply.lex as lex

lex.lex()

precedence = (
    ('left', 'AND'),
    ('left', 'OR'),
    ('nonassoc', 'INFTO', 'SUPTO', 'AFFECT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    # ('right','UMINUS'),
)


def p_start(p):
    ' START : BLOC'
    p[0] = ('START', p[1])
    print('Arbre de dérivation = ', p[0])
    evalInst(p[1])


def p_bloc(p):
    """ BLOC : BLOC statement SEMICOLON
    | statement SEMICOLON """
    if len(p) == 4:
        p[0] = ('bloc', p[1], p[2])
    else:
        p[0] = ('bloc', p[1], 'empty')


def p_statement_print(p):
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = ('print', p[3])


def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LACOL BLOC RACOL '
    p[0] = ('while', p[3], p[6])


def p_statement_if(p):
    ''' statement : IF LPAREN expression RPAREN LACOL BLOC RACOL
    | IF LPAREN expression RPAREN LACOL BLOC RACOL ELSE LACOL BLOC RACOL '''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if', p[3], p[6], 'else', p[10])


def p_statement_for(p):
    ''' statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN LACOL BLOC RACOL '''
    p[0] = ('for', p[3], p[5], p[7], p[10])


# def p_multiple_names(p):
#     '''multiname : NAME VIRG multiname
#     | NAME '''
#     if len(p) == 4:
#         p[0] = ('multiname', p[1], p[3])
#     else:
#         p[0] = ('multiname', p[1])


def p_def_function(p):
    'statement : FONCTION NAME LPAREN RPAREN LACOL BLOC RACOL'
    p[0] = ('fonction', p[2], p[6])


def p_call_function(p):
    'statement : FUNCNAME LPAREN RPAREN SEMICOLON'
    p[0] = functions[p[1]]


def p_statement_affect(p):
    'statement : NAME AFFECT expression '
    p[0] = ('assign', p[1], p[3])


def p_expression_binop_plus(p):
    'expression : expression PLUS expression'
    p[0] = ('+', p[1], p[3])


def p_expression_binop_times(p):
    'expression : expression TIMES expression'
    p[0] = ('*', p[1], p[3])


def p_expression_same(p):
    'expression : expression SAME expression'
    p[0] = ('==', p[1], p[3])


def p_expression_binop_divide_and_minus(p):
    '''expression : expression MINUS expression
    | expression DIVIDE expression'''
    if p[2] == '-':
        p[0] = ('-', p[1], p[3])
    else:
        p[0] = ('/', p[1], p[3])



def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_name(p):
    'expression : NAME'
    p[0] = p[1]


def p_expressionTrue(p):
    'expression : TRUE'
    p[0] = True


def p_expressionFalse(p):
    'expression : FALSE'
    p[0] = False


def p_expression_binop_boop(p):
    '''expression : expression AND expression
    | expression OR expression'''
    if p[2] == '&':
        p[0] = ('Expr', p[1], '&', p[3])
    elif p[2] == '|':
        p[0] = ('Expr', p[1], '|', p[3])


def p_expression_inequal(p):
    '''expression : expression INFTO expression
    | expression SUPTO expression '''
    if p[2] == '<':
        p[0] = ('<', p[1], p[3])
    elif p[2] == '>':
        p[0] = ('>', p[1], p[3])



def p_error(p):
    print("Syntax error at '%s'" % p.value)


def eval(t):  # evalExpre
    print(' eval de ', t)
    if type(t) is int:
        return t
    if type(t) is str:
        return names[t]
    if type(t) is tuple:
        if t[0] == '+':
            return eval(t[1]) + eval(t[2])
        elif t[0] == '-':
            return eval(t[1]) - eval(t[2])
        elif t[0] == '*':
            return eval(t[1]) * eval(t[2])
        elif t[0] == '/':
            return eval(t[1]) / eval(t[2])
        elif t[0] == '&':
            return eval(t[1]) & eval(t[2])
        elif t[0] == '|':
            return eval(t[1]) | eval(t[2])
        elif t[0] == '<':
            return eval(t[1]) < eval(t[2])
        elif t[0] == '>':
            return eval(t[1]) > eval(t[2])
        elif t[0] == '==':
            return eval(t[1]) == eval(t[2])


def evalInst(t):
    print(' evalInst de ', t)
    if t == 'empty':
        return
    elif t[0] == 'bloc':
        evalInst(t[1])
        evalInst(t[2])
    elif t[0] == 'assign':
        names[t[1]] = eval(t[2])
    elif t[0] == 'print':
        print('Calc >>', eval(t[1]))

    elif t[0] == 'if':
        if len(t) == 3:
            if eval(t[1]):
                evalInst(t[2])
        else:
            if eval(t[1]):
                evalInst(t[2])
            else:
                evalInst(t[4])

    elif t[0] == 'while':
        while eval(t[1]):
            evalInst(t[2])
            break

    elif t[0] == 'for':
        evalInst(t[1])
        while eval(t[2]):
            evalInst(t[4])
            evalInst(t[3])

    elif t[0] == 'function':
        # T1 = function_name T2 = function
        functions[t[1]] = t[2]


#
# def fibonacci():
#     # s = ' if(0){print(11);x=5;} else {print(10);x=14;};'
#     # s = ' function carre(){print(2);}for(i=0;i<10;i=i+1;){carre();}'
#     s = ' n = 15;'
#     s = s + 'if(n == 0){ a=3;};'
#     s = s + ' f0 = 0; f1 = 1;'
#     s = s + 'while(n>1){temp = f1; f1 = f1+f0; f0 = temp ; n = n-1; }; '
#     s = s + 'print(f1);'
#     return s


import ply.yacc as yacc

yacc.yacc()

""" if else """
# s = ' if(0){print(11);x=5;} else {print(1) ; };'

""" fibonacci """
# s = fibonacci()

""" while """
# s = ' x1 = 0 ; x2 = 1 ; while(1){ x = x1+x2 ; print(x) ; x1 = x2 ; x2 = x ; } ;'

""" for """
#s = ' for(x=0 ; x<3 ; x=x+1) { print(x); } ; '

""" fonction sans param """
#s='fonction carre(){print(2);}for(x=0 ; x<3 ; x=x+1){carre();};'
s=' carre(); '


# s = input('calc > ')
# s = ' eval(tup) ; '


yacc.parse(s)
