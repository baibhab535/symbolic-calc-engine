from lark import Lark, Transformer
from ast_nodes import Number, Variable, Add, Subtract, Multiply, Divide, Power, Function

math_grammar = """
    ?start: expr

    ?expr: expr "+" term     -> add
         | expr "-" term     -> subtract
         | term
         
    ?term: term "*" factor   -> multiply
         | term "/" factor   -> divide
         | factor
         
    ?factor: base "^" factor -> power
           | base
           
    ?base: NUMBER            -> number
         | CNAME             -> variable
         | CNAME "(" expr ")" -> function
         | "(" expr ")"
     
    ?value: NUMBER           -> number
         | CNAME            -> var
         | "-" value        -> neg      // <-- ADD THIS LINE
         | "(" expr ")"

    %import common.NUMBER
    %import common.CNAME
    %import common.WS
    %ignore WS
"""

class MathTransformer(Transformer):
    def number(self, args): return Number(float(args[0]))
    def variable(self, args): return Variable(str(args[0]))
    def add(self, args): return Add(args[0], args[1])
    def subtract(self, args): return Subtract(args[0], args[1])
    def multiply(self, args): return Multiply(args[0], args[1])
    def divide(self, args): return Divide(args[0], args[1])
    def power(self, args): return Power(args[0], args[1])
    def function(self, args): return Function(str(args[0]), args[1])
    def neg(self, args):
        # Translates -x into (-1 * x)
        return Multiply(Number(-1), args[0])
parser = Lark(math_grammar, parser='lalr', transformer=MathTransformer())

def parse_math(text: str):
    return parser.parse(text)