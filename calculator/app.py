import customtkinter as ctk
from .calculator import CalculatorEngine
from .constants import WIDTH, HEIGHT
from .buttons import create_buttons

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)
        self.calculator = CalculatorEngine()
        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.display = ctk.CTkEntry(self, font=("Roboto Mono", 30), justify="right", height=60)
        self.display.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        create_buttons(self)

    def button_press(self, symbol):
        if symbol == "=":
            expression = self.display.get()
            result = self.calculator.evaluate(expression)
            self.display.delete(0, "end")
            self.display.insert(0, result)

        elif symbol in ("⌫", "Back"):
            current = self.display.get()
            if current:
                self.display.delete(0, "end")
                self.display.insert(0, current[:-1])

        elif symbol == "C":
            self.display.delete(0, "end")

        elif symbol == "Hist":
            history = self.calculator.get_history()
            last_entry = history[-1] if history else "No history"
            self.display.delete(0, "end")
            self.display.insert(0, last_entry)

        elif symbol == "ClsHist":
            self.calculator.clear_history()
            self.display.delete(0, "end")
            self.display.insert(0, "History cleared")

        elif symbol == "LastAns":
            last = self.calculator.get_last_result()
            self.display.delete(0, "end")
            self.display.insert(0, last if last else "No last result")

        elif symbol == "DEG":
            self.calculator.set_mode("DEG")
            self.display.delete(0, "end")
            self.display.insert(0, "Mode: DEG")

        elif symbol == "RAD":
            self.calculator.set_mode("RAD")
            self.display.delete(0, "end")
            self.display.insert(0, "Mode: RAD")

        elif symbol in ("sin", "cos", "tan", "asin", "acos", "atan", "log", "ln", "sqrt", "cbrt", "exp"):
            self.display.insert("end", f"{symbol}(")

        elif symbol == "x²":
            self.display.insert("end", "**2")

        elif symbol == "x³":
            self.display.insert("end", "**3")

        elif symbol == "10^x":
            self.display.insert("end", "10^")

        elif symbol == "n!":
            self.display.insert("end", "!")

        elif symbol == "nCr":
            self.display.insert("end", "nCr(")

        elif symbol == "nPr":
            self.display.insert("end", "nPr(")

        elif symbol == "π":
            self.display.insert("end", "π")

        elif symbol == "e":
            self.display.insert("end", "e")

        else:
            self.display.insert("end", symbol)
