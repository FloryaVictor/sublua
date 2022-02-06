from typing import Union


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
        pass
    def __str__(self) -> str:
        pass


class GotoInstruction(Instruction):
    def __init__(self, target: int) -> None:
        self.target = target

    def __str__(self) -> str:
        return f"goto {self.target}"


class AssignmentInstruction(Instruction):
    def __init__(self, lhs: str, rhs: IRValue) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"{self.lhs} = {self.rhs}"


class ReturnInstruction(Instruction):
    def __init__(self, value: SingleValue) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"return {self.value}"


class ParameterInstruction(Instruction):
    def __init__(self, value: SingleValue) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"push parameter {self.value}"


class CallInstruction(Instruction, IRValue):
    def __init__(self, name: str, argc: int = 0, target: int = -1) -> None:
        self.name = name
        self.argc = argc
        self.target = target
        

    def __str__(self) -> str:
        if self.target >= 0:
            return f"call {self.name} {self.argc} {self.target}"
        return f"call {self.name} {self.argc}"


class IfGotoInstruction(Instruction):
    def __init__(self, cond: SingleValue, target: int) -> None:
        self.cond = cond
        self.target = target

    def __str__(self) -> str:
        return f"if {self.cond} goto {self.target}"


class EndInstruction(Instruction):
    def __init__(self) -> None:
        pass
    def __str__(self) -> str:
        return "end"