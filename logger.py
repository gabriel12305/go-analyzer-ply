from datetime import datetime
import os
from lexer import lexical_errors

def generate_log_filename(author_name="MilenaPazmiño"):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    return f"logs/lexico-{author_name}-{timestamp}.txt"


def log_tokens(lexer, data, log_filename):
    lexer.input(data)

    with open(log_filename, "w", encoding="utf-8") as log:
        while True:
            tok = lexer.token()

            if not tok:
                break

            line = f"[Line {tok.lineno}] {tok.type:<15} -> {tok.value}\n"

            log.write(line)
            print(line, end="")
        
        if lexical_errors:
            log.write("\n===== LEXICAL ERRORS =====\n")

            for error in lexical_errors:
                log.write(error + "\n")
