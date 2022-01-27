from numpy import source
from src.lexer import Lexer
from src.parser import Parser
from src.graph_utils import toGraphviz

import os
import sys

import graphviz

def main():
    lexer = Lexer()
    code_path = "compiler/data/test1.txt"
    code = ""
    with open(code_path, "r") as f:
        code = f.read()
    lexer.init(code)
 
    parser = Parser(lexer.lex())
    parsed_tree = parser.parse()
    
    graph = toGraphviz(parsed_tree, merge=True)
    graph.render("compiler/output/ast_tree", cleanup=True, format="png")


if __name__ == "__main__":
    main()