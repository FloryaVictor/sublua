from numpy import source
from src.lexer import Lexer
from src.parser import Parser
from src.graph_utils import node2Graphviz, buildCFG, basicBlock2Graphviz

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
    code = parsed_tree.codegen()
    cfg = buildCFG(code)
    

    for instruction in code:
        print(instruction)
    
    graph = basicBlock2Graphviz(cfg)
   
    graph.render("compiler/output/cfg", cleanup=True, format="png")


if __name__ == "__main__":
    main()