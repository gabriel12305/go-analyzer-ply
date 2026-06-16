import ply.yacc as yacc
from lexer import tokens, build_lexer

# =====================================
# START SYMBOL
# =====================================

start = 'program'

# =====================================
# PRECEDENCE
# =====================================

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'NOT'),
)

# =====================================
# GENERAL RULES
# =====================================

def p_program(p):
    '''
    program : statements
    '''
    pass


def p_statements(p):
    '''
    statements : statements statement
               | statement
    '''
    pass


def p_statement(p):
    '''
    statement : short_var_decl
              | print_stmt
              | for_stmt
              | function_decl
    '''
    pass


# =====================================
# EXPRESSIONS
# =====================================

def p_expression_binop(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression MODULO expression
    '''
    pass


def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    pass


def p_expression_atom(p):
    '''
    expression : INTEGER
               | FLOAT
               | STRING
               | VARIABLE
               | TRUE
               | FALSE
    '''
    pass


# =====================================
# CONDITIONS
# =====================================

def p_condition_rel(p):
    '''
    condition : expression GT expression
              | expression LT expression
              | expression GE expression
              | expression LE expression
              | expression EQ expression
              | expression NE expression
    '''
    pass


def p_condition_logic(p):
    '''
    condition : condition AND condition
              | condition OR condition
              | NOT condition
    '''
    pass


# =====================================
# MILENA RULES
# =====================================

# nombre := "Milena"
def p_short_var_decl(p):
    '''
    short_var_decl : VARIABLE DECLARE_ASSIGN expression
    '''
    pass


# fmt.Println(nombre)
def p_print_stmt(p):
    '''
    print_stmt : VARIABLE DOT VARIABLE LPAREN VARIABLE RPAREN
    '''
    pass


# for edad > 18 { }
def p_for_stmt(p):
    '''
    for_stmt : FOR condition LBRACE statements RBRACE
    '''
    pass


# func suma() { }
def p_function_decl(p):
    '''
    function_decl : FUNC VARIABLE LPAREN RPAREN LBRACE statements RBRACE
    '''
    pass


# =====================================
# ERROR HANDLING
# =====================================
def p_error(p):
    if p:
        print(
            f"Error sintáctico en línea {p.lineno}: token inesperado '{p.value}'"
        )
    else:
        print(
            "Error sintáctico: fin de archivo inesperado"
        )


# =====================================
# BUILD PARSER
# =====================================

parser = yacc.yacc()

lexer = build_lexer()

while True:
    try:
        s = input('parser > ')
    except EOFError:
        break

    if not s:
        continue

    result = parser.parse(s, lexer=lexer)

    print("Entrada válida")