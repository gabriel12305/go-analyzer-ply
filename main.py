from lexer import build_lexer, lexical_errors
import lexer
from logger import generate_log_filename, log_syntax_results, log_tokens
from parser import build_parser, syntax_errors

def main():

    test_authors = {"CarlaGutierrez": "pruebas/algorithm_carla.go",
                       "GabrielPelaez": "pruebas/algorithm_gabriel.go",
                       "MilenaPazmiño": "pruebas/algorithm_milena.go",
                    }
    
    for author,test in test_authors.items():
        lexical_errors.clear()
        syntax_errors.clear()
        file_path = test

        with open(file_path, "r", encoding="utf-8") as archivo:
            data = archivo.read()

        lexer = build_lexer()
        parser = build_parser()
        
        parser.parse(data, lexer=lexer)
        
        log_filename = generate_log_filename(author)
        
        log_tokens(lexer, data, log_filename)
        
        log_syntax_results(log_filename)


if __name__ == "__main__":
    main()