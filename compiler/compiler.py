from numpy import source
from src.lexer import Lexer
from src.parser import Parser
from src.graph_utils import node2Graphviz, buildCFG, basicBlock2Graphviz
from src.bytecode import tac2bytecode

import os
import sys

import graphviz

def main():
    lexer = Lexer()
    code_path = "compiler/data/tests/test1.txt"
    code = ""
    with open(code_path, "r") as f:
        code = f.read()
    lexer.init(code)
 
    parser = Parser(lexer.lex())
    parsed_tree = parser.parse()
    tac = parsed_tree.codegen()
    bytecode = tac2bytecode(tac)
    
    
    for instruction in bytecode:
        print(instruction)

    # graph = basicBlock2Graphviz(cfg)
   
    # graph.render("compiler/output/cfg", cleanup=True, format="png")


if __name__ == "__main__":
    main()