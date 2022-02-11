from numpy import var
from .IR import *

from collections import defaultdict

class Bytecode:
    def __init__(self) -> None:
        self.id = -1
    def __str__(self) -> str:
        pass



#Operations

class OrOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: OR"

class AndOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: AND"

class EqOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: EQ"

class NeqOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: NEQ"

class LessOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: LESS"

class LessEqOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: LESSEQ"

class GreaterOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: GR"

class GreaterEqOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: GREQ"

class AddOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: ADD"

class SubOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: SUB"

class MulOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: MUL"

class DivOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: DIV"

class DivRemOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: DIVREM"

class UnaryPlus(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: UPLUSS"

class UnaryMinus(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: UMINUS"

class UnaryNot(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: UNOT"

unOp2cls = {
    "+": UnaryPlus,
    "-": UnaryMinus,
    "not": UnaryNot,
}

biOp2cls = {
    "or": OrOp,
    "and": AndOp,
    "==": EqOp,
    "~=": NeqOp,
    "<": LessOp,
    "<=": LessEqOp,
    ">": GreaterOp,
    ">=": GreaterEqOp,
    "+": AddOp,
    "-": SubOp,
    "*": MulOp,
    "/": DivOp,
    "%": DivRemOp,
}


# Commands
class Pushv(Bytecode):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return f"{self.id}: PUSHV {self.name}"

class Pushl(Bytecode):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"{self.id}: PUSHL {self.value}"

class Pop(Bytecode):
    def __init__(self) -> None:
        super().__init__()
    
    def __str__(self) -> str:
        return f"{self.id}: POP"

class Load(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: LOAD"

class Jmp(Bytecode):
    def __init__(self) -> None:
        super().__init__()
        
    def __str__(self) -> str:
        return f"{self.id}: JMP"

class CJmp(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: CJMP"

class Call(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: CALL"

class Callb(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: CALLB"

class Return(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: RETURN"

class Hault(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: HAULT"


def tac2bytecode(tac: List[Instruction]) -> List[Bytecode]:
    var_ids = defaultdict(lambda: -1)
    for line in tac:
        if type(line) == AssignmentInstruction:
            var_ids[line.lhs] = len(var_ids)
        elif type(line) == ParameterInstruction and line.name:
            var_ids[line.name] = len(var_ids)
    mapping = {}
    toresolve = []

    def determine(value: str) -> str:
        if value.startswith('"'):
            return "str"
        elif value.isidentifier() and value not in ["true", "false"]:
            return "id"
        else:
            return "other" 
    
    def ins2byte(ins: Instruction) -> List[Bytecode]:
        t = type(ins)
        bytecode = []
        if t == GotoInstruction:
            target_id = ins.target.id
            bytecode.append(Pushl(None))
            toresolve.append((bytecode[-1], target_id))
            bytecode.append(Jmp())
        elif t == IfGotoInstruction:
            cond_var = ins.cond.value
            cond_id = var_ids[cond_var]
            target_id = ins.target.id
            bytecode.append(Pushl(None))
            toresolve.append((bytecode[-1], target_id))
            bytecode.append(Pushv(cond_id))
            bytecode.append(CJmp())
        elif t == AssignmentInstruction:
            var_id = var_ids[ins.lhs]
            rhs = ins.rhs
            rhst = type(rhs)
            if rhst in [SingleValue, UnaryOpValue]:
                kind = determine(rhs.value)
                value = rhs.value
                if kind == "id":
                    bytecode.append(Pushv(var_ids[value]))
                elif kind == "str":
                    bytecode.append(Pushl(value[1: -1]))
                else:
                    bytecode.append(Pushl(value))
                if rhst == UnaryOpValue:
                    bytecode.append(unOp2cls[rhs.op]())

            elif rhst == BinaryOpValue:
                value1 = rhs.value1
                value2 = rhs.value2
                for kind, value in zip([determine(value2), determine(value1)], [value2, value1]):
                    if kind == "id":
                        bytecode.append(Pushv(var_ids[value]))
                    elif kind == "str":
                        bytecode.append(Pushl(value[1: -1]))
                    else:
                        bytecode.append(Pushl(value))
                bytecode.append(biOp2cls[rhs.op]())
                
            elif rhst == CallInstruction:
                if rhs.target is None:
                    bytecode.append(Pushl(rhs.name))
                    bytecode.append(Pushl(rhs.argc))
                    bytecode.append(Callb())
                else:
                    target_id = rhs.target.id
                    bytecode.append(Pushl(None))
                    toresolve.append((bytecode[-1], target_id))
                    bytecode.append(Pushl(rhs.argc))
                    bytecode.append(Call())
            bytecode.append(Pushl(var_id))
            bytecode.append(Load())
        elif t == ReturnInstruction:
            kind = determine(ins.value.value)
            value = ins.value.value
            if kind == "id":
                bytecode.append(Pushv(var_ids[value]))
            elif kind == "str":
                bytecode.append(Pushl(value[1: -1]))
            else:
                bytecode.append(Pushl(value))
            bytecode.append(Return())
        elif t == ParameterInstruction:
            bytecode.append(Pushv(var_ids[ins.value.value]))
            if ins.name is None:
                bytecode.append(Pushl(-1))
            else:
                bytecode.append(Pushl(var_ids[ins.value.value]))
        elif t == CallInstruction:
            if ins.target is None:
                bytecode.append(Pushl(ins.name))
                bytecode.append(Pushl(ins.argc))
                bytecode.append(Callb())
                bytecode.append(Pop())
            else:
                target_id = ins.target.id
                bytecode.append(Pushl(None))
                toresolve.append((bytecode[-1], target_id))
                bytecode.append(Pushl(ins.argc))
                bytecode.append(Call())
                bytecode.append(Pop())
        elif t == EndInstruction:
            bytecode.append(Hault())
        
        mapping[ins.id] = bytecode
        return bytecode

    bytecode = []
    for ins in tac:
        bytecode.extend(ins2byte(ins))
    
    for i in range(len(bytecode)):
        bytecode[i].id = i
    
    for jmp in toresolve:
        code, ins_id = jmp[0], jmp[1]
        code.value = mapping[ins_id][0].id

    
    return bytecode 