from ast import UnaryOp
from numpy import var
from .IR import *

from collections import defaultdict

class Bytecode:
    def __init__(self) -> None:
        self.id = -1
    def __str__(self) -> str:
        pass
    
    def to_binary(self) -> bytearray:
        pass



#Operations

class OrOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: OR"

    def to_binary(self) -> bytearray:
        return bytearray([0])

class AndOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: AND"
    
    def to_binary(self) -> bytearray:
        return bytearray([1])

class EqOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: EQ"
    
    def to_binary(self) -> bytearray:
        return bytearray([2])

class NeqOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: NEQ"

    def to_binary(self) -> bytearray:
        return bytearray([3])

class LessOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: LESS"

    def to_binary(self) -> bytearray:
        return bytearray([4])

class LessEqOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: LESSEQ"

    def to_binary(self) -> bytearray:
        return bytearray([5])

class GreaterOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: GR"

    def to_binary(self) -> bytearray:
        return bytearray([6])

class GreaterEqOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: GREQ"
    
    def to_binary(self) -> bytearray:
        return bytearray([7])

class AddOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: ADD"

    def to_binary(self) -> bytearray:
        return bytearray([8])

class SubOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: SUB"

    def to_binary(self) -> bytearray:
        return bytearray([9])

class MulOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: MUL"

    def to_binary(self) -> bytearray:
        return bytearray([10])

class DivOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: DIV"

    def to_binary(self) -> bytearray:
        return bytearray([11])

class DivRemOp(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: DIVREM"

    def to_binary(self) -> bytearray:
        return bytearray([12])


class UnaryPlus(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: UPLUSS"

    def to_binary(self) -> bytearray:
        return bytearray([13])

class UnaryMinus(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: UMINUS"

    def to_binary(self) -> bytearray:
        return bytearray([14])

class UnaryNot(Bytecode):
    def __str__(self) -> str:
        return f"{self.id}: UNOT"

    def to_binary(self) -> bytearray:
        return bytearray([15])


opcode2cls = {
    0: OrOp, 
    1: AndOp,
    2: EqOp,
    3: NeqOp,
    4: LessOp,
    5: LessEqOp,
    6: GreaterOp,
    7: GreaterEqOp,
    8: AddOp,
    9: SubOp, 
    10: MulOp,
    11: DivOp,
    12: DivRemOp,
    13: UnaryPlus,
    14: UnaryMinus,
    15: UnaryNot
}


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

    def to_binary(self) -> bytearray:
        name = str(self.name)
        size1 = len(name) // 256
        size2 = len(name) % 256
        name = bytearray(name, encoding="ASCII")
        return bytearray([16]) + bytearray([size1, size2]) + name

class Pushl(Bytecode):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"{self.id}: PUSHL {self.value}"

    def to_binary(self) -> bytearray:
        value = str(self.value)
        size1 = len(value) // 256
        size2 = len(value) % 256
        value = bytearray(value, encoding="ASCII")
        return bytearray([17]) + bytearray([size1, size2]) + value
    

class Pop(Bytecode):
    def __init__(self) -> None:
        super().__init__()
    
    def __str__(self) -> str:
        return f"{self.id}: POP"

    def to_binary(self) -> bytearray:
        return bytearray([18])

class Load(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: LOAD"

    def to_binary(self) -> bytearray:
        return bytearray([19])

class Jmp(Bytecode):
    def __init__(self) -> None:
        super().__init__()
        
    def __str__(self) -> str:
        return f"{self.id}: JMP"

    def to_binary(self) -> bytearray:
        return bytearray([20])

class CJmp(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: CJMP"

    def to_binary(self) -> bytearray:
        return bytearray([21])

class Call(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: CALL"

    def to_binary(self) -> bytearray:
        return bytearray([22])

class Callb(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: CALLB"

    def to_binary(self) -> bytearray:
        return bytearray([23])

class Return(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: RETURN"

    def to_binary(self) -> bytearray:
        return bytearray([24])

class Hault(Bytecode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.id}: HAULT"

    def to_binary(self) -> bytearray:
        return bytearray([25])


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
            bytecode.append(Pushl(var_id))
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
                bytecode.append(Pushl(1))
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
            if ins.name is None:
                bytecode.append(Pushl(-1))
            else:
                bytecode.append(Pushl(var_ids[ins.name]))
            bytecode.append(Pushv(var_ids[ins.value.value]))
        elif t == CallInstruction:
            bytecode.append(Pushl(0))
            if ins.target is None:
                bytecode.append(Pushl(ins.name))
                bytecode.append(Pushl(ins.argc))
                bytecode.append(Callb())
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

def bytecode2binary(bytecode: List[Bytecode]) -> bytearray:
    binary = bytearray()
    for line in bytecode:
        binary += line.to_binary()
    return binary