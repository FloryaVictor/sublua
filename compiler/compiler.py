from src.lexer import Lexer
from src.parser import Parser

import os
import sys

def main():
    lexer = Lexer()
    code_path = "compiler/data/test_lex.txt"
    code = ""
    with open(code_path, "r") as f:
        code = f.read()
    lexer.init(code)
    # for token in lexer.lex():
    #     print(token)
    parser = Parser(lexer.lex())
    parsed_tree = parser.parse()
    print(parsed_tree)

if __name__ == "__main__":
    main()