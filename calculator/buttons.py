import customtkinter as ctk
from .constants import BUTTON_FONT

def create_buttons(app):
    button_grid = [
        ["C", "⌫", "ClsHist", "Hist", "RAD", "DEG"],
        ["sin", "cos", "tan", "asin", "acos", "atan"],
        ["log", "ln", "10^x", "exp", "x²", "x³"],
        ["√", "∛", "^", "π", "e", "n!"],
        ["7", "8", "9", "/", "nCr", "nPr"],
        ["4", "5", "6", "*", "(", ")"],
        ["1", "2", "3", "-", "", ""],
        ["0", ".", "=", "+", "", ""]
    ]
    
    for i, row in enumerate(button_grid):
        app.button_frame.grid_rowconfigure(i, weight=1)
        for j, symbol in enumerate(row):
            app.button_frame.grid_columnconfigure(j, weight=1)
            if symbol:
                btn = ctk.CTkButton(
                    app.button_frame,
                    text=symbol,
                    font=BUTTON_FONT,
                    command=lambda s=symbol: app.button_press(s)
                )
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
