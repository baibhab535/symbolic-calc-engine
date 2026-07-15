from dataclasses import dataclass

class Expr:
    # This is the base class. All our math nodes will inherit from this.
    pass

@dataclass
class Number(Expr):
    value: float

@dataclass
class Variable(Expr):
    name: str

@dataclass
class Add(Expr):
    left: Expr
    right: Expr

@dataclass
class Multiply(Expr):
    left: Expr
    right: Expr

@dataclass
class Power(Expr):
    base: Expr
    exponent: Expr

@dataclass
class Function(Expr):
    name: str
    argument: Expr

@dataclass
class Subtract(Expr):
    left: Expr
    right: Expr

@dataclass
class Divide(Expr):
    left: Expr
    right: Expr

