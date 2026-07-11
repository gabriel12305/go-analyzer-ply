# GoSubset Code Analyzer

> A graphical lexical, syntactic, and semantic analyzer for a subset of the Go programming language, built with **Python**, **PLY (Python Lex-Yacc)**, and **CustomTkinter**.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![PLY](https://img.shields.io/badge/PLY-Lex--Yacc-green)
![Go](https://img.shields.io/badge/Go-Subset-00ADD8)
![Academic Project](https://img.shields.io/badge/Project-Academic-lightgrey)

---

# Overview

GoSubset Code Analyzer is an educational compiler project developed for the **Programming Languages** course at **ESPOL (Escuela Superior Politécnica del Litoral)**.

The application implements the three fundamental phases of a compiler:

- **Lexical Analysis**
- **Syntactic Analysis**
- **Semantic Analysis**

using **PLY (Python Lex-Yacc)** to recognize and validate a carefully selected subset of the Go programming language.

Unlike a traditional console-based analyzer, this project provides a modern graphical interface that allows users to write, edit, analyze, and visualize Go code interactively. Analysis results are displayed in real time, including detected errors, symbol tables, generated logs, and exported reports.

---

# Features

| Component | Description |
|-----------|-------------|
| **Graphical Interface** | Modern editor with syntax highlighting, themes, line numbering, and integrated analysis tools. |
| **Lexical Analyzer** | Recognizes identifiers, reserved words, literals, operators, delimiters, and comments while reporting lexical errors. |
| **Syntax Analyzer** | Validates the grammar of supported Go statements using context-free grammar rules implemented with PLY. |
| **Semantic Analyzer** | Performs semantic validation including declarations, type compatibility, return types, conversions, and control structures. |
| **Symbol Table** | Stores declared identifiers and their associated types. |
| **Logger** | Automatically generates lexical, syntactic, and semantic log files after every execution. |
| **JSON Export** | Exports analysis results for later processing or reporting. |

---

# Compiler Phases

| Phase | Capabilities |
|-------|--------------|
| **Lexical Analysis** | Recognizes identifiers, reserved words, literals, operators, delimiters, comments, and invalid characters. |
| **Syntax Analysis** | Validates variable declarations, functions, control structures, expressions, arrays, slices, maps, and blocks. |
| **Semantic Analysis** | Detects undeclared identifiers, duplicate declarations, invalid assignments, incompatible arithmetic operations, incorrect function return types, invalid type conversions, and invalid control conditions. |

---

# Supported Go Subset

## Primitive Data Types

- `int`
- `float64`
- `string`
- `bool`

---

## Data Structures

- `array`
- `slice`
- `map`

---

## Variable Declarations

```go
var age int
var age int = 20
name := "Gabriel"
```

---

## Operators

### Arithmetic

```text
+   -   *   /   %
```

### Relational

```text
==   !=   <   >   <=   >=
```

### Logical

```text
&&   ||   !
```

### Assignment

```text
=
:=
+=
-=
*=
/=
```

### Increment

```text
++
```

---

## Control Structures

- `if`
- `if-else`
- `for`
- `switch-case`

---

## Functions

Supported features include:

- Function declaration
- Functions with return values
- Functions with multiple parameters
- Void functions
- Return statements

---

## Input and Output

```go
fmt.Print()
fmt.Println()
fmt.Scan()
```

---

## Type Conversions

```go
int(...)
float64(...)
```

---

## Comments

```go
// Single-line comment

/*
   Multi-line comment
*/
```

---

# Project Structure

```text
go-analyzer-ply/
│
├── gui.py                  # Graphical user interface
├── lexer.py                # Lexical analyzer
├── parser.py               # Syntax analyzer
├── semantic.py             # Semantic analyzer
├── logger.py               # Log generation
├── pruebas/                # Sample Go programs
├── logs/                   # Generated logs
├── parser.out
├── parsetab.py
├── requirements.txt
└── README.md
```

---

# Requirements and Installation

Python **3.11** (or higher) is required.

You can verify your installed version with:

```bash
python --version      # Windows
python3 --version     # macOS / Linux
```

It is recommended to create a virtual environment before installing the project dependencies.

## Windows

Create the virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

```powershell
venv\Scripts\Activate.ps1
```

> **Note (PowerShell users):**
> If script execution is disabled and you receive an error such as *"running scripts is disabled on this system"*, execute the following command once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the virtual environment again:

```powershell
venv\Scripts\Activate.ps1
```

Finally, install the required dependencies:

```bash
pip install -r requirements.txt
```

## macOS / Linux

Create and activate the virtual environment:

```bash
python3 -m venv venv

source venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Program

With the virtual environment activated:

```bash
python gui.py
```

---

# Graphical Interface

The application includes a modern desktop interface built with **CustomTkinter**.

Main features include:

- Code editor
- Line numbering
- Syntax highlighting
- Light and Dark themes
- Adjustable editor font size
- Open Go source files
- Save Go source files
- Execute lexical, syntactic, and semantic analysis
- Error summary panel
- Symbol table visualization
- Block-based syntax tree visualization
- Integrated log viewer
- JSON export of analysis results

---

# Semantic Validation

The semantic analyzer currently validates:

- Duplicate identifier declarations
- Use of undeclared identifiers
- Assignment type compatibility
- Arithmetic operand compatibility
- Function return types
- Type conversions
- Boolean conditions in control structures

---

# Generated Logs

Each execution automatically generates three independent log files inside the **logs/** directory.

```text
logs/

lexico-Author-DD-MM-YYYY-HHhMM.txt
sintactico-Author-DD-MM-YYYY-HHhMM.txt
semantico-Author-DD-MM-YYYY-HHhMM.txt
```

## Lexical Log

Contains:

- Recognized tokens
- Lexical errors

---

## Syntax Log

Contains:

- Syntax errors detected during parsing

---

## Semantic Log

Contains:

- Semantic validation errors

---

# JSON Export

The application can export the analysis results as a JSON file containing:

- Number of recognized tokens
- Lexical errors
- Syntax errors
- Semantic errors
- Symbol table

---

# Team

| Developer | GitHub | Responsibilities |
|------------|------------|------------|
| **Carla Gutiérrez** | cgutierrez05 | **Lexical:** Variables and reserved words.<br>**Syntax:** Variable declarations with `var`, `if-else`, arrays, void functions, printing statements.<br>**Semantic:** Identifier validation and arithmetic operand compatibility. |
| **Silvia Milena Pazmiño** | leno-mpm | **Lexical:** Literals and comments.<br>**Syntax:** Short variable declarations (`:=`), `for`, slices, functions with return values, printing statements.<br>**Semantic:** Assignment type compatibility and function return validation. |
| **Christian Gabriel Peláez** | gabriel12305 | **Lexical:** Operators and delimiters.<br>**Syntax:** Variable declarations, `switch`, maps, multiple-parameter functions, input handling.<br>**Semantic:** Type conversions and control structure validation. |

---

# Tech Stack

- Python 3.13
- PLY (Python Lex-Yacc)
- CustomTkinter
- Visual Studio Code
- Git
- GitHub

---

# Course

**Programming Languages**  
Faculty of Electrical and Computer Engineering (FIEC)  
Escuela Superior Politécnica del Litoral (ESPOL)

**Instructor:** Rodrigo Alexander Saraguro Bravo

**Year:** 2026

---

# References

1. https://go.dev/doc/
2. https://go.dev/tour/welcome/1
3. https://ply.readthedocs.io/en/latest/
4. https://customtkinter.tomschimansky.com/
5. https://docs.python.org/3/
