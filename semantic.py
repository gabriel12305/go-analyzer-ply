semantic_errors = []

symbol_table = {}

def declare_identifier(name, type_, line=None):
    """Registra un identificador con su tipo."""
    if name in symbol_table:
        semantic_errors.append(f"[Line {line}] Error Semántico [Declaración]: la variable/función '{name}' ya fue declarada.")
    else:
        symbol_table[name] = type_

def lookup_identifier(name, line=None):
    """Verifica si el identificador existe. Si no, agrega error."""
    if name not in symbol_table:
        semantic_errors.append(f"[Line {line}] Error Semántico [Identificador]: la variable/función '{name}' no ha sido declarada.")
        return None
    return symbol_table[name]

def get_type(identifier, line=None):
    """Devuelve el tipo de un identificador (o None si no existe)."""
    return lookup_identifier(identifier, line)

def check_arithmetic_operands(left_type, right_type, operator, line=None):
    """Verifica que ambos tipos sean numéricos compatibles para operación aritmética."""
    numeric_types = {'int', 'float64', 'INT_TYPE', 'FLOAT64_TYPE'}  # según tus tokens
    if left_type not in numeric_types or right_type not in numeric_types:
        semantic_errors.append(
            f"[Line {line}] Error Semántico [Tipos]: el operador '{operator}' no está definido para operandos de tipo '{left_type}' y '{right_type}'."
        )
        return False
    return True

# ==== GABRIEL PELAEZ CONTRIBUTION ====

def check_type_conversion(source_type, target_type, line):

    if source_type is None:
        return

    numeric = ['int', 'float64']

    if source_type == target_type:
        return

    if source_type in numeric and target_type in numeric:
        return

    semantic_errors.append(
        f"[Line {line}] Error Semántico [Conversión]: "
        f"no es posible convertir un valor de tipo "
        f"'{source_type}' a '{target_type}'."
    )
    
def check_control_condition(condition_type, line):

    if condition_type is None:
        return

    if condition_type != 'bool':
        semantic_errors.append(
            f"[Line {line}] Error Semántico [Estructura de Control]: "
            f"la condición debe producir un valor de tipo bool."
        )