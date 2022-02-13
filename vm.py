import argparse
from pydoc import resolve
from typing import Dict
from xmlrpc.client import Boolean


from compiler.compiler import compile
from compiler.src.bytecode import *

class Frame:
    def __init__(self) -> None:
        self.stack = []
        self.values = {}

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if not self.stack:
            raise Exception("Stack is empty")
        value = self.stack[-1]
        self.stack.pop()
        return value
    
    def top(self):
        if not self.stack:
            raise Exception("Stack is empty")
        return self.stack[-1]

    def is_defined(self, name):
        return name in self.values.keys()

    def set(self, name, value):
        self.values[name] = value
    
    def get(self, name):
        return self.values.get(name, None)


class VM:
    def __init__(self) -> None:
        self.bytecode = []
        self.pos = 0
        self.frames = []
        self.STACK_LIMIT = 999

    def init(self, bytecode: bytearray):
        self.pos = 0
        self.frames: List[Frame]  = [Frame()]
        self.builtins: Dict[str, function] = {}
        self.bytecode = bytecode
        self.bytecode = self._decode_bytecode()
        self._init_builtins()
        

    def run(self): 
        self.pos = 0
        while self.pos < len(self.bytecode):
            line = self.bytecode[self.pos]
          
            self.pos += 1
            t = type(line)
            if t == OrOp:
                arg1 = self.frames[-1].pop()
                arg2 = self.frames[-1].pop()
                self.frames[-1].push(arg1 or arg2)
            elif t == AndOp:
                arg1 = self.frames[-1].pop()
                arg2 = self.frames[-1].pop()
                self.frames[-1].push(arg1 and arg2)
            elif t == EqOp:
                arg1 = self.frames[-1].pop()
                arg2 = self.frames[-1].pop()
                self.frames[-1].push(arg1 == arg2)
            elif t == NeqOp:
                arg1 = self.frames[-1].pop()
                arg2 = self.frames[-1].pop()
                self.frames[-1].push(arg1 != arg2)
            elif t == LessOp:
                arg1 = self._value2number(self.frames[-1].pop())
                arg2 = self._value2number(self.frames[-1].pop())
                self.frames[-1].push(arg1 < arg2)
            elif t == LessEqOp:
                arg1 = self._value2number(self.frames[-1].pop())
                arg2 = self._value2number(self.frames[-1].pop())
                self.frames[-1].push(arg1 <= arg2)
            elif t == GreaterOp:
                arg1 = self._value2number(self.frames[-1].pop())
                arg2 = self._value2number(self.frames[-1].pop())
                self.frames[-1].push(arg1 > arg2)
            elif t == GreaterEqOp:
                arg1 = self._value2number(self.frames[-1].pop())
                arg2 = self._value2number(self.frames[-1].pop())
                self.frames[-1].push(arg1 >= arg2)
            elif t == AddOp:
                arg1 = self.frames[-1].pop()
                arg2 = self.frames[-1].pop()
                if type(arg1) != str or type(arg2) != str:
                    arg1 = self._value2number(arg1)
                    arg2 = self._value2number(arg2)
                self.frames[-1].push(arg1 + arg2)
            elif t == SubOp:
                arg1 = self._value2number(self.frames[-1].pop())
                arg2 = self._value2number(self.frames[-1].pop())
                self.frames[-1].push(arg1 - arg2)
            elif t == MulOp:
                arg1 = self._value2number(self.frames[-1].pop())
                arg2 = self._value2number(self.frames[-1].pop())
                self.frames[-1].push(arg1 * arg2)
            elif t == DivOp:
                arg1 = self._value2number(self.frames[-1].pop())
                arg2 = self._value2number(self.frames[-1].pop())
                self.frames[-1].push(arg1 / arg2)
            elif t == DivRemOp:
                arg1 = self._value2number(self.frames[-1].pop())
                arg2 = self._value2number(self.frames[-1].pop())
                self.frames[-1].push(arg1 % arg2)
            elif t == UnaryPlus:
                arg = self._value2number(self.frames[-1].pop())
                self.frames[-1].push(arg)
            elif t == UnaryMinus:
               arg = self._value2number(self.frames[-1].pop())
               self.frames[-1].push(-arg)
            elif t == UnaryNot:
                arg = self._value2bool(self.frames[-1].pop())
                self.frames[-1].push(not arg)
            elif t == Pushv:
                name = line.name
                value = self._resolve_frame(name)
                self.frames[-1].push(value)
            elif t == Pushl:
                self.frames[-1].push(line.value)
            elif t == Pop:
                self.frames[-1].pop()
            elif t == Load:
                value = self.frames[-1].pop()
                var_id = self.frames[-1].pop()
                self.frames[-1].set(var_id, value)
            elif t == Jmp:
                address = self.frames[-1].pop()
                self.pos = address
            elif t == CJmp:
                cond = self._value2bool(self.frames[-1].pop())
                address = self.frames[-1].pop()
                if cond:
                    self.pos = address
            elif t == Call:
                if len(self.frames) == self.STACK_LIMIT:
                    raise Exception("Stack overflow")
                argc = self.frames[-1].pop()
                addr = self.frames[-1].pop()
                is_assigned = self.frames[-1].pop()
                tmp_addr = None
                if is_assigned:
                    tmp_addr = self.frames[-1].pop()
                frame = Frame()
                frame.push(self.pos)
                for i in range(argc):
                    value = self.frames[-1].pop()
                    name = self.frames[-1].pop()
                    frame.set(name, value)
                if tmp_addr:
                    self.frames[-1].push(tmp_addr)
                self.frames.append(frame)
                self.pos = addr
            elif t == Callb:
                if len(self.frames) == self.STACK_LIMIT:
                    raise Exception("Stack overflow")
                argc = self.frames[-1].pop()
                name = self.frames[-1].pop()
                is_assigned = self.frames[-1].pop()
                tmp_addr = None
                if is_assigned:
                    tmp_addr = self.frames[-1].pop()
                values = []
                for i in range(argc):
                    values.append(self.frames[-1].pop())
                    self.frames[-1].pop()
                if tmp_addr:
                    self.frames[-1].push(tmp_addr)
                self.frames[-1].push(self.builtins[name](*reversed(values)))
            elif t == Return:
                value = self.frames[-1].pop()
                ret_addr = self.frames[-1].pop()
                self.frames.pop()
                if not self.frames:
                    print(value)
                    break
                self.frames[-1].push(value)
                self.pos = ret_addr
            elif t == Hault:
                break
            else:
                raise Exception("Unknown bytecode operation")


    def _read(self, n: int) -> bytearray:
        if self.pos >= len(self.bytecode):
            return None
        start = self.pos
        self.pos += n
        return self.bytecode[start: self.pos]

    def _decode_bytecode(self) -> List[Bytecode]:
        decoded = []
        opcode = self._read(1)
        while opcode:
            opcode = opcode[0]
            if opcode in range(16):
                decoded.append(opcode2cls[opcode]())
            elif opcode == 16:
                    size1, size2 = self._read(2)
                    size = 256 * size1 + size2
                    name = int(self._bytes2string(self._read(size)))
                    decoded.append(Pushv(name))
            elif opcode == 17:
                    size1, size2 = self._read(2)
                    size = 256 * size1 + size2
                    value = self._bytes2string(self._read(size))
                    value= self._parse_value(value)
                    decoded.append(Pushl(value))
            elif opcode == 18:
                    decoded.append(Pop())
            elif opcode == 19:
                    decoded.append(Load())
            elif opcode == 20:
                    decoded.append(Jmp())
            elif opcode == 21:
                    decoded.append(CJmp())
            elif opcode == 22:
                    decoded.append(Call())
            elif opcode == 23:
                    decoded.append(Callb())
            elif opcode == 24:
                    decoded.append(Return())
            elif opcode == 25:
                    decoded.append(Hault())
            opcode = self._read(1)

        for i, line in enumerate(decoded):
            line.id = i
        return decoded

    def _resolve_frame(self, name):
     
        return self.frames[-1].values.get(name, None)

    def _parse_value(self, value: str) -> Union[float, str, Boolean, None]:
        if value == "nil":
            return None
        elif value == "true":
            return True
        elif value == "false":
            return False
        elif value[0].isdigit():
            value: float = float(value)
            if value.is_integer():
                return int(value)
            return value
        else:
            return value
        
    def _value2bool(self, value) -> bool:
        if type(value) == bool:
            return value 
        if value is None:
            return False
        return True
    
    def _value2number(self, value) -> float:
        if type(value) in [float, int]:
            return value
        if type(value) == str:
            return float(value)
        raise Exception("Can't cast type to number")

    def _value2string(self, value) -> str:
        if value == True:
            return "true"
        if value == False:
            return "false"
        if value is None:
            return "nil"
        return str(value)

    def _bytes2string(self, bytes: bytearray) -> str:
        return bytes.decode(encoding="ASCII")

    
    def _init_builtins(self):
        def _print(*args):
            for arg in args:
                print(arg)

        def _tostring(*args):
            if not args:
                return ""
            return self._value2string(args[0])

        def _tonumber(*args):
            if not args:
                return 0
            return self._value2number(args[0])

        def _read(*args):
            text = input()
            return text

        self.builtins = {
            "print": _print,
            "tostring": _tostring,
            "tonumber": _tonumber,
            "read": _read
        }

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', action='store_true', help='target file is bytecode')
    parser.add_argument("file")
    args = parser.parse_args()
    file = args.file
    
    bytecode = None
    if args.b:
        with open(file, "rb") as f:
            bytecode = bytearray(f.read())
    else:
        bytecode = compile(file)

    
    vm = VM()
    vm.init(bytecode)
    vm.run()

if __name__ == "__main__":
    main()