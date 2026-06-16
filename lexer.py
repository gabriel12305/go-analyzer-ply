import ply.lex as lex

lexical_errors = []
tokens = [ 
    # ===== CARLA GUTIERREZ CONTRIBUTION START =====

    # Identifiers
    'VARIABLE',

    # ===== CARLA GUTIERREZ CONTRIBUTION END =====
    
    # ===== MILENA PAZMIÑO CONTRIBUTION START =====
    'INTEGER',
    'FLOAT',
    'STRING',
     # ===== MILENA PAZMIÑO CONTRIBUTION END =====

    # ===== GABRIEL PELAEZ CONTRIBUTION START =====
    
    # Arithmetic Operators
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    
    # Relational Operators
    'EQ',
    'NE',
    'LT',
    'GT',
    'LE',
    'GE',
    
    # Logical Operators
    'AND',
    'OR',
    'NOT',
    
    # Assignment Operators
    'ASSIGN',
    'DECLARE_ASSIGN',
    'PLUS_ASSIGN',
    'MINUS_ASSIGN',
    'TIMES_ASSIGN',
    'DIVIDE_ASSIGN',
    
    # Delimiters
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'DOT',
    'SEMICOLON',
    'COLON',
    
    # ===== GABRIEL PELAEZ CONTRIBUTION END =====    
]

# ===== CARLA GUTIERREZ CONTRIBUTION START =====

# Variables and Reserved Words
reserved_words = {
    'package': 'PACKAGE',
    'const': 'CONST',
    'var': 'VAR',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'true': 'TRUE',
    'false': 'FALSE',
    'func': 'FUNC',
    'return': 'RETURN',
    'map': 'MAP',
    'int': 'INT_TYPE',
    'float64': 'FLOAT64_TYPE',
    'string': 'STRING_TYPE',
    'bool': 'BOOL_TYPE',
    'range': 'RANGE',
    'true': 'TRUE',
    'false': 'FALSE',
}

tokens = tokens + list(reserved_words.values())

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_words.get(t.value, 'VARIABLE')
    return t


# ===== CARLA GUTIERREZ CONTRIBUTION END =====

# ==========================
# GABRIEL PELAEZ CONTRIBUTION START
# Operators and Delimiters
# ==========================

# Two-character operators
t_EQ = r'=='
t_DECLARE_ASSIGN = r':='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_AND = r'&&'
t_OR = r'\|\|'

# Single-character operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_NOT = r'!'
t_LT = r'<'
t_GT = r'>'
t_ASSIGN = r'='
t_MODULO = r'%'
t_ignore = ' \t'

# Delimiters
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA    = r','
t_DOT      = r'\.'
t_SEMICOLON = r';'
t_COLON     = r':'

# =======================
# GABRIEL PELAEZ CONTRIBUTION END
# =======================

# ==========================
# MILENA PAZMIÑO CONTRIBUTION START
# Recognize integers, floats, strings and comments
# ==========================

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"([^\\\n]|(\\.))*?"'
    return t

def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_UNCLOSED_STRING(t):
    r'"[^"\n]*'
    print(f"Error léxico: cadena no cerrada en línea {t.lexer.lineno}")
    error_msg = f"[Line {t.lexer.lineno}] ERROR           -> {t.value[0]}"
    lexical_errors.append(error_msg)
    
# =======================
# MILENA PAZMIÑO CONTRIBUTION END
# =======================

def t_error(t):
    print(f"Illegal character: {t.value[0]} at line {t.lineno}")
    error_msg = f"[Line {t.lineno}] ERROR           -> {t.value[0]}"
    lexical_errors.append(error_msg)
    t.lexer.skip(1)
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def build_lexer():
    return lex.lex()
