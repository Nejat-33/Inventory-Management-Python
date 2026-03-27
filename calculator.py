import math
import sympy
from pathlib import Path

from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

transformations = (standard_transformations + (implicit_multiplication_application, convert_xor))

class FuturisticCalculator:
    def __init__(self):
        # --- Constants & State ---
        self.stack = []
        self.output = []
        self.mode = 'radian'
        self.history_file = Path("calculation_file.txt")

        # VARIABLE MEMORY SYSTEM
        self.variables = {
            "pi": math.pi,
            "e": math.e,
            "ans": 0
        }

        self.precedence = {
            "!": 5, "sin": 4, "cos": 4, "tan": 4, "asin": 4, "acos": 4, "atan": 4,
            "log": 4, "ln": 4, "sqrt": 3, "^": 3, "*": 2, "/": 2, "%": 2, "+": 1, "-": 1, "(": 0
        }

        self.scientific_ops = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "log": math.log10, "ln": math.log, "sqrt": math.sqrt
        }

    # --- 1. FILE & HISTORY LOGIC ---
    def read_history(self):
        if self.history_file.exists() and self.history_file.stat().st_size > 0:
            print("\n--- History ---\n" + self.history_file.read_text())
        else:
            print(" No history found.")

    def save_to_history(self, entry):
        with self.history_file.open('a') as f:
            f.write(entry + '\n')

    def clear_history(self):
        self.history_file.write_text("")
        print("History cleared.")


    def is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def handle_variables(self, tokens):
        new_tokens = []
        for t in tokens:
            if t in self.variables:
                new_tokens.append(str(self.variables[t]))
            else:
                new_tokens.append(t)
        return new_tokens

    def handle_negatives(self, tokens):
        new_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] == '-' and (i == 0 or tokens[i - 1] in ['+', '-', '*', '/', '(', '%', '!', '^']):
                if i + 1 < len(tokens):
                    new_tokens.append("-" + tokens[i + 1])
                    i += 2
                    continue
            new_tokens.append(tokens[i])
            i += 1
        return new_tokens


    def validate(self, tokens):
        sta = []
        for t in tokens:
            if t == '(':
                sta.append(t)
            elif t == ')':
                if not sta: return "Unbalanced Parenthesis"
                sta.pop()
        if sta: return "Unbalanced Parenthesis"

        # Placement
        binary_ops = {'+', '-', '*', '/', '%', '^'}
        if tokens[-1] in binary_ops: return "Ends with operator"

        return True


    def evaluate_postfix(self, postfix_tokens):
        num_stack = []
        ops = {'+', '-', '*', '/', '%', '^', '!'}

        for token in postfix_tokens:
            if self.is_number(token):
                num_stack.append(float(token))
            elif token in self.scientific_ops:
                val = num_stack.pop()
                if token in ['sin', 'cos', 'tan']:
                    if self.mode == 'degree':
                        val = math.radians(val)
                    result = (self.scientific_ops[token](val))
                elif token in ['asin', 'acos', 'atan']:
                    result = self.scientific_ops[token](val)
                    if self.mode == 'degree':
                        result = math.degrees(result)
                else:
                    result = self.scientific_ops[token](val)
                num_stack.append(result)
            elif token in ops:
                if token == '!':
                    num_stack.append(float(math.factorial(int(num_stack.pop()))))
                else:
                    n1 = num_stack.pop()
                    n2 = num_stack.pop()
                    if token == '+':
                        num_stack.append(n2 + n1)
                    elif token == '-':
                        num_stack.append(n2 - n1)
                    elif token == '*':
                        num_stack.append(n2 * n1)
                    elif token == '/':
                        num_stack.append(n2 / n1)
                    elif token == '%':
                        num_stack.append(n2 % n1)
                    elif token == '^':
                        num_stack.append(n2 ** n1)
        print("post fix", num_stack)
        return num_stack[0]

    def solve_derivative(self, userinput):
        expre = userinput.replace('deff', '')
        x = sympy.Symbol('x')
        result = sympy.solve(expre, x)
        return f"derivative: {result}"

    def solve_integration(self, userinput):
        expr = userinput.replace('integ', "")
        x= sympy.Symbol('x')
        result = sympy.integrate(expr, x)
        return  f"integration {result}"

    def solve_eq(self, userinput):
      try:
        equ = userinput.replace("solve", "")
        if "=" not in equ:
            return " Error: Missing '=' sign"
        lhs, rhs = equ.split("=")
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        x = sympy.Symbol('x')
        result = sympy.solve(lhs-lhs, x)
        if not result:
            return "No solution found."
        return f"x = {result}"
      except Exception as e:
          return f"error happen: {e}"


    def solve_limit(self, userinput):
        part = userinput.split()
        expr = sympy.parse_expr(part[1])
        var = sympy.Symbol(part[2])
        point = float(part[3])
        return sympy.limit(expr, var, point)

    def solve_matrix(self, userinput):
        raw = userinput.replace("matrix", "").strip()
        # If user wants inverse
        if "inv" in raw:
            m_str = raw.replace("inv", "").strip()
            return sympy.Matrix(sympy.sympify(m_str)).inv()
        # Otherwise just return the matrix
        return sympy.Matrix(sympy.sympify(raw))

    def process_input(self, user_input):
        user_input = user_input

        # A. Variable Assignment (e.g., x = 10 + 2)
        target_var = None
        if user_input.startswith('diff'):
            return self.solve_derivative(user_input)
        elif user_input.startswith('solve'):
            return self.solve_eq(user_input)
        elif user_input.startswith('limit'):
            return self.solve_limit(user_input)
        elif user_input.startswith('matrix'):
            return self.solve_matrix(user_input)
        elif user_input.startswith('int'):
            return self.solve_integration(user_input)
        elif "=" in user_input and "==" not in user_input:
            parts = user_input.split("=")
            target_var = parts[0].strip()
            user_input = parts[1].strip()

        # B. Tokenization & Variable Replacement
        tokens = user_input.split()
        tokens = self.handle_variables(tokens)
        tokens = self.handle_negatives(tokens)

        # C. Validation
        val_status = self.validate(tokens)
        if val_status is not True:
            print(f" {val_status}")
            return

        # D. Shunting-Yard
        self.output = []
        self.stack = []
        for t in tokens:
            if self.is_number(t):
                self.output.append(t)
            elif t == '(':
                self.stack.append(t)
            elif t == ')':
                while self.stack and self.stack[-1] != '(':
                    self.output.append(self.stack.pop())
                self.stack.pop()
            else:
                while self.stack and self.precedence.get(self.stack[-1], 0) >= self.precedence.get(t, 0):
                    self.output.append(self.stack.pop())
                self.stack.append(t)
        while self.stack: self.output.append(self.stack.pop())
        print(self.output)
        # E. Evaluation
        try:
            result = self.evaluate_postfix(self.output)
            print(f"Result: {result}")

            # Save to Memory
            self.variables["ans"] = result
            if target_var:
                self.variables[target_var] = result
                print(f" Saved to variable '{target_var}'")

            self.save_to_history(f"{user_input} = {result}")
        except Exception as e:
            print(f" Math Error: {e}")


# --- 6. RUNNER ---
calc = FuturisticCalculator()

while True:
    print(f"\n [ current Mode: {calc.mode.upper()} ]")
    print("\n[ 1:History | 2:Clear | 3:Deg/Rad | 4:Exit | Or type Math ]")
    choice = input(">>> ").strip().lower()

    if choice == '1':
        calc.read_history()
    elif choice == '2':
        calc.clear_history()
    elif choice == '3':
        calc.mode = 'degree' if calc.mode == 'radian' else 'radian'
        print(f"switched to {calc.mode.upper()}")
    elif choice == '4':
        break
    elif choice.startswith("solve"):
        # You MUST print the return value of solve_eq
        result = calc.solve_eq(choice)
        print(result)
        calc.save_to_history(f"Input: {choice} | Result: {result}")

    elif choice.startswith("deff"):
        print(calc.solve_derivative(choice))
    else:
        calc.process_input(choice)

