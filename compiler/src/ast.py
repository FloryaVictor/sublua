from typing import Union
from .IR import *


class CodegenError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
    
    def __str__(self) -> str:
        return self.msg


class FunctionInfo:
    def __init__(self, name: str, args: list[str], location: Instruction) -> None:
        self.name = name
        self.args = args
        self.location = location


class Namespace:
    def __init__(self) -> None:
        self.funcs = dict()


class CodegenContext:
    def __init__(self) -> None:
        self.namespaces = [Namespace()]
        self.loop_exits = []
        self.ti = 0
    
    def tmpName(self) -> str:
        name = f"_t{self.ti}"
        self.ti += 1
        return name
    

    def resolveFunc(self, name: str) -> Union[FunctionInfo, None]:
        for i in reversed(range(len(self.namespaces))):
            if name in self.namespaces[i].funcs:
                return self.namespaces[i].funcs[name]
        return None
    

    def create(self):
        self.namespaces.append(Namespace())
    
    def top(self) -> Namespace:
        return self.namespaces[-1]
    
    def drop(self) -> Namespace:
        return self.namespaces.pop()


class Node:
    def __init__(self) -> None:
        pass

    def children(self) -> list:
        return []

    def __str__(self) -> str:
        return ""
    

class Statement(Node):
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass

class StatementList(Node):
    def __init__(self, statements: list[Statement]) -> None:
        self.statements = statements

    def children(self) -> list:
        return self.statements

    def __str__(self) -> str:
        return "StatementList"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = []
        for statement in self.statements:
            code.extend(statement.codegen(context))
        return code


class Program(Node):
    def __init__(self, statements: StatementList) -> None:
        self.statements = statements

    def children(self) -> list:
        return self.statements.children()

    def __str__(self) -> str:
        return "Program"
    
    def codegen(self) -> list[Instruction]:
        context = CodegenContext()
        code = self.statements.codegen(context)
        code.append(EndInstruction())
        enumerate_instructions(code)
        code = remove_blanks(code)
        return code

# Expressions
class Expr(Node): pass

class OrExpr(Expr): 
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass

class AndExpr(Expr): 
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass

class EqExpr(Expr): 
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass

class CmpExpr(Expr): 
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass

class AddExpr(Expr): 
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass

class MulExpr(Expr):
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass

class UnaryExpr(Expr):
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass

class ValueExpr(Expr): 
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass

class Value(Expr):
    def codegen(self, context: CodegenContext) -> IRValue:
        pass

class CallExpr: 
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass



class OrExpr(Expr):
    def __init__(self, exprs: list[AndExpr]) -> None:
        self.exprs = exprs

    def children(self) -> list:
        return self.exprs
    
    def __str__(self) -> str:
        return "OrExpr"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = self.exprs[0].codegen(context)
        for i in range(1, len(self.exprs)):
            andExpr = self.exprs[i]
            last = code[-1]
            code.extend(andExpr.codegen(context))
            tmp = BinaryOpValue("or", last.lhs, code[-1].lhs)
            tmp_name = context.tmpName()
            code.append(AssignmentInstruction(tmp_name, tmp))
        return code

        
class AndExpr(Expr):
    def __init__(self, exprs: list[EqExpr]) -> None:
        self.exprs = exprs

    def children(self) -> list:
        return self.exprs
    
    def __str__(self) -> str:
        return "AndExpr"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = self.exprs[0].codegen(context)
        for i in range(1, len(self.exprs)):
            eqExpr = self.exprs[i]
            last = code[-1]
            code.extend(eqExpr.codegen(context))
            tmp = BinaryOpValue("and", last.lhs, code[-1].lhs)
            tmp_name = context.tmpName()
            code.append(AssignmentInstruction(tmp_name, tmp))
        return code

class EqExpr(Expr):
    def __init__(self, exprs: list[CmpExpr], ops: list[str]) -> None:
        self.exprs = exprs
        self.ops = ops

    def children(self) -> list:
        return self.exprs

    def __str__(self) -> str:
        return f"EqExpr(ops: {self.ops})"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = self.exprs[0].codegen(context)
        for i in range(1, len(self.exprs)):
            cmpExpr = self.exprs[i]
            last = code[-1]
            code.extend(cmpExpr.codegen(context))
            tmp = BinaryOpValue(self.ops[i - 1], last.lhs, code[-1].lhs)
            tmp_name = context.tmpName()
            code.append(AssignmentInstruction(tmp_name, tmp))
        return code


class CmpExpr(Expr):
    def __init__(self, exprs: list[AddExpr], ops: list[str]) -> None:
        self.exprs = exprs
        self.ops = ops

    def children(self) -> list:
        return self.exprs

    def __str__(self) -> str:
        return f"CmpExpr(ops: {self.ops})"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = self.exprs[0].codegen(context)
        for i in range(1, len(self.exprs)):
            addExpr = self.exprs[i]
            last = code[-1]
            code.extend(addExpr.codegen(context))
            tmp = BinaryOpValue(self.ops[i - 1], last.lhs, code[-1].lhs)
            tmp_name = context.tmpName()
            code.append(AssignmentInstruction(tmp_name, tmp))
        return code


class AddExpr(Expr):
    def __init__(self, exprs: list[MulExpr],  ops: list[str]) -> None:
        self.exprs = exprs
        self.ops = ops

    def children(self) -> list:
        return self.exprs

    def __str__(self) -> str:
        return f"AddExpr(ops: {self.ops})"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = self.exprs[0].codegen(context)
        for i in range(1, len(self.exprs)):
            mulExpr = self.exprs[i]
            last = code[-1]
            code.extend(mulExpr.codegen(context))
            tmp = BinaryOpValue(self.ops[i - 1], last.lhs, code[-1].lhs)
            tmp_name = context.tmpName()
            code.append(AssignmentInstruction(tmp_name, tmp))
        return code


class MulExpr(Expr):
    def __init__(self, exprs: list[UnaryExpr],  ops: list[str]) -> None:
        self.exprs = exprs
        self.ops = ops

    def children(self) -> list:
        return self.exprs

    def __str__(self) -> str:
        return f"MulExpr(ops: {self.ops})"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = self.exprs[0].codegen(context)
        for i in range(1, len(self.exprs)):
            unaryExpr = self.exprs[i]
            last = code[-1]
            code.extend(unaryExpr.codegen(context))
            tmp = BinaryOpValue(self.ops[i - 1], last.lhs, code[-1].lhs)
            tmp_name = context.tmpName()
            code.append(AssignmentInstruction(tmp_name, tmp))
        return code


class UnaryExpr(Expr):
    def __init__(self, value: ValueExpr, ops: list[str]) -> None:
        self.value = value
        self.ops = ops

    def children(self) -> list:
        return [self.value]

    def __str__(self) -> str:
        return f"UnaryExpr(ops: {self.ops})"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = self.value.codegen(context)
        for op in self.ops:
            tmp = UnaryOpValue(op, code[-1].lhs)
            tmp_name = context.tmpName()
            code.append(AssignmentInstruction(tmp_name, tmp))
        return code


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
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        if self.type == "id":
            name = context.tmpName()
            return [AssignmentInstruction(name, SingleValue(self.value))]
        elif self.type == "value":
            name = context.tmpName()
            return [AssignmentInstruction(name, self.value.codegen(context))]
        elif self.type == "expr":
            return self.value.codegen(context)
        else:
            callCode = self.value.codegen(context)
            name = context.tmpName()
            callCode[-1] = AssignmentInstruction(name, callCode[-1])
            return callCode


class Value(Expr):
    def __init__(self, value: str, type:str) -> None:
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return f"Value({self.type}: {self.value})"
    
    def codegen(self, context: CodegenContext) -> IRValue:
        return SingleValue(self.value)


class CallExpr(Expr):
    def __init__(self, name: str, argList:list[Expr]) -> None:
        self.name = name
        self.argList = argList

    def children(self) -> list:
        return self.argList

    def __str__(self) -> str:
        return f"CallExpr({self.name})"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        finfo = context.resolveFunc(self.name)
        code = []
        if not finfo:
            for arg in self.argList:
                code.extend(arg.codegen(context))
                code.append(ParameterInstruction(SingleValue(code[-1].lhs)))   
            code.append(CallInstruction(self.name, len(self.argList)))
        else:
            for i, arg in enumerate(self.argList):
                code.extend(arg.codegen(context))
                name = finfo.args[i] if i < len(finfo.args) else None
                code.append(ParameterInstruction(SingleValue(code[-1].lhs), name))
            calllen = len(self.argList)
            arglen = len(finfo.args)
            if calllen < arglen:
                for i in range(calllen, arglen):
                    name = finfo.args[i]
                    code.append(ParameterInstruction(SingleValue("nil"), name))
            code.append(CallInstruction(self.name, arglen, finfo.location))
        return code

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
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = []
        cond = self.cond.codegen(context)
        thenBr = self.thenBr.codegen(context)
        if not thenBr:
            thenBr.append(BlankInstruction())
        elseBr = self.elseBr.codegen(context)
        if not elseBr:
            elseBr.append(BlankInstruction())
        ifgoto = IfGotoInstruction(SingleValue(cond[-1].lhs), thenBr[0])
        endBlank = BlankInstruction()
        code.extend(cond)
        code.append(ifgoto)
        code.append(GotoInstruction(elseBr[0]))
        code.extend(thenBr)
        code.append(GotoInstruction(endBlank))
        code.extend(elseBr)
        code.append(endBlank)
        return code
        

class WhileStatement(Statement):
    def __init__(self, cond: Expr, loop: StatementList) -> None:
        self.cond = cond
        self.loop = loop

    def children(self) -> list:
        return [self.cond, self.loop]

    def __str__(self) -> str:
        return "WhileStatement"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = []
        cond = self.cond.codegen(context)
        endBlank = BlankInstruction()
        context.loop_exits.append(endBlank)
        loop = self.loop.codegen(context)
        if not loop:
            loop.append(BlankInstruction())
        context.loop_exits.pop()
        ifgoto = IfGotoInstruction(SingleValue(cond[-1].lhs), loop[0])
        code.append(GotoInstruction(cond[0]))
        code.extend(loop)
        code.extend(cond)
        code.append(ifgoto)
        code.append(endBlank)
        return code


class ReturnStatement(Statement):
    def __init__(self, result: Expr = None) -> None:
        self.result = result

    def children(self) -> list:
        return [self.result]
    
    def __str__(self) -> str:
        return "ReturnStatement"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        if not self.result:
            return [ReturnInstruction(SingleValue("nil"))]
        code = []
        code.extend(self.result.codegen(context))
        code.append(ReturnInstruction(SingleValue(code[-1].lhs)))
        return code


class BreakStatement(Statement):
    def __str__(self) -> str:
        return "BreakStatement"
    
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        if not context.loop_exits:
            raise CodegenError("Break statement out of loop")
        exit = context.loop_exits[-1]
        return [GotoInstruction(exit)]


class Declaration(Statement):
    def codegen(self, context: CodegenContext) -> list[Instruction]:
        pass


class VarDeclaration(Declaration):
    def __init__(self, name: str, value: Expr) -> None:
        self.name = name
        self.value = value

    def children(self) -> list:
        return [self.value]
    
    def __str__(self) -> str:
        return f"VarDeclaration({self.name})"

    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = []
        code.extend(self.value.codegen(context))
        code.append(AssignmentInstruction(self.name, SingleValue(code[-1].lhs)))
        return code


class FunctionDeclaration(Declaration):
    def __init__(self, name: str, argList: list[str] = None, body: StatementList = None) -> None:
        self.name = name
        self.argList = argList
        self.body = body

    def children(self) -> list:
        return [self.body]
    
    def __str__(self) -> str:
        return f"FunctionDeclaration(name: {self.name}, args: {self.argList})"

    def codegen(self, context: CodegenContext) -> list[Instruction]:
        code = []
        start = BlankInstruction()
        end = BlankInstruction()
        finfo = FunctionInfo(self.name, self.argList, start)
        context.top().funcs[self.name] = finfo
        context.create()
        body = self.body.codegen(context)
        context.drop()
        code.append(GotoInstruction(end))
        code.append(start)
        code.extend(body)
        code.append(ReturnInstruction(SingleValue("nil")))
        code.append(end) 
        return code