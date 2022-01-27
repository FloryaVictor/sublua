from typing import Union


class Node:
    def __init__(self) -> None:
        pass

    def children(self) -> list:
        return []

    def __str__(self) -> str:
        return ""


class Statement(Node):
    pass

class StatementList(Node):
    def __init__(self, statements: list[Statement]) -> None:
        self.statements = statements

    def children(self) -> list:
        return self.statements

    def __str__(self) -> str:
        return "StatementList"

class Program(Node):
    def __init__(self, statements: StatementList) -> None:
        self.statements = statements

    def children(self) -> list:
        return self.statements.children()

    def __str__(self) -> str:
        return "Program"

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

    def children(self) -> list:
        return self.exprs
    
    def __str__(self) -> str:
        return "OrExpr"
        
class AndExpr(Expr):
    def __init__(self, exprs: list[EqExpr]) -> None:
        self.exprs = exprs

    def children(self) -> list:
        return self.exprs
    
    def __str__(self) -> str:
        return "AndExpr"

class EqExpr(Expr):
    def __init__(self, exprs: list[CmpExpr], ops: list[str]) -> None:
        self.exprs = exprs
        self.ops = ops

    def children(self) -> list:
        return self.exprs

    def __str__(self) -> str:
        return f"EqExpr(ops: {self.ops})"


class CmpExpr(Expr):
    def __init__(self, exprs: list[AddExpr], ops: list[str]) -> None:
        self.exprs = exprs
        self.ops = ops

    def children(self) -> list:
        return self.exprs

    def __str__(self) -> str:
        return f"CmpExpr(ops: {self.ops})"


class AddExpr(Expr):
    def __init__(self, exprs: list[MulExpr],  ops: list[str]) -> None:
        self.exprs = exprs
        self.ops = ops

    def children(self) -> list:
        return self.exprs

    def __str__(self) -> str:
        return f"AddExpr(ops: {self.ops})"


class MulExpr(Expr):
    def __init__(self, exprs: list[UnaryExpr],  ops: list[str]) -> None:
        self.exprs = exprs
        self.ops = ops

    def children(self) -> list:
        return self.exprs

    def __str__(self) -> str:
        return f"MulExpr(ops: {self.ops})"


class UnaryExpr(Expr):
    def __init__(self, value: ValueExpr, ops: list[str]) -> None:
        self.value = value
        self.ops = ops

    def children(self) -> list:
        return [self.value]

    def __str__(self) -> str:
        return f"UnaryExpr(ops: {self.ops})"


class ValueExpr(Expr):
    def __init__(self, value: Union[str, Value, Expr, CallExpr], type:str) -> None:
        self.value = value
        self.type = type

    def children(self) -> list:
        if self.type != "id":
            return [self.value]
        return []
    
    def __str__(self) -> str:
        if self.type != "id":
            return f"ValueExpr({self.type})"
        return f"ValueExpr({self.type}: {self.value})"


class Value(Expr):
    def __init__(self, value: str, type:str) -> None:
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return f"Value({self.type}: {self.value})"


class CallExpr(Expr):
    def __init__(self, name: str, argList:list[Expr]) -> None:
        self.name = name
        self.argList = argList

    def children(self) -> list:
        return self.argList

    def __str__(self) -> str:
        return f"CallExpr({self.name})"

# Statements
class IfStatement(Statement):
    def __init__(self, cond: Expr, thenBr: StatementList = None, elseBr: StatementList = None) -> None:
        self.cond = cond
        self.thenBr = thenBr
        self.elseBr = elseBr

    def children(self) -> list:
        return [self.cond, self.thenBr, self.elseBr]

    def __str__(self) -> str:
        return "IfStatement"


class WhileStatement(Statement):
    def __init__(self, cond: Expr, loop: StatementList) -> None:
        self.cond = cond
        self.loop = loop

    def children(self) -> list:
        return [self.cond, self.loop]

    def __str__(self) -> str:
        return "WhileStatement"


class ReturnStatement(Statement):
    def __init__(self, result: Expr = None) -> None:
        self.result = result

    def children(self) -> list:
        return [self.result]
    
    def __str__(self) -> str:
        return "ReturnStatement"


class BreakStatement(Statement):
    pass

# Declarations
class Declaration(Statement):
    pass

class VarDeclaration(Declaration):
    def __init__(self, name: str, value: Expr) -> None:
        self.name = name
        self.value = value

    def children(self) -> list:
        return [self.value]
    
    def __str__(self) -> str:
        return f"VarDeclaration({self.name})"


class FunctionDeclaration(Declaration):
    def __init__(self, name: str, argList: list[str] = None, body: StatementList = None) -> None:
        self.name = name
        self.argList = argList
        self.body = body

    def children(self) -> list:
        return [self.body]
    
    def __str__(self) -> str:
        return f"FunctionDeclaration(name: {self.name}, args: {self.argList})"

