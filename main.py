import customtkinter as ctk
from calculator import CalculatorApp
from calculator.themes import get_theme_path

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme(get_theme_path())
    app = CalculatorApp()
    app.mainloop()