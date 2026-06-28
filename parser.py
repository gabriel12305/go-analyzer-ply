import ply.yacc as yacc
import semantic
from semantic import semantic_errors, declare_identifier, lookup_identifier, check_arithmetic_operands
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
              | assignment_stmt
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

    # ===== CARLA GUTIERREZ CONTRIBUTION - SEMANTIC RULE =====
    left_type = p[1]['type']   
    right_type = p[3]['type']

    check_arithmetic_operands(left_type, right_type, p[2], p.lineno(2))

    if left_type == 'float64' or right_type == 'float64':
        p[0] = {'type': 'float64'}
    else:
        p[0] = {'type': 'int'}


def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''

    # ===== CARLA GUTIERREZ CONTRIBUTION - SEMANTIC RULE =====
    p[0] = p[2]

def p_expression_conversion(p):
    '''
    expression : INT_TYPE LPAREN expression RPAREN
               | FLOAT64_TYPE LPAREN expression RPAREN
    '''
    # ==== GABRIEL PELAEZ CONTRIBUTION - SEMANTIC RULE ====
    source_type = p[3]['type']
    target_type = p[1]

    semantic.check_type_conversion(
        source_type,
        target_type,
        p.lineno(1)
    )

    p[0] = {'type': target_type}

def p_expression_atom(p):
    '''
    expression : INTEGER
               | FLOAT
               | STRING
               | VARIABLE
               | TRUE
               | FALSE
    '''
    # ===== CARLA GUTIERREZ CONTRIBUTION - SEMANTIC RULE =====
    if p.slice[1].type == 'INTEGER':
        p[0] = {'type': 'int', 'value': p[1]}

    elif p.slice[1].type == 'FLOAT':
        p[0] = {'type': 'float64', 'value': p[1]}

    elif p.slice[1].type == 'STRING':
        p[0] = {'type': 'string', 'value': p[1]}

    elif p.slice[1].type == 'TRUE' or p.slice[1].type == 'FALSE':
        p[0] = {'type': 'bool', 'value': p[1]}

    elif p.slice[1].type == 'VARIABLE':
        var_name = p[1]
        var_type = lookup_identifier(var_name, p.lineno(1))
        p[0] = {'type': var_type, 'value': var_name}

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
    # ==== GABRIEL PELAEZ CONTRIBUTION - SEMANTIC RULE ====
    p[0] = {'type': 'bool'}


def p_condition_logic(p):
    '''
    condition : condition AND condition
              | condition OR condition
              | NOT condition
    '''
    # ==== GABRIEL PELAEZ CONTRIBUTION - SEMANTIC RULE ====
    p[0] = {'type': 'bool'}

def p_condition_expr(p):
    '''
    condition : expression
    '''
    # ==== GABRIEL PELAEZ CONTRIBUTION - SEMANTIC RULE ====
    p[0] = p[1]

# =====================================
# MILENA PAZMIÑO CONTRIBUTION START
# =====================================

# nombre := "Milena"
def p_short_var_decl(p):
    '''
    short_var_decl : VARIABLE DECLARE_ASSIGN expression
    '''
    # ===== MILENA PAZMIÑO CONTRIBUTION - SEMANTIC RULE - Aquí no existe declaración de tipos =====
    # ===== CARLA GUTIERREZ CONTRIBUTION - SEMANTIC RULE =====
    declare_identifier(p[1], p[3]['type'], p.lineno(1))


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
    # ==== GABRIEL PELAEZ CONTRIBUTION - SEMANTIC RULE ====
    semantic.check_control_condition(
        p[2]['type'],
        p.lineno(1)
    )


# function with return
def p_function_decl(p):
    '''
    function_decl : FUNC VARIABLE LPAREN RPAREN type LBRACE return_stmt RBRACE
                  | FUNC VARIABLE LPAREN RPAREN type LBRACE statements return_stmt RBRACE
    '''
    
    #==== MILENA PAZMIÑO CONTRIBUTION - SEMANTIC RULE - Funcion con retorno ====
    #Para esto fue necesario que p_type y p_return_stmt devuelvan el tipo de la expresión, 
    #para poder comparar si el tipo de retorno de la función coincide con el tipo de la expresión retornada.
    
    expected_type = p[5]

    if len(p) == 9: #Len (p) calcula el número de elementos en la producción. 
        returned_type = p[7]['type']
    else:
        returned_type = p[8]['type']

    if expected_type != returned_type:
        semantic_errors.append(
            f"[Line {p.lineno(5)}] Error Semántico [Retorno de Función]: "
            f"se esperaba un valor de tipo '{expected_type}' "
            f"pero se retornó un valor de tipo '{returned_type}'."
        )

def p_type(p):
    '''
    type : INT_TYPE
         | FLOAT64_TYPE
         | STRING_TYPE
         | BOOL_TYPE
    '''

    # ===== CARLA GUTIERREZ CONTRIBUTION - SEMANTIC RULE =====
    p[0] = p[1] #Necesario para que la función devuelva el tipo, útil para validaciones semánticas posteriores.

def p_return_stmt(p):
    '''
    return_stmt : RETURN expression
    '''
    p[0] = p[2] #Necesario para que la función devuelva el tipo de la expresión retornada, útil para validaciones semánticas posteriores.

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
    # ===== CARLA GUTIERREZ CONTRIBUTION - SEMANTIC RULE =====
    declare_identifier(p[2], p[3], p.lineno(2))


def p_assignment_stmt(p):
    '''
    assignment_stmt : VARIABLE ASSIGN expression
    '''
    # ===== MILENA PAZMIÑO CONTRIBUTION - SEMANTIC RULE =====
    var_name = p[1]

    declared_type = lookup_identifier(var_name, p.lineno(1)) # Verifica si la variable fue declarada y obtiene su tipo
    expr_type = p[3]['type']

    if declared_type is not None and declared_type != expr_type:
        semantic_errors.append(
            f"[Line {p.lineno(2)}] Error Semántico [Asignación de Tipo]: "
            f"no se puede asignar un valor de tipo '{expr_type}' "
            f"a una variable de tipo '{declared_type}'."
        )

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
    #=== MILENA PAZMIÑO CONTRIBUTION - SEMANTIC RULE - Funcion con retorno ====
    #Para esto fue necesario que p_type y p_return_stmt devuelvan el tipo de la expresión, 
    #para poder comparar si el tipo de retorno de la función coincide con el tipo de la expresión retornada.
    
    expected_type = p[6]

    if len(p) == 10:
        returned_type = p[8]['type']
    else:
        returned_type = p[9]['type']

    if expected_type != returned_type:
        semantic_errors.append(
            f"[Line {p.lineno(6)}] Error Semántico [Retorno de Función]: "
            f"se esperaba un valor de tipo '{expected_type}' "
            f"pero se retornó un valor de tipo '{returned_type}'."
        )


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
    # ===== CARLA GUTIERREZ CONTRIBUTION - SEMANTIC RULE =====
    lookup_identifier(p[6], p.lineno(6))

def p_increment_stmt(p):
    '''
    increment_stmt : VARIABLE INCREMENT
    '''
    # ===== CARLA GUTIERREZ CONTRIBUTION - SEMANTIC RULE =====
    lookup_identifier(p[1], p.lineno(1)) 

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
    
    # ==== MILENA PAZMIÑO CONTRIBUTION - SEMANTIC RULE ====
    
    var_name = p[2]          
    declared_type = p[3]   
    expr_type = p[5]['type']

    declare_identifier(var_name, declared_type, p.lineno(2)) # Verifica si la variable ya fue declarada y la registra en la tabla de símbolos

    if declared_type != expr_type:
        semantic_errors.append(
            f"[Line {p.lineno(4)}] Error Semántico [Tipos]: no se puede asignar "
            f"expresión de tipo '{expr_type}' a variable de tipo '{declared_type}'."
        )

    

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
    # ==== GABRIEL PELAEZ CONTRIBUTION - SEMANTIC RULE ====
    semantic.check_control_condition(
        p[2]['type'],
        p.lineno(1)
    )

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
