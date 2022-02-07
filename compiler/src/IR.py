from sys import prefix
from typing import Union
from copy import deepcopy

class IRValue:
    def __init__(self) -> None:
        pass
    def __str__(self) -> str:
        pass

class SingleValue(IRValue):
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

class UnaryOpValue(IRValue):
    def __init__(self, op: str, value: str) -> None:
        self.op = op
        self.value = value

    def __str__(self) -> str:
        return f"{self.op} {self.value}"

class BinaryOpValue(IRValue):
    def __init__(self, op: str, value1: str, value2: str) -> None:
        self.op = op
        self.value1 = value1
        self.value2 = value2

    def __str__(self) -> str:
        return f"{self.value1} {self.op} {self.value2}"


class Instruction:
    def __init__(self) -> None:
        self.id = -1

    def __str__(self) -> str:
        pass


class GotoInstruction(Instruction):
    def __init__(self, target: Instruction) -> None:
        super().__init__()
        self.target = target

    def __str__(self) -> str:
        return f"{self.id}: goto {self.target.id}"


class AssignmentInstruction(Instruction):
    def __init__(self, lhs: str, rhs: IRValue) -> None:
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"{self.id}: {self.lhs} = {self.rhs}"


class ReturnInstruction(Instruction):
    def __init__(self, value: SingleValue) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"{self.id}: return {self.value}"


class ParameterInstruction(Instruction):
    def __init__(self, value: SingleValue, name: str = None) -> None:
        super().__init__()
        self.value = value
        self.name = name

    def __str__(self) -> str:
        if self.name:
            return f"{self.id}: push parameter {self.name} = {self.value}"
        return f"{self.id}: push parameter {self.value}"


class CallInstruction(Instruction, IRValue):
    def __init__(self, name: str, argc: int = 0, target: Instruction = None) -> None:
        super().__init__()
        self.name = name
        self.argc = argc
        self.target = target
        

    def __str__(self) -> str:
        prefix = f"{self.id}: " if self.id >=0 else ""
        if self.target:
            return f"{prefix}call {self.name} {self.argc} {self.target.id}"
        return f"{prefix}call {self.name} {self.argc}"


class IfGotoInstruction(Instruction):
    def __init__(self, cond: SingleValue, target: Instruction) -> None:
        super().__init__()
        self.cond = cond
        self.target = target

    def __str__(self) -> str:
        return f"{self.id}: if {self.cond} goto {self.target.id}"


class EndInstruction(Instruction):
    def __init__(self) -> None:
        super().__init__()
        pass
    def __str__(self) -> str:
        return f"{self.id}: end"

class BlankInstruction(Instruction):
    def __init__(self) -> None:
        super().__init__()
    
    def __str__(self) -> str:
        return f"{self.id}: blank"

def enumerate_instructions(code: list[Instruction]) -> None:
    for i, instruction in enumerate(code):
        instruction.id = i

def remove_blanks(code: list[Instruction]) -> list[Instruction]:
    mapping = dict()
    code = deepcopy(code)
    for instruction in code:
        if type(instruction) == BlankInstruction:
            old_id = instruction.id
            new_id = old_id
            while type(code[new_id]) == BlankInstruction:
                new_id += 1
            mapping[old_id] = new_id

    for instruction in code:
        t = type(instruction)
    
        if t in [GotoInstruction, IfGotoInstruction, CallInstruction] and instruction.target:
            old_id = instruction.target.id
            if old_id in mapping:
                instruction.target = code[mapping[old_id]]
        elif t == AssignmentInstruction and type(instruction.rhs) == CallInstruction and instruction.rhs.target:
            old_id = instruction.rhs.target.id
            if old_id in mapping:
                instruction.rhs.target = code[mapping[old_id]]


    code = list(filter(lambda i: type(i) != BlankInstruction, code))
    
    enumerate_instructions(code)
    return code
    