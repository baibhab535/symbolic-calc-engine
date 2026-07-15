from ast_nodes import Expr,Number, Variable, Add, Subtract, Multiply, Power, Divide ,Function
import math
import time
import os

def print_splash():
    # Clear terminal for a fresh boot-up feel
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ANSI Cyan color code
    CYAN = "\033[96m"
    RESET = "\033[0m"
    
    logo = f"""
{CYAN}
 ██████╗      ██╗  █████╗ ██╗   ██╗███████╗███████╗
 ██╔══██╗     ██║ ██╔══██╗╚██╗ ██╔╝██╔════╝██╔════╝
 ██████╔╝     ██║ ███████║ ╚████╔╝ █████╗  █████╗  
 ██╔══██╗██   ██║ ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══╝  
 ██████╔╝╚█████╔╝ ██║  ██║   ██║   ███████╗███████╗
 ╚═════╝  ╚════╝  ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝
{RESET}
    """
    
    print(logo)
    print("      COMPILER INITIALIZED SUCCESSFULLY")
    print("      ---------------------------------------")
    print("      Loading parsing libraries...")
    time.sleep(0.4) 
    print("      Verifying integration rules...")
    time.sleep(0.3)
    print("      System ready for input.\n")

if __name__ == "__main__":
    print_splash()
    # Your main loop logic goes here
```

### Step 2: Build the `main.exe`
Now that the branding is crisp, let’s package it. 

1.  Open your **VS Code Terminal**.
2.  Make sure you have `pyinstaller` installed (`pip install pyinstaller`).
3.  Run the build command:
    ```bash
    pyinstaller --onefile main.py
    ```

### Step 3: Verify the Build
Once that finishes:
1.  Look for a new folder called `dist/` in your `math_compiler` directory.
2.  Inside `dist/`, you will see `main.exe`.
3.  **Double-click it.** 

You should see the terminal window pop up, fill with that clean **BJAYEE** logo in Cyan, and pause exactly as you defined.

**Does that look like the logo you wanted?** If it does, your branding is done, and you are ready to ship this to your friends!
# The Master Rulebook for Functions
# Format: "function_name": lambda argument, variable: (Chain Rule AST)
DERIVATIVE_RULES = {
    "log": lambda arg, var: Divide(derive(arg, var), arg),
    "exp": lambda arg, var: Multiply(Function("exp", arg), derive(arg, var)),
    "sin": lambda arg, var: Multiply(Function("cos", arg), derive(arg, var)),
    "cos": lambda arg, var: Multiply(Multiply(Number(-1), Function("sin", arg)), derive(arg, var)),
    "tan": lambda arg, var: Multiply(Power(Function("sec", arg), Number(2)), derive(arg, var)),
    "cot": lambda arg, var: Multiply(Multiply(Number(-1), Power(Function("csc", arg), Number(2))), derive(arg, var)),
    "sec": lambda arg, var: Multiply(Multiply(Function("sec", arg), Function("tan", arg)), derive(arg, var)),
    "csc": lambda arg, var: Multiply(Multiply(Number(-1), Multiply(Function("csc", arg), Function("cot", arg))), derive(arg, var))
}

# ... existing code ...
def derive(expr, var):
    if isinstance(expr, Number):
        return Number(0.0)
    elif isinstance(expr, Variable):
        return Number(1.0) if expr.name == var else Number(0.0)
    elif isinstance(expr, Add):
        return Add(derive(expr.left, var), derive(expr.right, var))
    elif isinstance(expr, Subtract):
        return Subtract(derive(expr.left, var), derive(expr.right, var))
    elif isinstance(expr, Multiply):
        # Product Rule: u'v + uv'
        return Add(Multiply(derive(expr.left, var), expr.right), 
                   Multiply(expr.left, derive(expr.right, var)))
    elif isinstance(expr, Divide):
        # Quotient Rule: (u'v - uv') / v^2
        num = Subtract(Multiply(derive(expr.left, var), expr.right),
                       Multiply(expr.left, derive(expr.right, var)))
        den = Power(expr.right, Number(2.0))
        return Divide(num, den)
    elif isinstance(expr, Power):
        # Generalized Exponential & Power Rule
        if isinstance(expr.exponent, Number):
            n = expr.exponent.value
            new_pow = Power(expr.base, Number(n - 1.0))
            return Multiply(Multiply(Number(n), new_pow), derive(expr.base, var))
        else:
            term1 = Multiply(derive(expr.exponent, var), Function("log", expr.base))
            term2 = Multiply(expr.exponent, Divide(derive(expr.base, var), expr.base))
            return Multiply(expr, Add(term1, term2))
    elif isinstance(expr, Function):
        # Universal Chain Rule: f'(g(x)) * g'(x)
        inner_deriv = derive(expr.argument, var)
        name = expr.name
        if name == "sin":
            outer_deriv = Function("cos", expr.argument)
        elif name == "cos":
            outer_deriv = Multiply(Number(-1.0), Function("sin", expr.argument))
        elif name == "tan":
            outer_deriv = Divide(Number(1.0), Power(Function("cos", expr.argument), Number(2.0)))
        elif name == "exp":
            outer_deriv = Function("exp", expr.argument)
        elif name in ["log", "ln"]:
            outer_deriv = Divide(Number(1.0), expr.argument)
        elif name == "asin":
            outer_deriv = Divide(Number(1.0), Power(Subtract(Number(1.0), Power(expr.argument, Number(2.0))), Number(0.5)))
        elif name == "atan":
            outer_deriv = Divide(Number(1.0), Add(Number(1.0), Power(expr.argument, Number(2.0))))
        else:
            raise ValueError(f"Derivative of function '{name}' is not defined.")
        return Multiply(outer_deriv, inner_deriv)
    
    raise ValueError(f"Derivative rule for {type(expr).__name__} is not defined.")

def integrate(expr, var):
    # --- LEVEL 1: BASE CASES ---
    if isinstance(expr, Number):
        if expr.value == 0:
            return Number(0.0)
        return Multiply(expr, Variable(var))
        
    elif isinstance(expr, Variable):
        if expr.name == var:
            return Divide(Power(expr, Number(2.0)), Number(2.0))
        return Multiply(expr, Variable(var))

    # --- LEVEL 2: LINEARITY & LIATE BY-PARTS ---
    elif isinstance(expr, Add):
        return Add(integrate(expr.left, var), integrate(expr.right, var))
        
    elif isinstance(expr, Subtract):
        return Subtract(integrate(expr.left, var), integrate(expr.right, var))

    elif isinstance(expr, Multiply):
        if isinstance(expr.left, Number):
            return Multiply(expr.left, integrate(expr.right, var))
        elif isinstance(expr.right, Number):
            return Multiply(expr.right, integrate(expr.left, var))
            
        # The LIATE Algorithm (Integration by Parts)
        # Logarithmic, Inverse trig, Algebraic, Trigonometric, Exponential
        def liate_score(e):
            if isinstance(e, Function) and e.name in ["log", "ln"]: return 5
            if isinstance(e, Function) and e.name in ["asin", "acos", "atan"]: return 4
            if isinstance(e, (Variable, Power)): return 3
            if isinstance(e, Function) and e.name in ["sin", "cos", "tan"]: return 2
            if isinstance(e, Function) and e.name == "exp": return 1
            if isinstance(e, Power) and not isinstance(e.base, Variable): return 1
            return 0

        score_left = liate_score(expr.left)
        score_right = liate_score(expr.right)
        
        u, dv = (expr.left, expr.right) if score_left >= score_right else (expr.right, expr.left)
        
        try:
            v = integrate(dv, var)
            du = derive(u, var)
            v_du_integral = integrate(Multiply(v, du), var)
            return Subtract(Multiply(u, v), v_du_integral)
        except ValueError:
            pass
            
        raise ValueError(f"Integration by Parts failed for: {to_string(expr)}")

    # --- LEVEL 3: POWER & EXPONENTIAL (ORACLE U-SUB) ---
    elif isinstance(expr, Power):
        inner_deriv = derive(expr.base, var)
        try:
            val1 = evaluate(inner_deriv, var, 0.0)
            val2 = evaluate(inner_deriv, var, 1.0)
            
            if abs(val1 - val2) < 1e-9 and val1 != 0.0:
                coeff = Number(val1)
                if isinstance(expr.exponent, Number):
                    n = expr.exponent.value
                    if n == -1:
                        base_int = Function("log", expr.base)
                    else:
                        new_exponent = Number(n + 1.0)
                        base_int = Divide(Power(expr.base, new_exponent), new_exponent)
                    return base_int if coeff.value == 1 else Divide(base_int, coeff)
        except Exception:
            pass

        if isinstance(expr.exponent, Variable) and expr.exponent.name == var:
            return Divide(expr, Function("log", expr.base))

    # --- LEVEL 4: FUNCTIONS (ORACLE U-SUB) ---
    elif isinstance(expr, Function):
        inner_deriv = derive(expr.argument, var)
        try:
            val1 = evaluate(inner_deriv, var, 0.0)
            val2 = evaluate(inner_deriv, var, 1.0)
            
            if abs(val1 - val2) < 1e-9 and val1 != 0.0:
                coeff = Number(val1)
                name = expr.name
                if name == "sin":
                    base_int = Multiply(Number(-1.0), Function("cos", expr.argument))
                elif name == "cos":
                    base_int = Function("sin", expr.argument)
                elif name == "exp":
                    base_int = Function("exp", expr.argument)
                elif name == "tan":
                    base_int = Multiply(Number(-1.0), Function("log", Function("cos", expr.argument)))
                elif name in ["log", "ln"]:
                    base_int = Subtract(Multiply(expr.argument, Function("log", expr.argument)), expr.argument)
                else:
                    raise ValueError(f"Integration rule for {name} not defined.")
                    
                return base_int if coeff.value == 1 else Divide(base_int, coeff)
        except Exception:
            pass

    # --- LEVEL 5: FRACTIONS & QUOTIENTS ---
    elif isinstance(expr, Divide):
        if isinstance(expr.left, Number):
            return Multiply(expr.left, integrate(Divide(Number(1.0), expr.right), var))
        if isinstance(expr.right, Number):
            return Divide(integrate(expr.left, var), expr.right)
            
        # Logarithmic Quotient Integrator: int( f'(x) / f(x) ) = ln(f(x))
        den_deriv = derive(expr.right, var)
        try:
            ratio = Divide(expr.left, den_deriv)
            val1 = evaluate(ratio, var, 0.1)
            val2 = evaluate(ratio, var, 0.9)
            if abs(val1 - val2) < 1e-9 and val1 != 0.0:
                coeff = Number(val1)
                base_int = Function("log", expr.right)
                return base_int if coeff.value == 1 else Multiply(coeff, base_int)
        except Exception:
            pass
            
        raise ValueError(f"Quotient integration failed for: {to_string(expr)}")

    raise ValueError(f"Integration rule for this pattern is not defined yet: {to_string(expr)}")

def evaluate(expr, var_name, val):
    if isinstance(expr, Number):
        return float(expr.value)
    elif isinstance(expr, Variable):
        if expr.name == var_name:
            return val
        raise ValueError(f"Unknown variable in evaluation: {expr.name}")
    elif isinstance(expr, Add):
        return evaluate(expr.left, var_name, val) + evaluate(expr.right, var_name, val)
    elif isinstance(expr, Subtract):
        return evaluate(expr.left, var_name, val) - evaluate(expr.right, var_name, val)
    elif isinstance(expr, Multiply):
        return evaluate(expr.left, var_name, val) * evaluate(expr.right, var_name, val)
    elif isinstance(expr, Divide):
        denominator = evaluate(expr.right, var_name, val)
        if denominator == 0:
            raise ZeroDivisionError("Evaluation resulted in division by zero!")
        return evaluate(expr.left, var_name, val) / denominator
    elif isinstance(expr, Power):
        base = evaluate(expr.base, var_name, val)
        exponent = evaluate(expr.exponent, var_name, val)
        return math.pow(base, exponent)
    elif isinstance(expr, Function):
        arg = evaluate(expr.argument, var_name, val)
        name = expr.name
        if name == "sin": return math.sin(arg)
        elif name == "cos": return math.cos(arg)
        elif name == "tan": return math.tan(arg)
        elif name in ["log", "ln"]:
            if arg <= 0: raise ValueError(f"Logarithm domain error at x = {val}")
            return math.log(arg)
        elif name == "exp": return math.exp(arg)
        elif name == "asin":
            if arg < -1 or arg > 1: raise ValueError(f"Domain error for asin at x = {val}")
            return math.asin(arg)
        elif name == "atan": return math.atan(arg)
    raise ValueError(f"Cannot evaluate this pattern yet: {type(expr).__name__}")
# ... existing code ...




def simplify(expr: Expr) -> Expr:
    # 1. Base Cases (If you lose these, the whole tree collapses into 'None'!)
    if isinstance(expr, Number) or isinstance(expr, Variable):
        return expr
        
    # 2. Simplify Addition
    elif isinstance(expr, Add):
        left = simplify(expr.left)
        right = simplify(expr.right)
        
        if isinstance(left, Number) and left.value == 0:
            return right
        if isinstance(right, Number) and right.value == 0:
            return left
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value + right.value)
            
        return Add(left, right)
        
    # 3. Simplify Multiplication
    elif isinstance(expr, Multiply):
        left = simplify(expr.left)
        right = simplify(expr.right)
        
        if (isinstance(left, Number) and left.value == 0) or \
           (isinstance(right, Number) and right.value == 0):
            return Number(0)
        if isinstance(left, Number) and left.value == 1:
            return right
        if isinstance(right, Number) and right.value == 1:
            return left
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value * right.value)
            
        return Multiply(left, right)
        
    # 4. Simplify Subtraction
    elif isinstance(expr, Subtract):
        left = simplify(expr.left)
        right = simplify(expr.right)
        
        if isinstance(right, Number) and right.value == 0:
            return left
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value - right.value)
        if to_string(left) == to_string(right):
            return Number(0)
            
        return Subtract(left, right)
        
    # 5. Simplify Division (With Zero-Division Protection)
    elif isinstance(expr, Divide):
        left = simplify(expr.left)
        right = simplify(expr.right)
        
        # FATAL ERROR TRAP
        if isinstance(right, Number) and right.value == 0:
            raise ZeroDivisionError(f"Math Error: Division by zero is undefined! Cannot divide by {to_string(right)}")
            
        if isinstance(left, Number) and left.value == 0:
            return Number(0)
        if to_string(left) == to_string(right):
            return Number(1)
        if isinstance(right, Number) and right.value == 1:
            return left
            
        return Divide(left, right)
        
    # 6. Simplify Powers
    elif isinstance(expr, Power):
        base = simplify(expr.base)
        exponent = simplify(expr.exponent)
        
        if isinstance(exponent, Number) and exponent.value == 0:
            return Number(1)
        if isinstance(exponent, Number) and exponent.value == 1:
            return base
            
        return Power(base, exponent)
        
    # 7. Simplify Functions (With Domain Protection)
    elif isinstance(expr, Function):
        arg = simplify(expr.argument)
        
        # FATAL ERROR TRAP
        if expr.name == "log" and isinstance(arg, Number):
            if arg.value <= 0:
                raise ValueError(f"Domain Error: log({arg.value}) is mathematically undefined!")
                
        return Function(expr.name, arg)
        
    return expr

def to_string(expr: Expr) -> str:
    if isinstance(expr, Number):
        if isinstance(expr.value, int):
            return str(expr.value)
        return f"{int(expr.value)}" if expr.value.is_integer() else str(expr.value)
        
    elif isinstance(expr, Variable):
        return expr.name
        
    elif isinstance(expr, Add):
        return f"({to_string(expr.left)} + {to_string(expr.right)})"
        
    elif isinstance(expr, Subtract):
        return f"({to_string(expr.left)} - {to_string(expr.right)})"
        
    elif isinstance(expr, Multiply):
        return f"{to_string(expr.left)} * {to_string(expr.right)}"
        
    elif isinstance(expr, Divide):
        return f"({to_string(expr.left)} / {to_string(expr.right)})"
        
    elif isinstance(expr, Power):
        return f"{to_string(expr.base)}^{to_string(expr.exponent)}"
        
    elif isinstance(expr, Function):
        return f"{expr.name}({to_string(expr.argument)})"
        
    return str(expr)

def to_c_code(expr: Expr) -> str:
    """Translates the AST directly into C code syntax."""
    if isinstance(expr, Number):
        # C likes decimals for floating point math
        if isinstance(expr.value, int) or expr.value.is_integer():
            return f"{int(expr.value)}.0"
        return str(expr.value)
        
    elif isinstance(expr, Variable):
        return expr.name
        
    elif isinstance(expr, Add):
        return f"({to_c_code(expr.left)} + {to_c_code(expr.right)})"
        
    elif isinstance(expr, Subtract):
        return f"({to_c_code(expr.left)} - {to_c_code(expr.right)})"
        
    elif isinstance(expr, Multiply):
        return f"({to_c_code(expr.left)} * {to_c_code(expr.right)})"
        
    elif isinstance(expr, Divide):
        return f"({to_c_code(expr.left)} / {to_c_code(expr.right)})"
        
    elif isinstance(expr, Power):
        # C uses the pow() function from math.h, not ^
        return f"pow({to_c_code(expr.base)}, {to_c_code(expr.exponent)})"
        
    elif isinstance(expr, Function):
        # Most standard math functions share the same name in C's math.h
        return f"{expr.name}({to_c_code(expr.argument)})"
        
    return str(expr)

from math_parser import parse_math

# 2. Parse a raw string into our AST!
from math_parser import parse_math

print("=======================================")
print("  Welcome to the Math Compiler Engine  ")
print("  compute derivative and integration  ")
print("=======================================")

# The Read-Eval-Print Loop (REPL)
while True:
    try:
        # 1. UI MENU
        print("\n" + "="*30)
        print("   ADVANCED MATH COMPILER   ")
        print("="*30)
        print("1. Calculate Derivative")
        print("2. Calculate Indefinite Integral")
        print("3. Calculate Definite Integral (Area)")
        print("4. Quit")
        
        choice = input("\nSelect operation (1/2/3/4): ").strip()
        
        if choice == '4' or choice.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
            
        if choice not in ['1', '2', '3']:
            print("[!] Invalid choice. Please try again.")
            continue
            
        # 2. READ & PARSE
        user_input = input("\nEnter expression: ").strip()
        if not user_input:
            continue
            
        my_math_tree = parse_math(user_input)
        my_math_tree = simplify(my_math_tree)
        
        # 3. COMPUTE
        if choice == '1':
            raw_result = derive(my_math_tree, "x")
            clean_result = simplify(raw_result)
            print(f"\nDerivative: {to_string(clean_result)}")
            print(f"Compiled C: double result = {to_c_code(clean_result)};")
            
            # --- NEW: Evaluate Derivative at a Point ---
            eval_choice = input("\nEvaluate this derivative at a specific x value? (y/n): ").strip().lower()
            if eval_choice == 'y':
                x_val = float(input("Enter value for x: ").strip())
                numerical_result = evaluate(clean_result, "x", x_val)
                print(f"f'({x_val}) = {numerical_result:.4f}")
            
        elif choice == '2':
            base_integral = integrate(my_math_tree, "x")
            raw_result = Add(base_integral, Variable("C"))
            clean_result = simplify(raw_result)
            print(f"\nIntegral: {to_string(clean_result)}")
            print(f"Compiled C: double result = {to_c_code(clean_result)};")
            
        elif choice == '3':
            # Definite Integral Engine
            a_val = float(input("Enter lower bound (a): ").strip())
            b_val = float(input("Enter upper bound (b): ").strip())
            
            # Step A: Find the symbolic integral F(x)
            F_x = integrate(my_math_tree, "x")
            
            # Step B: Evaluate F(b) and F(a)
            F_b = evaluate(F_x, "x", b_val)
            F_a = evaluate(F_x, "x", a_val)
            
            # Step C: F(b) - F(a)
            area = F_b - F_a
            print(f"\nSymbolic Integral: {to_string(simplify(F_x))}")
            print(f"Total Area from {a_val} to {b_val}: {area:.4f}")
            
    except ZeroDivisionError as e:
        print(f"\n[!] Math Error: {e}")
    except ValueError as e:
        print(f"\n[!] Error: {e}")
    except Exception as e:
        print(f"\n[!] System Error: {e}")

print(f"--- Parsing: {user_input} ---")
my_math_tree = parse_math(user_input)

# 1. Show the original equation
print("Original Equation:")
print(to_string(my_math_tree))

# 2. Derive and Simplify
raw_derivative = derive(my_math_tree, "x")
clean_derivative = simplify(raw_derivative)

# 3. Show the final derivative
print("\nDerivative:")
print(to_string(clean_derivative))
