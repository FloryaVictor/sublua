from numpy import source
from .src.lexer import Lexer
from .src.parser import Parser
from .src.graph_utils import node2Graphviz, buildCFG, basicBlock2Graphviz
from .src.bytecode import tac2bytecode, bytecode2binary



def compile(file: str) -> bytearray:
    lexer = Lexer()
    code = ""
    with open(file, "r") as f:
        code = f.read()
    lexer.init(code)
    parser = Parser(lexer.lex())
    tree = parser.parse()
    tac = tree.codegen()
    bytecode = tac2bytecode(tac)
    binary = bytecode2binary(bytecode)
    return binary


def main():
    file = "data/tests/test1.txt"
    result = "output/binary"
    binary = compile(file)
    with open(result, "wb") as f:
        f.write(binary)
   

if __name__ == "__main__":
    main()
