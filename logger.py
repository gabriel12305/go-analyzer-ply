from datetime import datetime
import os
from lexer import lexical_errors
from parser import syntax_errors
from semantic import semantic_errors


def generate_log_filename(author_name="MilenaPazmiño"):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    return f"logs/sintactico-{author_name}-{timestamp}.txt"


def generate_lexical_log_filename(author_name="MilenaPazmiño"):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    return f"logs/lexico-{author_name}-{timestamp}.txt"

def log_lexical_results(tokens_list, author_name):
    log_filename = generate_lexical_log_filename(author_name)
    with open(log_filename, "w", encoding="utf-8") as log:
        for tok_type, tok_value, tok_lineno in tokens_list:
            line = f"[Line {tok_lineno}] {tok_type:<15} -> {tok_value}\n"
            log.write(line)
            print(line, end="")

        if lexical_errors:
            log.write("\n===== LEXICAL ERRORS =====\n")
            for error in lexical_errors:
                log.write(error + "\n")
            print(f"Errores léxicos guardados en {log_filename}")
        else:
            log.write("\nNo se encontraron errores lexicos.\n")
            print(f"No se encontraron errores lexicos. Log generado en {log_filename}")
    return log_filename

def log_syntax_results(log_filename):
    with open(log_filename, "a", encoding="utf-8") as log:
        if syntax_errors:
            log.write("\n===== SYNTAX ERRORS =====\n")
            for error in syntax_errors:
                log.write(error + "\n")
            print(f"Errores sintácticos guardados en {log_filename}")
        else:
            log.write("No se encontraron errores sintacticos.\n")
            print("No se encontraron errores sintacticos.")


def generate_semantic_log_filename(author_name="CarlaGutierrez"):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    return f"logs/semantico-{author_name}-{timestamp}.txt"


def log_semantic_errors(author_name):

    filename = generate_semantic_log_filename(author_name)

    with open(filename, "w", encoding="utf-8") as f:

        if semantic_errors:
            f.write("===== ERRORES SEMÁNTICOS =====\n")

            for error in semantic_errors:
                f.write(error + "\n")

            print(f"Errores semánticos guardados en {filename}")

        else:
            f.write("No se encontraron errores semánticos.\n")
            print(f"No se encontraron errores semánticos. Log generado en {filename}")