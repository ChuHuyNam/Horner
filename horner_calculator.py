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
    def __init__(self) -> None:
        super().__init__()
        self.title("Máy tính đa thức bậc 5")
        self.geometry("1040x650")
        self.minsize(820, 560)
        self.entries: list[ttk.Entry] = []
        self._configure_styles()
        self._build_interface()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Formula.TLabel", font=("Cambria Math", 14), foreground="#444444")
        style.configure("Result.TLabel", font=("Segoe UI", 22, "bold"), foreground="#1257a6")
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=(20, 9))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=31)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=7)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(16, 8))

    def _build_interface(self) -> None:
        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Máy tính đa thức bậc 5", style="Title.TLabel").pack()
        ttk.Label(
            container,
            text="f(x) = a₁x⁵ + a₂x⁴ + a₃x³ + a₄x² + a₅x + a₆",
            style="Formula.TLabel",
        ).pack(pady=(5, 20))

        input_group = ttk.LabelFrame(container, text="Nhập hệ số", padding=14)
        input_group.pack(fill="x")
        for column in range(7):
            input_group.columnconfigure(column, weight=1)

        for index in range(6):
            cell = ttk.Frame(input_group)
            cell.grid(row=0, column=index, sticky="ew", padx=5)
            ttk.Label(cell, text=f"a{index + 1}").pack(anchor="center")
            entry = ttk.Entry(cell, width=10, justify="center", font=("Segoe UI", 11))
            entry.pack(fill="x", pady=(4, 0), ipady=4)
            self.entries.append(entry)

        x_cell = ttk.Frame(input_group)
        x_cell.grid(row=0, column=6, sticky="ew", padx=5)
        ttk.Label(x_cell, text="x").pack(anchor="center")
        self.x_entry = ttk.Entry(x_cell, width=10, justify="center", font=("Segoe UI", 11))
        self.x_entry.pack(fill="x", pady=(4, 0), ipady=4)

        ttk.Button(container, text="Tính", command=self.calculate).pack(pady=15)
        self.bind("<Return>", lambda _event: self.calculate())

        self.result_label = ttk.Label(
            container,
            text="Nhập dữ liệu rồi nhấn Tính",
            style="Result.TLabel",
            anchor="center",
        )
        self.result_label.pack(fill="x", pady=(0, 5))
        self.expression_label = ttk.Label(container, text="", anchor="center", justify="center")
        self.expression_label.pack(fill="x", pady=(0, 12))

        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)
        self.horner_tree = self._create_tree(
            notebook,
            ("k", "coefficient", "calculation", "result"),
            ("k", "Hệ số", "Phép tính Horner", "b[k]"),
            (55, 100, 430, 120),
        )
        self.direct_tree = self._create_tree(
            notebook,
            ("i", "term", "value", "total"),
            ("i", "Hạng tử", "Giá trị", "Tổng tích lũy"),
            (55, 350, 130, 150),
        )
        notebook.add(self.horner_tree.master, text="Horner")
        notebook.add(self.direct_tree.master, text="Phương pháp lặp")

    def _create_tree(
        self,
        parent: ttk.Notebook,
        columns: tuple[str, ...],
        headings: tuple[str, ...],
        widths: tuple[int, ...],
    ) -> ttk.Treeview:
        frame = ttk.Frame(parent, padding=5)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=6)
        for column, heading, width in zip(columns, headings, widths):
            tree.heading(column, text=heading)
            anchor = "center" if column in {"k", "i", "coefficient", "result", "value", "total"} else "w"
            tree.column(column, width=width, minwidth=55, anchor=anchor)
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)
        return tree

    def calculate(self) -> None:
        try:
            coefficients = [float(entry.get().strip().replace(",", ".")) for entry in self.entries]
            x = float(self.x_entry.get().strip().replace(",", "."))
            if not all(math.isfinite(value) for value in [*coefficients, x]):
                raise ValueError
        except ValueError:
            messagebox.showerror("Dữ liệu không hợp lệ", "Hãy nhập đủ 6 hệ số và giá trị x.")
            return

        horner_result, horner_steps = evaluate_horner(coefficients, x)
        direct_result, direct_steps = evaluate_direct(coefficients, x)
        self.result_label.configure(text=f"f({format_number(x)}) = {format_number(horner_result)}")
        self.expression_label.configure(text=self._horner_expression(coefficients, x))
        self._fill_tree(self.horner_tree, horner_steps)
        direct_rows = [
            (index, term, format_number(value), format_number(total))
            for index, term, value, total in direct_steps
        ]
        self._fill_tree(self.direct_tree, direct_rows)

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
            expression = f"({expression}) × {format_number(x)} {sign} {format_number(abs(coefficient))}"
        return f"Horner: {expression}"

if __name__ == "__main__":
    HornerCalculator().mainloop()
