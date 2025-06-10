import math
import re

class CalculatorEngine:
    """Core calculator engine handling evaluation, history, and mode management."""
    
    def __init__(self):
        self.current_input = ""
        self.history = []
        self.mode = "DEG"

    def fact(self, n):
        """Calculate factorial of integer n."""
        return math.factorial(int(n))

    def nCr(self, n, r):
        """Calculate combinations (n choose r)."""
        n, r = int(n), int(r)
        if r > n: return 0
        return math.comb(n, r)

    def nPr(self, n, r):
        """Calculate permutations (n permute r)."""
        n, r = int(n), int(r)
        if r > n: return 0
        return math.perm(n, r)

    def cbrt(self, x):
        """Calculate cube root of x."""
        return x ** (1 / 3)

    def preprocess(self, expr):
        """Convert calculator notation to Python-compatible math expressions."""
        expr = expr.replace(" ", "")
        
        expr = re.sub(r"√(\d*\.?\d+)", r"sqrt(\1)", expr)  # √5 → sqrt(5)
        expr = re.sub(r"∛(\d*\.?\d+)", r"cbrt(\1)", expr)  # ∛8 → cbrt(8)
        
        """other replacements"""
        expr = expr.replace("^", "**").replace("π", "pi").replace("√", "sqrt").replace("∛", "cbrt")
        expr = expr.replace("10^", "10**")

        """implicit multiplication"""
        expr = re.sub(r"(\d)(pi|e|sin|cos|tan|asin|acos|atan|sqrt|log|ln|exp|cbrt)", r"\1*\2", expr)
        expr = re.sub(r"(\d)\(", r"\1*(", expr)
        expr = re.sub(r"\)(pi|e|sin|cos|tan|asin|acos|atan|sqrt|log|ln|exp|cbrt)", r")*\1", expr)
        expr = re.sub(r"\)(\d)", r")*\1", expr)
        
       """factorials"""
        expr = re.sub(r"(\d+)!+", r"fact(\1)", expr)
        
        """combinations and permutations"""
        expr = expr.replace("nCr", "nCr")
        expr = expr.replace("nPr", "nPr")

        return self._convert_trig_mode(expr)

    def set_mode(self, mode):
        """Set angle mode (DEG or RAD)."""
        if mode.upper() in ["DEG", "RAD"]:
            self.mode = mode.upper()

    def _convert_trig_mode(self, expr):
        if self.mode == "RAD":
            return expr

        def convert(match):
            func, arg = match.group(1), match.group(2)
            try:
                angle = float(eval(arg, {"__builtins__": None}, {"pi": math.pi, "e": math.e}))
                return f"{func}(({arg})*pi/180)"
            except:
                return match.group(0)

        return re.sub(r"(sin|cos|tan|asin|acos|atan)\(([^)]+)\)", convert, expr)

    def is_safe(self, expr):
        """Check if expression contains potentially dangerous code."""
        banned = ["__", "import", "exec", "eval", "open", "file", "os", "sys", "subprocess", "input"]
        return not any(b in expr.lower() for b in banned)

    def evaluate(self, expr):
        """Evaluate a mathematical expression and return the result."""
        if not expr.strip():
            return "Error: Empty expression"

        original = expr
        expr = self.preprocess(expr)
        print(expr)

        if not self.is_safe(expr):
            return "Error: Unsafe expression"

        safe = {
            "__builtins__": {},
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "inf": float("inf"),
            "nan": float("nan"),
            "fact": self.fact,
            "nCr": self.nCr,
            "nPr": self.nPr,
            "cbrt": self.cbrt
        }

        try:
            result = eval(expr, {"__builtins__": {}}, safe)

            if isinstance(result, complex):
                if result.imag == 0:
                    result = result.real
                else:
                    result = f"{result.real:.10g}+{result.imag:.10g}i"

            if isinstance(result, float):
                if abs(result - round(result)) < 1e-10:
                    result = int(round(result))
                elif abs(result) < 1e-10:
                    result = 0
                elif abs(result) > 1e10:
                    result = f"{result:.6e}"
                else:
                    result = f"{result:.10g}"

            result_str = str(result)
            self.history.append(f"{original} = {result_str}")
            return result_str

        except ZeroDivisionError:
            return "Error: Division by zero"
        except ValueError as e:
            return f"Error: {str(e)}"
        except OverflowError:
            return "Error: Number too large"
        except SyntaxError:
            return "Error: Syntax"
        except Exception as e:
            return f"Error: {type(e).__name__}"

    def get_history(self):
        """Return calculation history."""
        return self.history.copy()

    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()

    def get_last_result(self):
        """Get the result of the last calculation."""
        if self.history:
            return self.history[-1].split(" = ")[-1]
        return None