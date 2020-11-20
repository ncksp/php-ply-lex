import ply.lex as lex
import re

states = (
    ('php', 'exclusive'),
)

tokens = (

    'ELSE', 'IF', 'PRINT', 'WHILE',

    'WHITESPACE',

    'OPEN_TAG', 'OPEN_TAG_WITH_ECHO', 'CLOSE_TAG',

    'COMMENT',

    'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'AND', 'OR', 'NOT', 'XOR', 'SL',
    'SR', 'BOOLEAN_AND', 'BOOLEAN_OR', 'BOOLEAN_NOT', 'IS_SMALLER',
    'IS_GREATER', 'IS_SMALLER_OR_EQUAL', 'IS_GREATER_OR_EQUAL', 'IS_EQUAL',
    'IS_NOT_EQUAL', 'IS_IDENTICAL', 'IS_NOT_IDENTICAL',

    'EQUALS', 'MUL_EQUAL', 'DIV_EQUAL', 'MOD_EQUAL', 'PLUS_EQUAL',
    'MINUS_EQUAL', 'SL_EQUAL', 'SR_EQUAL', 'AND_EQUAL', 'OR_EQUAL',
    'XOR_EQUAL', 'CONCAT_EQUAL',

    'INC', 'DEC',

    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'DOLLAR',
    'COMMA', 'CONCAT', 'QUESTION', 'COLON', 'SEMI', 'AT', 'NS_SEPARATOR',

    'INLINE_HTML',

    'STRING', 'VARIABLE',
    'LNUMBER', 'QUOTE',
)

# Newlines
def t_php_WHITESPACE(t):
    r'[ \t\r\n]+'
    t.lexer.lineno += t.value.count("\n")
    return t


# Operators
t_php_PLUS = r'\+'
t_php_MINUS = r'-'
t_php_MUL = r'\*'
t_php_DIV = r'/'
t_php_MOD = r'%'
t_php_AND = r'&'
t_php_OR = r'\|'
t_php_NOT = r'~'
t_php_XOR = r'\^'
t_php_SL = r'<<'
t_php_SR = r'>>'
t_php_BOOLEAN_AND = r'&&'
t_php_BOOLEAN_OR = r'\|\|'
t_php_BOOLEAN_NOT = r'!'
t_php_IS_SMALLER = r'<'
t_php_IS_GREATER = r'>'
t_php_IS_SMALLER_OR_EQUAL = r'<='
t_php_IS_GREATER_OR_EQUAL = r'>='
t_php_IS_EQUAL = r'=='
t_php_IS_NOT_EQUAL = r'(!=(?!=))|(<>)'
t_php_IS_IDENTICAL = r'==='
t_php_IS_NOT_IDENTICAL = r'!=='

# Assignment operators
t_php_EQUALS = r'='
t_php_MUL_EQUAL = r'\*='
t_php_DIV_EQUAL = r'/='
t_php_MOD_EQUAL = r'%='
t_php_PLUS_EQUAL = r'\+='
t_php_MINUS_EQUAL = r'-='
t_php_SL_EQUAL = r'<<='
t_php_SR_EQUAL = r'>>='
t_php_AND_EQUAL = r'&='
t_php_OR_EQUAL = r'\|='
t_php_XOR_EQUAL = r'\^='
t_php_CONCAT_EQUAL = r'\.='


# Delimeters
t_php_LPAREN = r'\('
t_php_RPAREN = r'\)'
t_php_DOLLAR = r'\$'
t_php_COMMA = r','
t_php_CONCAT = r'\.(?!\d|=)'
t_php_QUESTION = r'\?'
t_php_COLON = r':'
t_php_SEMI = r';'
t_php_NS_SEPARATOR = r'\\'
t_php_LBRACKET = '\['
t_php_RBRACKET = '\]'
t_php_LBRACE = '\{'
t_php_RBRACE = '\}'
t_php_QUOTE = '"'

# Comments
def t_php_COMMENT(t):
    r'/\*(.|\n)*?\*/ | //([^?%\n]|[?%](?!>))*\n? | \#([^?%\n]|[?%](?!>))*\n?'
    t.lexer.lineno += t.value.count("\n")
    return t

# Escaping from HTML
def t_OPEN_TAG(t):
    r'<[?%](([Pp][Hh][Pp][ \t\r\n]?)|=)?'
    if '=' in t.value:
        t.type = 'OPEN_TAG_WITH_ECHO'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.begin('php')
    return t


def t_php_CLOSE_TAG(t):
    r'[?%]>\r?\n?'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.begin('INITIAL')
    return t


def t_INLINE_HTML(t):
    r'([^<]|<(?![?%]))+'
    t.lexer.lineno += t.value.count("\n")
    return t

# Identifier
def t_php_STRING(t):
    r'[A-Za-z_][\w_]*'
    return t

# Variable
def t_php_VARIABLE(t):
    r'\$[A-Za-z_][\w_]*'
    return t


# Integer literal
def t_php_LNUMBER(t):
    r'(0b[01]+)|(0x[0-9A-Fa-f]+)|\d+'
    return t

# String literal
def t_php_CONSTANT_ENCAPSED_STRING(t):
    r"'([^\\']|\\(.|\n))*'"
    t.lexer.lineno += t.value.count("\n")
    return t


t_quotedvar_VARIABLE = t_php_VARIABLE


def t_ANY_error(t):
    raise SyntaxError('illegal character', (None, t.lineno, None, t.value))


def peek(lexer):
    try:
        return lexer.lexdata[lexer.lexpos]
    except IndexError:
        return ''

def get_lexer():
    return lex.lex()
