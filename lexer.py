import ply.lex as lex
from datetime import datetime

tokens = (
    
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
    'SEMICOLON'
    
    # ===== GABRIEL PELAEZ CONTRIBUTION END =====
)

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

# =======================
# GABRIEL PELAEZ CONTRIBUTION END
# =======================

def t_error(t):
    print(f"Illegal character: {t.value[0]} at line {t.lineno}")
    t.lexer.skip(1)
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
lexer = lex.lex()

with open("lexer_go/pruebas/algorithm_gabriel.go", "r", encoding="utf-8") as archivo:
    data = archivo.read()

timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
log_filename = f"lexer_go/logs/lexico-GabrielPelaez-{timestamp}.txt"

lexer.input(data)

with open(log_filename, "w", encoding="utf-8") as log:

    while True:
        tok = lexer.token()
        if not tok:
            break

        line = f"[Line {tok.lineno}] {tok.type:<15} -> {tok.value}\n"
        log.write(line)
        print(line, end="")
    
