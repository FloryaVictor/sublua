from typing import Union


class Node:
    def __init__(self) -> None:
        pass

class Statement(Node):
    pass

class Program(Node):
    def __init__(self, statements: list[Statement]) -> None:
        self.statements = statements

# Expressions
class Expr(Node): pass

class OrExpr(Expr): pass
        
class AndExpr(Expr): pass

class EqExpr(Expr):  pass

class CmpExpr(Expr): pass

class AddExpr(Expr): pass

class MulExpr(Expr):pass

class UnaryExpr(Expr):pass

class ValueExpr(Expr): pass

class Value(Expr):pass

class CallExpr: pass



class OrExpr(Expr):
    def __init__(self, exprs: list[AndExpr]) -> None:
        self.exprs = exprs

class AndExpr(Expr):
    def __init__(self, exprs: list[EqExpr]) -> None:
        self.exprs = exprs

class EqExpr(Expr):
    def __init__(self, exprs: list[CmpExpr]) -> None:
        self.exprs = exprs

class CmpExpr(Expr):
    def __init__(self, exprs: list[AddExpr]) -> None:
        self.exprs = exprs

class AddExpr(Expr):
    def __init__(self, exprs: list[MulExpr]) -> None:
        self.exprs = exprs

class MulExpr(Expr):
    def __init__(self, exprs: list[UnaryExpr]) -> None:
        self.exprs = exprs

class UnaryExpr(Expr):
    def __init__(self, unaryPrefix: list[str]) -> None:
        self.unaryPrefix = unaryPrefix

class ValueExpr(Expr):
    def __init__(self, value: Union[str, Value, Expr, CallExpr], type:int) -> None:
        self.value = value
        self.type = type

class Value(Expr):
    def __init__(self, value: str, type:int) -> None:
        self.value = value
        self.type = type

class CallExpr(Expr):
    def __init__(self, name: str, argList:list[Expr]) -> None:
        self.name = name
        self.argList = argList


# Statements
class IfStatement(Statement):
    def __init__(self, thenBr: Program, elseBr: Program = None) -> None:
        self.thenBr = thenBr
        self.elseBr = elseBr


class WhileStatement(Statement):
    def __init__(self, cond: Expr, loop: Program) -> None:
        self.cond = cond
        self.loop = loop

class ReturnStatement(Statement):
    def __init__(self, result: Expr = None) -> None:
        self.result = result


class BreakStatement(Statement):
    pass

# Declarations
class Declaration(Statement):
    pass

class VarDeclaration(Declaration):
    def __init__(self, name: str, value: Expr) -> None:
        self.name = name
        self.value = value


class FunctionDeclaration(Declaration):
    def __init__(self, name: str, argList: list[str] = None, body: Program = None) -> None:
        self.name = name
        self.argList = argList
        self.body = body

