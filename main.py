from lexer import build_lexer, lexical_errors
import lexer
from logger import generate_log_filename, log_syntax_results, log_lexical_results, log_semantic_errors
from parser import build_parser, syntax_errors
from semantic import semantic_errors, symbol_table

def main():

    test_authors = {"CarlaGutierrez": "pruebas/algorithm_carla.go",
                       "GabrielPelaez": "pruebas/algorithm_gabriel.go",
                       "MilenaPazmiño": "pruebas/algorithm_milena.go",}
    
    for author,test in test_authors.items():
        lexical_errors.clear()
        syntax_errors.clear()
        semantic_errors.clear()
        symbol_table.clear()
        
        file_path = test

        with open(file_path, "r", encoding="utf-8") as archivo:
            data = archivo.read()

        lexer = build_lexer()
        parser = build_parser()

        # Capturamos los tokens en la única pasada real del parser,
        # así no se vuelve a tokenizar (y no se duplican errores léxicos)
        captured_tokens = []
        original_token = lexer.token
        def token_wrapper():
            tok = original_token()
            if tok:
                captured_tokens.append((tok.type, tok.value, tok.lineno))
            return tok
        lexer.token = token_wrapper

        parser.parse(data, lexer=lexer)
        
        log_filename = generate_log_filename(author)
        log_syntax_results(log_filename)

        log_lexical_results(captured_tokens, author)
        log_semantic_errors(author)


if __name__ == "__main__":
    main()