# https://learntutorials.net/fr/python/topic/10510/python-lex-yacc
import ply.yacc as yacc
from ply import lex

tokens = (
    'PLUS',
    'MINUS',
    'TIMES',
    'DIV',
    'LPAREN',
    'RPAREN',
    'FLOAT',
    'NUMBER',
    'MODULO',
    'POWER',
    'FUNCNAME',
    'BAR',
    'FUNCTION'
)

t_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MODULO = r'\%'
t_TIMES = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_POWER = r'\^'
t_BAR = r'\|'
t_FUNCTION = r'FUNCTION'

functions = {}



def t_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_FUNCNAME(t):
    r"""[a-z]+[a-z0-9]*"""
    print(f'FUNCNAME: {t}')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV'),
    ('left', 'FUNCTION', 'FUNCNAME'),
    ('nonassoc', 'UMINUS')
)


def p_split_bar(p):
    'expr : expr BAR expr'
    p[0] = (p[1], p[3])
    print(f'p_split_bar: {list(p)}')


def p_add(p):
    'expr : expr PLUS expr'
    p[0] = p[1] + p[3]


def p_sub(p):
    'expr : expr MINUS expr'
    p[0] = p[1] - p[3]


def p_expr2uminus(p):
    'expr : MINUS expr %prec UMINUS'
    p[0] = - p[2]


def p_mult_div_modulo_power(p):
    '''expr : expr TIMES expr
    | expr DIV expr
    | expr MODULO expr
    | expr POWER expr
    '''

    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    elif p[2] == '^':
        p[0] = p[1] ** p[3]
    else:
        if p[3] == 0:
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')
        p[0] = p[1] / p[3]


def p_expr2POWER(p):
    'expr : POWER'
    p[0] = p[1]


def p_expr2NUM(p):
    'expr : NUMBER'
    p[0] = p[1]


def p_expr2FLOAT(p):
    'expr : FLOAT'
    p[0] = p[1]


def p_parens(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]


def p_def_function(p):
    'expr : FUNCTION FUNCNAME LPAREN expr RPAREN'
    p[0] = functions[p[2]] = p[4]
    print(f'p_def_function: {list(p)}')


def p_call_function(p):
    'expr : FUNCNAME LPAREN RPAREN'
    p[0] = functions[p[1]]
    print(f'p_call_function: {list(p)}')


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()

res = parser.parse("FUNCTION carre(3*5)|carre()")  # the input
print(res)
