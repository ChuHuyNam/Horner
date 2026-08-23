"""Desktop calculator for a fifth-degree polynomial."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, ttk


def format_number(value: float) -> str:
    if math.isclose(value, 0.0, abs_tol=1e-12):
        return "0"
    return f"{value:.12g}"


def evaluate_horner(coefficients: list[float], x: float) -> tuple[float, list[tuple]]:
    result = coefficients[0]
    steps = [(0, coefficients[0], f"b0 = {format_number(result)}", result)]
    for index, coefficient in enumerate(coefficients[1:], start=1):
        previous = result
        result = previous * x + coefficient
        sign = "+" if coefficient >= 0 else "-"
        calculation = f"{format_number(previous)} x {format_number(x)} {sign} {format_number(abs(coefficient))}"
        steps.append((index, coefficient, calculation, result))
    return result, steps


def evaluate_direct(coefficients: list[float], x: float) -> tuple[float, list[tuple]]:
    total = 0.0
    steps = []
    for index, coefficient in enumerate(coefficients):
        power = len(coefficients) - index - 1
        value = coefficient * x**power
        total += value
        term = f"{format_number(coefficient)} x ({format_number(x)})^{power}"
        steps.append((index + 1, term, value, total))
    return total, steps


class HornerCalculator(tk.Tk):
    COLORS = {"background": "#f4f2ec", "surface": "#ffffff", "ink": "#17211d", "muted": "#64706a", "green": "#1d5b43"}

    def __init__(self) -> None:
        super().__init__()
        self.title("Tính đa thức - Horner và phương pháp lặp")
        self.geometry("1120x720")
        self.minsize(900, 620)
        self.configure(bg=self.COLORS["background"])
        self.entries: list[ttk.Entry] = []
        self._configure_styles()
        self._build_interface()
        self.load_example()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=self.COLORS["background"])
        style.configure("Surface.TFrame", background=self.COLORS["surface"])
        style.configure("TLabel", background=self.COLORS["background"], foreground=self.COLORS["ink"], font=("Segoe UI", 11))
        style.configure("Surface.TLabel", background=self.COLORS["surface"], foreground=self.COLORS["ink"], font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground=self.COLORS["ink"])
        style.configure("Section.TLabel", background=self.COLORS["surface"], font=("Segoe UI", 14, "bold"))
        style.configure("Result.TLabel", background="#f4f2ec", foreground=self.COLORS["green"], font=("Segoe UI", 25, "bold"))
        style.configure("Accent.TButton", background=self.COLORS["green"], foreground="white", font=("Segoe UI", 11, "bold"), padding=10)
        style.map("Accent.TButton", background=[("active", "#154b36")])
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=32, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=(18, 9))

    def _build_interface(self) -> None:
        container = ttk.Frame(self, padding=28)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="Tính giá trị đa thức bậc 5", style="Title.TLabel").pack(anchor="w")
        ttk.Label(container, text="f(x) = a1x^5 + a2x^4 + a3x^3 + a4x^2 + a5x + a6", foreground=self.COLORS["muted"]).pack(anchor="w", pady=(4, 22))
        workspace = ttk.Frame(container)
        workspace.pack(fill="both", expand=True)
        workspace.columnconfigure(0, weight=2, minsize=320)
        workspace.columnconfigure(1, weight=5, minsize=520)
        workspace.rowconfigure(0, weight=1)
        self._build_input_panel(workspace)
        self._build_result_panel(workspace)

    def _build_input_panel(self, parent: ttk.Frame) -> None:
        panel = ttk.Frame(parent, style="Surface.TFrame", padding=24)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(panel, text="01  Dữ liệu đầu vào", style="Section.TLabel").pack(anchor="w", pady=(0, 20))
        coefficient_frame = ttk.Frame(panel, style="Surface.TFrame")
        coefficient_frame.pack(fill="x")
        for column in range(2):
            coefficient_frame.columnconfigure(column, weight=1)
        for index, default in enumerate([2, -3, 1, -4, 7, 8]):
            cell = ttk.Frame(coefficient_frame, style="Surface.TFrame")
            cell.grid(row=index // 2, column=index % 2, sticky="ew", padx=5, pady=7)
            ttk.Label(cell, text=f"a{index + 1}", style="Surface.TLabel").pack(anchor="w")
            entry = ttk.Entry(cell, font=("Segoe UI", 12))
            entry.insert(0, str(default))
            entry.pack(fill="x", pady=(4, 0), ipady=5)
            self.entries.append(entry)
        x_frame = ttk.Frame(panel, style="Surface.TFrame")
        x_frame.pack(fill="x", pady=(20, 8))
        ttk.Label(x_frame, text="Giá trị x", style="Surface.TLabel").pack(side="left")
        self.x_entry = ttk.Entry(x_frame, width=12, font=("Segoe UI", 12))
        self.x_entry.pack(side="right", ipady=5)
        ttk.Button(panel, text="Tính giá trị", style="Accent.TButton", command=self.calculate).pack(fill="x", pady=(18, 8))
        ttk.Button(panel, text="Dùng ví dụ trong giáo trình", command=self.load_example).pack(fill="x")
        self.bind("<Return>", lambda _event: self.calculate())

    def _build_result_panel(self, parent: ttk.Frame) -> None:
        panel = ttk.Frame(parent, style="Surface.TFrame", padding=24)
        panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        panel.rowconfigure(3, weight=1)
        panel.columnconfigure(0, weight=1)
        ttk.Label(panel, text="02  Kết quả", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        self.result_label = ttk.Label(panel, text="p(2) = 29", style="Result.TLabel", anchor="center")
        self.result_label.grid(row=1, column=0, sticky="ew", pady=18, ipady=12)
        self.expression_label = ttk.Label(panel, text="", style="Surface.TLabel", foreground=self.COLORS["green"], wraplength=680, justify="left")
        self.expression_label.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        notebook = ttk.Notebook(panel)
        notebook.grid(row=3, column=0, sticky="nsew")
        self.horner_tree = self._create_tree(notebook, ("k", "coefficient", "calculation", "result"), ("k", "Hệ số", "Phép tính Horner", "b[k]"), (55, 90, 350, 100))
        self.direct_tree = self._create_tree(notebook, ("i", "term", "value", "total"), ("i", "Hạng tử", "Giá trị", "Tổng tích lũy"), (55, 280, 110, 130))
        notebook.add(self.horner_tree.master, text="Horner")
        notebook.add(self.direct_tree.master, text="Phương pháp lặp")

    def _create_tree(self, parent: ttk.Notebook, columns: tuple[str, ...], headings: tuple[str, ...], widths: tuple[int, ...]) -> ttk.Treeview:
        frame = ttk.Frame(parent, style="Surface.TFrame")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
        for column, heading, width in zip(columns, headings, widths):
            tree.heading(column, text=heading)
            anchor = "center" if column in {"k", "i", "coefficient", "result", "value", "total"} else "w"
            tree.column(column, width=width, minwidth=50, anchor=anchor)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        return tree

    def load_example(self) -> None:
        for entry, value in zip(self.entries, [2, -3, 1, -4, 7, 8]):
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, "2")
        self.calculate()

    def calculate(self) -> None:
        try:
            coefficients = [float(entry.get().strip().replace(",", ".")) for entry in self.entries]
            x = float(self.x_entry.get().strip().replace(",", "."))
            if not all(math.isfinite(value) for value in [*coefficients, x]):
                raise ValueError
        except ValueError:
            messagebox.showerror("Dữ liệu không hợp lệ", "Vui lòng nhập đầy đủ các giá trị số hợp lệ.")
            return
        horner_result, horner_steps = evaluate_horner(coefficients, x)
        direct_result, direct_steps = evaluate_direct(coefficients, x)
        self.result_label.configure(text=f"p({format_number(x)}) = {format_number(horner_result)}")
        self.expression_label.configure(text=self._horner_expression(coefficients, x))
        self._fill_tree(self.horner_tree, horner_steps)
        rows = [(i, term, format_number(value), format_number(total)) for i, term, value, total in direct_steps]
        self._fill_tree(self.direct_tree, rows)
        tolerance = 1e-10 * max(1.0, abs(horner_result), abs(direct_result))
        if abs(horner_result - direct_result) > tolerance:
            messagebox.showwarning("Sai số", "Hai phương pháp có sai số vượt mức làm tròn dự kiến.")

    @staticmethod
    def _fill_tree(tree: ttk.Treeview, rows: list[tuple]) -> None:
        tree.delete(*tree.get_children())
        for row in rows:
            formatted = tuple(format_number(value) if isinstance(value, float) else value for value in row)
            tree.insert("", "end", values=formatted)

    @staticmethod
    def _horner_expression(coefficients: list[float], x: float) -> str:
        expression = format_number(coefficients[0])
        for coefficient in coefficients[1:]:
            sign = "+" if coefficient >= 0 else "-"
            expression = f"({expression}) x {format_number(x)} {sign} {format_number(abs(coefficient))}"
        return f"Horner: {expression}"


if __name__ == "__main__":
    HornerCalculator().mainloop()
