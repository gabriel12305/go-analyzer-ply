"""
GoSubset Code Analyzer - Interfaz gráfica.

"""

import os
import re
import glob
import json
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

import lexer
import parser as go_parser
import semantic
import logger

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# =====================================================================
# PALETA DE COLORES
# =====================================================================

PALETTE = {
    "Light": {
        "bg": "#F3F5FA",
        "card": "#FFFFFF",
        "border": "#E3E7EF",
        "text": "#1F2937",
        "muted": "#6B7280",
        "accent": "#2F6FEB",
        "accent_hover": "#255BC4",
        "green": "#17A34A",
        "orange": "#F59E0B",
        "red": "#DC2626",
        "red_bg": "#FDECEC",
        "editor_bg": "#FFFFFF",
        "editor_fg": "#1F2937",
        "gutter_bg": "#F3F5FA",
        "gutter_fg": "#9AA3B2",
        "select_bg": "#DCE7FF",
    },
    "Dark": {
        "bg": "#1B1D24",
        "card": "#242630",
        "border": "#33363F",
        "text": "#E7E9EE",
        "muted": "#9AA0AC",
        "accent": "#5B8DEF",
        "accent_hover": "#4A76CC",
        "green": "#3ED17E",
        "orange": "#F5B94A",
        "red": "#F16565",
        "red_bg": "#3A2429",
        "editor_bg": "#1E1F27",
        "editor_fg": "#E7E9EE",
        "gutter_bg": "#1B1D24",
        "gutter_fg": "#6B7280",
        "select_bg": "#2E3A56",
    },
}

SYNTAX_COLORS_LIGHT = {
    "keyword": "#8B3FE8",
    "string": "#B45309",
    "number": "#2563EB",
    "comment": "#16A34A",
}
SYNTAX_COLORS_DARK = {
    "keyword": "#C792EA",
    "string": "#E0AF68",
    "number": "#7DB3FF",
    "comment": "#6BCB77",
}

RESERVED_WORDS = set(lexer.reserved_words.keys())

DEMO_CODE = '''var edad int = 20
var nombre string = "Carla"
promedio := 8.5

fmt.Println(nombre)

resultado := edad + promedio

if edad >= 18 {
    fmt.Println("Mayor de edad")
} else {
    fmt.Println("Menor de edad")
}

edad = "veinte"

fmt.Println(x)
'''

AUTHORS = ["Christian Gabriel Peláez", "Silvia Milena Pazmiño", "Carla Gutiérrez", "Usuario"]


# =====================================================================
# PUENTE HACIA EL ANALIZADOR (usa lexer.py / parser.py / semantic.py tal cual)
# =====================================================================

class AnalysisResult:
    def __init__(self):
        self.tokens = []
        self.lexical_errors = []
        self.syntax_errors = []
        self.semantic_errors = []
        self.symbol_table = {}


class Analyzer:
    """Envuelve las funciones ya existentes del proyecto sin alterarlas."""

    def __init__(self):
        self.parser = go_parser.build_parser()

    def run(self, code):
        lexer.lexical_errors.clear()
        go_parser.syntax_errors.clear()
        semantic.semantic_errors.clear()
        semantic.symbol_table.clear()

        lx = lexer.build_lexer()
        collected_tokens = []
        original_token = lx.token

        def token_wrapper():
            tok = original_token()
            if tok:
                collected_tokens.append(tok)
            return tok

        lx.token = token_wrapper

        try:
            self.parser.parse(code, lexer=lx)
        except Exception as exc:
            go_parser.syntax_errors.append(f"Syntax error: {exc}")

        result = AnalysisResult()
        result.tokens = collected_tokens
        result.lexical_errors = list(dict.fromkeys(lexer.lexical_errors))
        result.syntax_errors = list(go_parser.syntax_errors)
        result.semantic_errors = list(semantic.semantic_errors)
        result.symbol_table = dict(semantic.symbol_table)
        return result

    def write_logs(self, code, result, author):
        """Genera los archivos de log reales usando logger.py, sin re-tokenizar
        con el mismo lexer (evita duplicar lexical_errors) y usando el resultado
        de una única pasada ya calculado en `result`."""
        os.makedirs("logs", exist_ok=True)
        log_filename = logger.generate_log_filename(author)

        with open(log_filename, "w", encoding="utf-8") as f:
            for tok in result.tokens:
                f.write(f"[Line {tok.lineno}] {tok.type:<15} -> {tok.value}\n")

        lexer.lexical_errors.clear()
        lexer.lexical_errors.extend(result.lexical_errors)
        go_parser.syntax_errors.clear()
        go_parser.syntax_errors.extend(result.syntax_errors)
        logger.log_syntax_results(log_filename)

        semantic.semantic_errors.clear()
        semantic.semantic_errors.extend(result.semantic_errors)
        logger.log_semantic_errors(author)

        sem_files = sorted(
            glob.glob(f"logs/semantico-{author}-*.txt"), key=os.path.getmtime
        )
        sem_filename = sem_files[-1] if sem_files else None
        return log_filename, sem_filename


# =====================================================================
# FORMATEO DE ERRORES PARA LA UI
# =====================================================================

def format_lexical(msg):
    m = re.match(r"\[Line (\d+)\]\s*ERROR\s*->\s*(.*)", msg)
    if m:
        line, ch = m.groups()
        return line, f"Carácter no reconocido: '{ch}'"
    return "-", msg


def format_syntax(msg):
    m = re.search(r"line (\d+):\s*(.*)", msg)
    if m:
        return m.group(1), m.group(2)
    return "-", msg


def format_semantic(msg):
    m = re.match(r"\[Line (\d+)\]\s*Error Semántico\s*\[(.*?)\]:\s*(.*)", msg)
    if m:
        line, category, desc = m.groups()
        return line, f"{category} - {desc}"
    return "-", msg


def build_findings(result):
    findings = []
    for raw in result.lexical_errors:
        line, msg = format_lexical(raw)
        findings.append({"line": line, "type": "Léxico", "message": msg})
    for raw in result.syntax_errors:
        line, msg = format_syntax(raw)
        findings.append({"line": line, "type": "Sintáctico", "message": msg})
    for raw in result.semantic_errors:
        line, msg = format_semantic(raw)
        findings.append({"line": line, "type": "Semántico", "message": msg})

    def sort_key(item):
        try:
            return (0, int(item["line"]))
        except ValueError:
            return (1, 0)

    findings.sort(key=sort_key)
    return findings


def build_block_tree(tokens):
    lines = []
    depth = 0
    for tok in tokens:
        if tok.type == "RBRACE":
            depth = max(depth - 1, 0)
        indent = "    " * depth
        value = tok.value
        if isinstance(value, str) and len(value) > 24:
            value = value[:21] + "..."
        lines.append(f"{indent}[L{tok.lineno:<3}] {tok.type:<14} {value}")
        if tok.type == "LBRACE":
            depth += 1
    return "\n".join(lines) if lines else "(sin tokens que mostrar)"


# =====================================================================
# WIDGETS AUXILIARES
# =====================================================================

class Dot(ctk.CTkFrame):
    def __init__(self, master, color, size=11):
        super().__init__(master, width=size, height=size, corner_radius=size // 2,
                          fg_color=color, bg_color="transparent")
        self.grid_propagate(False)


class Card(ctk.CTkFrame):
    def __init__(self, master, colors, title=None, icon=""):
        super().__init__(master, fg_color=colors["card"], corner_radius=12,
                          border_width=1, border_color=colors["border"])
        self.colors = colors
        if title:
            header = ctk.CTkLabel(
                self, text=f"{icon}  {title}".strip(),
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=colors["text"], anchor="w",
            )
            header.pack(fill="x", padx=16, pady=(14, 6))


# =====================================================================
# APLICACIÓN PRINCIPAL
# =====================================================================

class GoAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.settings = {"author": AUTHORS[0], "theme": "Light", "font_size": 13}
        self.colors = PALETTE[self.settings["theme"]]
        self.current_file = None
        self.analyzer = Analyzer()
        self.last_result = None
        self.last_log_files = None

        self.title("GoSubset Code Analyzer - v1.0")
        self.geometry("1360x780")
        self.minsize(1040, 640)
        self.configure(fg_color=self.colors["bg"])

        self._build_toolbar()
        self._build_main()
        self._build_statusbar()

        self.code_text.insert("1.0", DEMO_CODE)
        self._refresh_line_numbers()
        self._highlight_syntax()
        self._set_status("Listo | Código de ejemplo cargado")

        self.bind_all("<Control-Return>", lambda e: self.run_analysis())
        self.bind_all("<F5>", lambda e: self.run_analysis())
        self.bind_all("<Control-o>", lambda e: self.load_file())
        self.bind_all("<Control-s>", lambda e: self.save_file())

    # -----------------------------------------------------------------
    # TOOLBAR
    # -----------------------------------------------------------------

    def _build_toolbar(self):
        bar = ctk.CTkFrame(self, fg_color=self.colors["card"], corner_radius=0,
                            height=58, border_width=0)
        bar.pack(side="top", fill="x")
        bar.pack_propagate(False)

        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side="left", padx=14, pady=10)

        def make_btn(parent, text, command, primary=False):
            return ctk.CTkButton(
                parent, text=text, command=command,
                fg_color=self.colors["accent"] if primary else "transparent",
                hover_color=self.colors["accent_hover"] if primary else self.colors["bg"],
                text_color="#FFFFFF" if primary else self.colors["text"],
                border_width=0 if primary else 1,
                border_color=self.colors["border"],
                corner_radius=8, font=ctk.CTkFont(size=13, weight="bold" if primary else "normal"),
                height=34,
            )

        make_btn(left, "📂  Cargar Archivo (.go)", self.load_file).pack(side="left", padx=4)
        make_btn(left, "💾  Guardar", self.save_file).pack(side="left", padx=4)
        make_btn(left, "🔍  Analizar Código", self.run_analysis, primary=True).pack(side="left", padx=4)
        make_btn(left, "🗑  Limpiar Editor", self.clear_editor).pack(side="left", padx=4)

        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right", padx=14, pady=10)
        make_btn(right, "⚙  Configuración", self.open_settings).pack(side="right")

        self.toolbar = bar

    # -----------------------------------------------------------------
    # MAIN LAYOUT
    # -----------------------------------------------------------------

    def _build_main(self):
        container = ctk.CTkFrame(self, fg_color=self.colors["bg"], corner_radius=0)
        container.pack(side="top", fill="both", expand=True, padx=14, pady=(12, 6))
        container.grid_columnconfigure(0, weight=3)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)

        self._build_editor(container)
        self._build_results(container)

    # ---- Editor ----

    def _build_editor(self, parent):
        card = Card(parent, self.colors)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        editor_wrap = tk.Frame(card, bg=self.colors["card"])
        editor_wrap.pack(fill="both", expand=True, padx=10, pady=10)

        text_frame = tk.Frame(editor_wrap, bg=self.colors["border"], bd=0)
        text_frame.pack(fill="both", expand=True)

        vsb = ctk.CTkScrollbar(text_frame, orientation="vertical", command=self._on_vsb)
        vsb.pack(side="right", fill="y")

        inner = tk.Frame(text_frame, bg=self.colors["editor_bg"])
        inner.pack(side="left", fill="both", expand=True, padx=1, pady=1)

        font = ("Consolas", self.settings["font_size"])

        self.line_numbers = tk.Text(
            inner, width=4, padx=8, pady=8, takefocus=0, border=0,
            state="disabled", wrap="none", font=font,
            bg=self.colors["gutter_bg"], fg=self.colors["gutter_fg"],
            highlightthickness=0,
        )
        self.line_numbers.pack(side="left", fill="y")

        self.code_text = tk.Text(
            inner, wrap="none", undo=True, padx=8, pady=8, border=0,
            font=font, bg=self.colors["editor_bg"], fg=self.colors["editor_fg"],
            insertbackground=self.colors["accent"], selectbackground=self.colors["select_bg"],
            highlightthickness=0,
        )
        self.code_text.pack(side="left", fill="both", expand=True)

        self.code_text.configure(yscrollcommand=lambda *a: self._on_code_yscroll(vsb, *a))

        self.code_text.bind("<KeyRelease>", self._on_code_change)
        self.code_text.bind("<MouseWheel>", self._sync_scroll_wheel)
        self.line_numbers.bind("<MouseWheel>", self._sync_scroll_wheel)

    def _on_vsb(self, *args):
        self.code_text.yview(*args)
        self.line_numbers.yview(*args)

    def _on_code_yscroll(self, scrollbar, first, last):
        scrollbar.set(first, last)
        self.line_numbers.yview_moveto(first)

    def _sync_scroll_wheel(self, event):
        delta = -1 if event.delta > 0 else 1
        self.code_text.yview_scroll(delta, "units")
        self.line_numbers.yview_scroll(delta, "units")
        return "break"

    def _on_code_change(self, event=None):
        self._refresh_line_numbers()
        self._highlight_syntax()

    def _refresh_line_numbers(self):
        n_lines = int(self.code_text.index("end-1c").split(".")[0])
        content = "\n".join(str(i) for i in range(1, n_lines + 1))
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", content)
        self.line_numbers.configure(state="disabled")

    def _highlight_syntax(self):
        colors = SYNTAX_COLORS_DARK if self.settings["theme"] == "Dark" else SYNTAX_COLORS_LIGHT
        for tag in ("keyword", "string", "number", "comment"):
            self.code_text.tag_remove(tag, "1.0", "end")

        self.code_text.tag_configure("keyword", foreground=colors["keyword"])
        self.code_text.tag_configure("string", foreground=colors["string"])
        self.code_text.tag_configure("number", foreground=colors["number"])
        self.code_text.tag_configure("comment", foreground=colors["comment"])

        content = self.code_text.get("1.0", "end-1c")

        patterns = [
            ("comment", r"//[^\n]*|/\*[\s\S]*?\*/"),
            ("string", r'"([^"\\]|\\.)*"'),
            ("number", r"\b\d+(\.\d+)?\b"),
            ("keyword", r"\b(" + "|".join(re.escape(w) for w in RESERVED_WORDS) + r")\b"),
        ]
        for tag, pattern in patterns:
            for m in re.finditer(pattern, content):
                start = f"1.0+{m.start()}c"
                end = f"1.0+{m.end()}c"
                self.code_text.tag_add(tag, start, end)

    # ---- Results panel ----

    def _build_results(self, parent):
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        wrap.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.tabview = ctk.CTkTabview(
            wrap, fg_color=self.colors["card"], corner_radius=12,
            segmented_button_fg_color=self.colors["bg"],
            segmented_button_selected_color=self.colors["accent"],
            segmented_button_selected_hover_color=self.colors["accent_hover"],
            segmented_button_unselected_color=self.colors["bg"],
            text_color=self.colors["text"],
            border_width=1, border_color=self.colors["border"],
        )
        self.tabview.pack(fill="both", expand=True)

        self.tab_resumen = self.tabview.add("Resumen")
        self.tab_symbols = self.tabview.add("Tabla de Símbolos")
        self.tab_tree = self.tabview.add("Árbol Sintáctico")
        self.tab_logs = self.tabview.add("Logs")

        self._build_resumen_tab()
        self._build_symbols_tab()
        self._build_tree_tab()
        self._build_logs_tab()

    def _build_resumen_tab(self):
        tab = self.tab_resumen
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        stats_card = Card(tab, self.colors, "Estadísticas de Análisis", "📊")
        stats_card.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))

        self.stat_rows = {}
        for key, label, color in [
            ("tokens", "Tokens Reconocidos", self.colors["accent"]),
            ("lexico", "Errores Léxicos", self.colors["green"]),
            ("sintactico", "Errores Sintácticos", self.colors["green"]),
            ("semantico", "Errores Semánticos", self.colors["green"]),
        ]:
            row = ctk.CTkFrame(stats_card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=4)
            dot = Dot(row, color)
            dot.pack(side="left", padx=(0, 8))
            ctk.CTkLabel(row, text=label, text_color=self.colors["text"],
                         font=ctk.CTkFont(size=13), anchor="w").pack(side="left")
            val = ctk.CTkLabel(row, text="0", text_color=self.colors["muted"],
                               font=ctk.CTkFont(size=13, weight="bold"))
            val.pack(side="right")
            self.stat_rows[key] = (dot, val)
        ctk.CTkFrame(stats_card, fg_color="transparent", height=8).pack()

        results_card = Card(tab, self.colors, "Resultados Detallados", "🧾")
        results_card.grid(row=1, column=0, sticky="nsew", padx=10, pady=(6, 10))
        results_card.grid_rowconfigure(1, weight=1)
        results_card.grid_columnconfigure(0, weight=1)

        self.results_scroll = ctk.CTkScrollableFrame(
            results_card, fg_color="transparent")
        self.results_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        footer = ctk.CTkFrame(results_card, fg_color="transparent")
        footer.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkButton(
            footer, text="Exportar Resultados (JSON)", command=self.export_json,
            fg_color="transparent", text_color=self.colors["accent"],
            hover_color=self.colors["bg"], border_width=1,
            border_color=self.colors["border"], corner_radius=8, height=28,
            font=ctk.CTkFont(size=12),
        ).pack(side="right")

        self._render_placeholder(self.results_scroll, "Presiona “Analizar Código” para ver resultados.")

    def _build_symbols_tab(self):
        tab = self.tab_symbols
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        self.symbols_scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self.symbols_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self._render_symbol_table({})

    def _build_tree_tab(self):
        tab = self.tab_tree
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            tab, text="Estructura por anidación de bloques (a partir de los tokens reconocidos)",
            text_color=self.colors["muted"], font=ctk.CTkFont(size=12), anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))

        wrap = tk.Frame(tab, bg=self.colors["border"])
        wrap.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        vsb = ctk.CTkScrollbar(wrap, orientation="vertical")
        vsb.pack(side="right", fill="y")

        inner = tk.Frame(wrap, bg=self.colors["editor_bg"])
        inner.pack(side="left", fill="both", expand=True, padx=1, pady=1)

        self.tree_text = tk.Text(
            inner, wrap="none", state="disabled", padx=10, pady=10, border=0,
            font=("Consolas", 12), bg=self.colors["editor_bg"], fg=self.colors["editor_fg"],
            highlightthickness=0,
        )
        self.tree_text.pack(side="left", fill="both", expand=True)
        vsb.configure(command=self.tree_text.yview)
        self.tree_text.configure(yscrollcommand=vsb.set)

    def _build_logs_tab(self):
        tab = self.tab_logs
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        self.logs_info = ctk.CTkLabel(
            tab, text="Aún no se han generado logs en esta sesión.",
            text_color=self.colors["muted"], font=ctk.CTkFont(size=12), anchor="w",
        )
        self.logs_info.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))

        wrap = tk.Frame(tab, bg=self.colors["border"])
        wrap.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        vsb = ctk.CTkScrollbar(wrap, orientation="vertical")
        vsb.pack(side="right", fill="y")

        inner = tk.Frame(wrap, bg=self.colors["editor_bg"])
        inner.pack(side="left", fill="both", expand=True, padx=1, pady=1)

        self.logs_text = tk.Text(
            inner, wrap="word", state="disabled", padx=10, pady=10, border=0,
            font=("Consolas", 12), bg=self.colors["editor_bg"], fg=self.colors["editor_fg"],
            highlightthickness=0,
        )
        self.logs_text.pack(side="left", fill="both", expand=True)
        vsb.configure(command=self.logs_text.yview)
        self.logs_text.configure(yscrollcommand=vsb.set)

    # -----------------------------------------------------------------
    # STATUS BAR
    # -----------------------------------------------------------------

    def _build_statusbar(self):
        bar = ctk.CTkFrame(self, fg_color=self.colors["card"], corner_radius=0, height=30)
        bar.pack(side="bottom", fill="x")
        bar.pack_propagate(False)
        self.status_label = ctk.CTkLabel(
            bar, text="Listo", text_color=self.colors["muted"],
            font=ctk.CTkFont(size=11), anchor="w",
        )
        self.status_label.pack(side="left", padx=14)

    def _set_status(self, text):
        self.status_label.configure(text=text)

    # -----------------------------------------------------------------
    # ACCIONES
    # -----------------------------------------------------------------

    def load_file(self):
        initial_dir = "pruebas" if os.path.isdir("pruebas") else "."
        path = filedialog.askopenfilename(
            title="Cargar archivo Go",
            initialdir=initial_dir,
            filetypes=[("Archivos Go", "*.go"), ("Todos los archivos", "*.*")],
        )
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.code_text.delete("1.0", "end")
        self.code_text.insert("1.0", content)
        self._refresh_line_numbers()
        self._highlight_syntax()
        self.current_file = path
        self._set_status(f"Listo | Código cargado desde: `{os.path.basename(path)}`")

    def save_file(self):
        path = filedialog.asksaveasfilename(
            title="Guardar archivo Go",
            initialdir="pruebas" if os.path.isdir("pruebas") else ".",
            defaultextension=".go",
            filetypes=[("Archivos Go", "*.go"), ("Todos los archivos", "*.*")],
            initialfile=os.path.basename(self.current_file) if self.current_file else "codigo.go",
        )
        if not path:
            return
        code = self.code_text.get("1.0", "end-1c")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        self.current_file = path
        self._set_status(f"Listo | Guardado en: `{os.path.basename(path)}`")

    def clear_editor(self):
        self.code_text.delete("1.0", "end")
        self._refresh_line_numbers()
        self.current_file = None
        self.last_result = None
        self._reset_stats()
        self._render_placeholder(self.results_scroll, "Presiona “Analizar Código” para ver resultados.")
        self._render_symbol_table({})
        self._set_tree_text("(sin código analizado)")
        self._set_logs_text("Aún no se han generado logs en esta sesión.", info="Editor limpio.")
        self._set_status("Editor limpio")

    def run_analysis(self):
        code = self.code_text.get("1.0", "end-1c")
        if not code.strip():
            messagebox.showinfo("Analizar Código", "El editor está vacío. Escribe o carga código Go primero.")
            return

        result = self.analyzer.run(code)
        self.last_result = result

        total_errors = (
            len(result.lexical_errors) + len(result.syntax_errors) + len(result.semantic_errors)
        )

        self._update_stats(result)
        self._render_findings(result)
        self._render_symbol_table(result.symbol_table)
        self._set_tree_text(build_block_tree(result.tokens))

        try:
            log_file, sem_file = self.analyzer.write_logs(code, result, self.settings["author"])
            self.last_log_files = (log_file, sem_file)
            self._show_logs(log_file, sem_file)
        except Exception as exc:
            self._set_logs_text(f"No se pudieron generar los logs: {exc}")

        source = f"`{os.path.basename(self.current_file)}`" if self.current_file else "el editor"
        if total_errors == 0:
            self._set_status(f"Listo | Código analizado desde {source} | Último análisis completado exitosamente")
        else:
            self._set_status(
                f"Listo | Código analizado desde {source} | Último análisis completado con {total_errors} error(es)"
            )

    def export_json(self):
        if self.last_result is None:
            messagebox.showinfo("Exportar", "Ejecuta un análisis antes de exportar.")
            return
        path = filedialog.asksaveasfilename(
            title="Exportar resultados", defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Texto plano", "*.txt")],
            initialfile="analisis.json",
        )
        if not path:
            return
        data = {
            "tokens_reconocidos": len(self.last_result.tokens),
            "errores_lexicos": self.last_result.lexical_errors,
            "errores_sintacticos": self.last_result.syntax_errors,
            "errores_semanticos": self.last_result.semantic_errors,
            "tabla_simbolos": self.last_result.symbol_table,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self._set_status(f"Listo | Resultados exportados a `{os.path.basename(path)}`")

    # -----------------------------------------------------------------
    # RENDER HELPERS
    # -----------------------------------------------------------------

    def _reset_stats(self):
        for key in self.stat_rows:
            dot, val = self.stat_rows[key]
            val.configure(text="0")
            dot.configure(fg_color=self.colors["accent"] if key == "tokens" else self.colors["green"])

    def _update_stats(self, result):
        counts = {
            "tokens": len(result.tokens),
            "lexico": len(result.lexical_errors),
            "sintactico": len(result.syntax_errors),
            "semantico": len(result.semantic_errors),
        }
        for key, count in counts.items():
            dot, val = self.stat_rows[key]
            val.configure(text=str(count))
            if key == "tokens":
                dot.configure(fg_color=self.colors["accent"])
            else:
                dot.configure(fg_color=self.colors["green"] if count == 0 else self.colors["orange"])

    def _clear_scrollable(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def _render_placeholder(self, frame, text):
        self._clear_scrollable(frame)
        ctk.CTkLabel(frame, text=text, text_color=self.colors["muted"],
                     font=ctk.CTkFont(size=13)).pack(pady=20)

    def _render_findings(self, result):
        frame = self.results_scroll
        self._clear_scrollable(frame)
        findings = build_findings(result)

        if not findings:
            success = ctk.CTkFrame(frame, fg_color=self.colors["green"], corner_radius=8)
            success.pack(fill="x", pady=4)
            ctk.CTkLabel(
                success, text="✓  No se encontraron errores. Programa aceptado exitosamente.",
                text_color="#FFFFFF", font=ctk.CTkFont(size=13, weight="bold"), anchor="w",
            ).pack(fill="x", padx=12, pady=10)
            return

        for item in findings:
            row = ctk.CTkFrame(frame, fg_color=self.colors["red_bg"], corner_radius=8)
            row.pack(fill="x", pady=4)
            text = f"Línea {item['line']}: Error {item['type']} - {item['message']}"
            ctk.CTkLabel(
                row, text=f"⚠  {text}", text_color=self.colors["red"],
                font=ctk.CTkFont(size=12, weight="bold"), anchor="w", justify="left",
                wraplength=380,
            ).pack(fill="x", padx=12, pady=8)

    def _render_symbol_table(self, symbol_table):
        frame = self.symbols_scroll
        self._clear_scrollable(frame)

        header = ctk.CTkFrame(frame, fg_color=self.colors["bg"], corner_radius=6)
        header.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(header, text="Nombre", text_color=self.colors["muted"],
                     font=ctk.CTkFont(size=12, weight="bold"), width=180, anchor="w").pack(
            side="left", padx=12, pady=8)
        ctk.CTkLabel(header, text="Tipo", text_color=self.colors["muted"],
                     font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(
            side="left", padx=12, pady=8)

        if not symbol_table:
            ctk.CTkLabel(frame, text="La tabla de símbolos está vacía.",
                         text_color=self.colors["muted"], font=ctk.CTkFont(size=13)).pack(pady=16)
            return

        for i, (name, type_) in enumerate(sorted(symbol_table.items())):
            bg = self.colors["card"] if i % 2 == 0 else self.colors["bg"]
            row = ctk.CTkFrame(frame, fg_color=bg, corner_radius=6)
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=name, text_color=self.colors["text"],
                         font=ctk.CTkFont(size=13, family="Consolas"), width=180, anchor="w").pack(
                side="left", padx=12, pady=6)
            ctk.CTkLabel(row, text=type_, text_color=self.colors["accent"],
                         font=ctk.CTkFont(size=13, weight="bold"), anchor="w").pack(
                side="left", padx=12, pady=6)

    def _set_tree_text(self, content):
        self.tree_text.configure(state="normal")
        self.tree_text.delete("1.0", "end")
        self.tree_text.insert("1.0", content)
        self.tree_text.configure(state="disabled")

    def _set_logs_text(self, content, info=None):
        if info is not None:
            self.logs_info.configure(text=info)
        self.logs_text.configure(state="normal")
        self.logs_text.delete("1.0", "end")
        self.logs_text.insert("1.0", content)
        self.logs_text.configure(state="disabled")

    def _show_logs(self, log_file, sem_file):
        parts = []
        if log_file and os.path.isfile(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                parts.append(f"===== {log_file} =====\n{f.read()}")
        if sem_file and os.path.isfile(sem_file):
            with open(sem_file, "r", encoding="utf-8") as f:
                parts.append(f"===== {sem_file} =====\n{f.read()}")
        info = f"Archivos generados: {log_file or '-'} | {sem_file or '-'}"
        self._set_logs_text("\n\n".join(parts) if parts else "No se generó contenido de log.", info=info)

    # -----------------------------------------------------------------
    # CONFIGURACIÓN
    # -----------------------------------------------------------------

    def open_settings(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Configuración")
        dialog.geometry("380x300")
        dialog.configure(fg_color=self.colors["bg"])
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Desarrollador (para nombres de log)",
                     text_color=self.colors["text"], font=ctk.CTkFont(size=13)).pack(
            anchor="w", padx=20, pady=(20, 4))
        author_combo = ctk.CTkComboBox(dialog, values=AUTHORS, width=320)
        author_combo.set(self.settings["author"])
        author_combo.pack(padx=20, pady=(0, 16))

        ctk.CTkLabel(dialog, text="Tema visual",
                     text_color=self.colors["text"], font=ctk.CTkFont(size=13)).pack(
            anchor="w", padx=20, pady=(0, 4))
        theme_seg = ctk.CTkSegmentedButton(dialog, values=["Light", "Dark"])
        theme_seg.set(self.settings["theme"])
        theme_seg.pack(padx=20, pady=(0, 16), fill="x")

        ctk.CTkLabel(dialog, text="Tamaño de fuente del editor",
                     text_color=self.colors["text"], font=ctk.CTkFont(size=13)).pack(
            anchor="w", padx=20, pady=(0, 4))
        font_slider = ctk.CTkSlider(dialog, from_=10, to=20, number_of_steps=10)
        font_slider.set(self.settings["font_size"])
        font_slider.pack(padx=20, pady=(0, 20), fill="x")

        def apply_and_close():
            self.settings["author"] = author_combo.get()
            new_theme = theme_seg.get()
            new_font_size = int(font_slider.get())
            theme_changed = new_theme != self.settings["theme"]
            font_changed = new_font_size != self.settings["font_size"]
            self.settings["theme"] = new_theme
            self.settings["font_size"] = new_font_size

            dialog.destroy()

            if theme_changed:
                self._apply_theme()
            elif font_changed:
                self.code_text.configure(font=("Consolas", self.settings["font_size"]))
                self.line_numbers.configure(font=("Consolas", self.settings["font_size"]))
                self._highlight_syntax()

        ctk.CTkButton(
            dialog, text="Guardar configuración", command=apply_and_close,
            fg_color=self.colors["accent"], hover_color=self.colors["accent_hover"],
            corner_radius=8,
        ).pack(padx=20, pady=(0, 20), fill="x")

    def _apply_theme(self):
        ctk.set_appearance_mode(self.settings["theme"])
        self.colors = PALETTE[self.settings["theme"]]

        code = self.code_text.get("1.0", "end-1c")
        current_file = self.current_file
        last_result = self.last_result
        last_log_files = self.last_log_files

        for widget in self.winfo_children():
            widget.destroy()

        self.configure(fg_color=self.colors["bg"])
        self._build_toolbar()
        self._build_main()
        self._build_statusbar()

        self.code_text.insert("1.0", code)
        self.current_file = current_file
        self.last_result = last_result
        self.last_log_files = last_log_files
        self._refresh_line_numbers()
        self._highlight_syntax()

        if last_result is not None:
            self._update_stats(last_result)
            self._render_findings(last_result)
            self._render_symbol_table(last_result.symbol_table)
            self._set_tree_text(build_block_tree(last_result.tokens))

        if last_log_files is not None:
            self._show_logs(*last_log_files)

        source = f"`{os.path.basename(current_file)}`" if current_file else "el editor"
        self._set_status(f"Listo | Tema aplicado: {self.settings['theme']} | Código desde {source}")


def main():
    app = GoAnalyzerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
