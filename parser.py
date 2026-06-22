import ply.yacc as yacc
from lexer import tokens, build_lexer

syntax_errors = []

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
              | slice_decl
              | var_decl
              | switch_stmt
              | map_decl
              | multi_param_function
              | scan_stmt
              | complete_var_dec
              | block
              | if_else
              | array_decl
              | function_no_return
              | increment_stmt
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

def p_expression_list(p):
    '''
    expression_list : expression
                    | expression COMMA expression_list
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

def p_condition_expr(p):
    '''
    condition : expression
    '''
    pass

# =====================================
# MILENA PAZMIÑO CONTRIBUTION START
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
    print_stmt : FMT DOT PRINTLN LPAREN expression RPAREN
                | FMT DOT PRINT LPAREN expression RPAREN
    '''
    pass


# Control Structure for edad > 18 { }
def p_for_stmt(p):
    '''
    for_stmt : FOR condition block
    '''
    pass


# function with return
def p_function_decl(p):
    '''
    function_decl : FUNC VARIABLE LPAREN RPAREN type LBRACE return_stmt RBRACE
                  | FUNC VARIABLE LPAREN RPAREN type LBRACE statements return_stmt RBRACE
    '''
    pass

def p_type(p):
    '''
    type : INT_TYPE
         | FLOAT64_TYPE
         | STRING_TYPE
         | BOOL_TYPE
    '''
    pass

def p_return_stmt(p):
    '''
    return_stmt : RETURN expression
    '''
    pass

# Data structure - Slice. Ej. nombres := []string{} 
def p_slice_decl(p):
    '''
    slice_decl : VARIABLE DECLARE_ASSIGN LBRACKET RBRACKET type LBRACE RBRACE
    '''
    pass

# =====================================
# MILENA PAZMIÑO CONTRIBUTION END
# =====================================

# =====================================
# GABRIEL PELAEZ CONTRIBUTION START
# =====================================

# Variable declaration without initialization
def p_var_decl(p):
    '''
    var_decl : VAR VARIABLE type
    '''
    pass

# Switch control structure
def p_switch_stmt(p):
    '''
    switch_stmt : SWITCH VARIABLE LBRACE case_list default_stmt RBRACE
    '''
    pass

def p_case_list(p):
    '''
    case_list : case_list case_stmt
              | case_stmt
    '''
    pass


def p_case_stmt(p):
    '''
    case_stmt : CASE INTEGER COLON statements
              | CASE STRING COLON statements
    '''
    pass


def p_default_stmt(p):
    '''
    default_stmt : DEFAULT COLON statements
    '''
    pass

# Map data structure. Example: edades := map[string]int{}
def p_map_decl(p):
    '''
    map_decl : VARIABLE DECLARE_ASSIGN MAP LBRACKET STRING_TYPE RBRACKET type LBRACE RBRACE
             | VARIABLE DECLARE_ASSIGN MAP LBRACKET STRING_TYPE RBRACKET type LBRACE map_items RBRACE
    '''
    pass

def p_map_items(p):
    '''
    map_items : map_item
              | map_item COMMA map_items
    '''
    pass

def p_map_item(p):
    '''
    map_item : STRING COLON expression
    '''
    pass

# Function with multiple parameters
def p_multi_param_function(p):
    '''
    multi_param_function : FUNC VARIABLE LPAREN parameter_list RPAREN type LBRACE return_stmt RBRACE
                         | FUNC VARIABLE LPAREN parameter_list RPAREN type LBRACE statements return_stmt RBRACE
    '''
    pass


def p_parameter_list(p):
    '''
    parameter_list : parameter
                   | parameter COMMA parameter_list
    '''
    pass


def p_parameter(p):
    '''
    parameter : VARIABLE type
    '''
    pass

# Input reading with fmt.Scan(&variable)
def p_scan_stmt(p):
    '''
    scan_stmt : FMT DOT SCAN LPAREN AMPERSAND VARIABLE RPAREN
    '''
    pass

def p_increment_stmt(p):
    '''
    increment_stmt : VARIABLE INCREMENT
    '''
    pass

# =====================================
# GABRIEL PELAEZ CONTRIBUTION END
# =====================================

# =====================================
# CARLA GUTIERREZ CONTRIBUTION START
# =====================================

def p_complete_var_dec(p):
    '''
    complete_var_dec : VAR VARIABLE type ASSIGN expression
    '''
    pass

def p_block(p):
    '''
    block : LBRACE statements RBRACE
            | LBRACE RBRACE
    '''
    pass

def p_if_else(p):
    '''
    if_else : IF condition block ELSE block
    '''
    pass

def p_array_decl(p):
    '''
    array_decl : VARIABLE DECLARE_ASSIGN LBRACKET INTEGER RBRACKET type LBRACE expression_list RBRACE
    '''
    pass

def p_function_no_return(p):
    '''
    function_no_return : FUNC VARIABLE LPAREN parameter_list RPAREN block
    '''
    pass

# =====================================
# CARLA GUTIERREZ CONTRIBUTION END
# =====================================

# =====================================
# ERROR HANDLING
# =====================================

def p_error(p):

    if p:
        error_msg = (
            f"Syntax error at line {p.lineno}: "
            f"unexpected token '{p.value}'"
        )

    else:
        error_msg = (
            "Syntax error: unexpected end of file"
        )

    syntax_errors.append(error_msg)

    print(error_msg)


# =====================================
# BUILD PARSER
# =====================================

def build_parser():
    return yacc.yacc()
