from lexer import build_lexer
from logger import generate_log_filename, log_tokens

def main():

    test_authors = {"CarlaGutierrez": "pruebas/algorithm_carla.go",
                       "GabrielPelaez": "pruebas/algorithm_gabriel.go",
                       "MilenaPazmiño": "pruebas/algorithm_milena.go",}
    
    for author,test in test_authors.items():
        file_path = test

        with open(file_path, "r", encoding="utf-8") as archivo:
            data = archivo.read()

        lexer = build_lexer()

        log_filename = generate_log_filename(author)

        log_tokens(lexer, data, log_filename)


if __name__ == "__main__":
    main()