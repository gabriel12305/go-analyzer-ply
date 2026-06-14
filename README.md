# go-analyzer-ply

> Lexical, syntactic, and semantic analyzer for a subset of the Go programming language, built with Python and PLY (Python Lex-Yacc).

---

## Overview

This project implements the three core phases of language analysis — **lexical**, **syntactic**, and **semantic** — for a carefully selected subset of Go. It was developed as part of the *Programming Languages* course at **ESPOL** (Escuela Superior Politécnica del Litoral), FIEC.

The analyzer reads Go source code, tokenizes it, validates its grammar, and checks for semantic consistency — reporting errors with precise line numbers and descriptions at every stage.

---

## Features

| Phase | Capabilities |
|---|---|
| **Lexical** | Recognizes identifiers, keywords, operators, delimiters, literals; detects invalid characters |
| **Syntactic** | Validates variable declarations, control structures, functions, data structures, and expressions |
| **Semantic** | Checks type compatibility, identifier scope, function return types, and control flow correctness |

---

## Go Subset Supported

### Data Types
`int` · `float64` · `string` · `bool`

### Data Structures
`array` · `slice` · `map`

### Operators
- Arithmetic: `+` `-` `*` `/` `%`
- Relational: `==` `!=` `<` `>` `<=` `>=`
- Logical: `&&` `||` `!`
- Assignment: `=` `+=` `-=` `*=` `/=`

### Control Structures
`if / else` · `for` · `switch`

### Other
- Variable declaration (`var`, `:=`, `const`)
- Function declaration and calls
- `fmt.Println` / `fmt.Scan`
- Single-line (`//`) and multi-line (`/* */`) comments

---

## Project Structure

```

```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PLY library

```bash
pip install ply
```

### Running the Analyzer

```bash
python main.py
```

---

## Log Files

Every time the analyzer runs, it generates a log file in the `logs/` folder with the following naming convention:

```
lexico-NombreApellido-DD-MM-YYYY-HHhMM.txt
```

Example: `lexico-MilenaPazmiño-14-06-2026-14h32.txt`

Each log records all recognized tokens (or errors), the developer's name, and a timestamp.

---

## Team

## Team

| Developer | GitHub | Responsibilities |
|------------|------------|------------|
| Carla Gutiérrez | cgutierrez05 | **Lexical:** Variables and reserved words. <br> **Syntactic:** Variable declaration with `var`, `if-else` structure, Array data structure, void functions, string printing. <br> **Semantic:** Identifier validation and permitted operations. |
| Silvia Milena Pazmiño | leno-mpm | **Lexical:** Data types and comments. <br> **Syntactic:** Short variable declaration (`:=`), `for` structure, Slice data structure, functions with return values, variable printing. <br> **Semantic:** Type assignment and function return validation. |
| Christian Gabriel Peláez | gabriel12305 | **Lexical:** Arithmetic, relational, logical and assignment operators, and delimiters. <br> **Syntactic:** Variable declaration without initialization, `switch` structure, Map data structure, functions with multiple parameters, keyboard input handling. <br> **Semantic:** Type conversion and control structure validation. |

---

## Tech Stack

- **Python 3.13** — implementation language
- **PLY (Python Lex-Yacc)** — lexer and parser construction
- **Visual Studio Code** — development environment
- **Git / GitHub** — version control and collaboration
- **Canva** — UI prototyping

---

## Course

**Programming Languages** · FIEC · ESPOL  
Instructor: Rodrigo Alexander Saraguro Bravo · 2026

---

## References

1. [Go Documentation](https://go.dev/doc/)
2. [A Tour of Go](https://go.dev/tour/welcome/1)
3. [PLY Documentation](https://ply.readthedocs.io/en/latest/)
