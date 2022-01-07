import re


class Token:
    def __init__(self, tag: str, line: int, pos: int, value: str):
        self.tag = tag
        self.line = line
        self.pos = pos
        self.value = value

    def __str__(self):
        return "{} ({}, {}): {}".format(self.tag, self.line, self.pos,
                                        self.value)


class Lexer:
    def __init__(self):
        self._index = 0
        self._pos = self._line = 1
        self.code = ''
        rules = [
            (r'--.*', 'Comment'),
            (r'end', 'end'),
            (r'function', 'function'),
            (r'return', 'return'),
            (r'while', 'while'),
            (r'break', 'break'),
            (r'do', 'do'),
            (r'if', 'if'),
            (r'then', 'then'),
            (r'else', 'else'),
            (r'nil', 'nil'),
            (r'not', 'not'),
            (r'or', 'or'),
            (r'and', 'and'),
            (r'(true|false)', 'boolean'),
            (r'[^\d\W]\w*', 'id'),
            (r'\d*\.\d+|\d+', 'number'),
            (r'".*"', 'string'),
            (r'\(', 'lparen'),
            (r'\)', 'rparen'),
            (r',', 'comma'),
            (r'\+', 'plus'),
            (r'\-', 'minus'),
            (r'\*', 'mul'),
            (r'\/', 'div'),
            (r'\%', 'divrem'),
            (r'\<\=', 'lesseq'),
            (r'\>\=', 'greatereq'),
            (r'\<', 'less'),
            (r'\>', 'greater'),
            (r'\=\=', 'eq'),
            (r'\~\=', 'neq'), 
            (r'\=', 'assign')
        ]
        self.rules = []
        for regex, tag in rules:
            self.rules.append((re.compile(regex), tag))
        self.redundant = ['Comment']

    def init(self, code: str):
        self._index = 0
        self._pos = self._line = 1
        self.code = code

    def _cur(self):
        if self._index == len(self.code):
            return -1
        return self.code[self._index]

    def _is_end(self):
        return self._cur() == -1

    def _is_new_line(self):
        if self._index == len(self.code):
            return True
        if self._cur() == '\r' and self._index + 1 < len(self.code):
            return self.code[self._index + 1] == '\n'
        return self._cur() == '\n'

    def _shift(self):
        if self._index < len(self.code):
            if self._is_new_line():
                if self._cur() == '\r':
                    self._index += 1
                self._line += 1
                self._pos = 1
            else:
                self._pos += 1
            self._index += 1

    def _next(self):
        while not self._is_end():
            while not self._is_end() and self._cur().isspace():
                self._shift()
            for regex, tag in self.rules:
                m = regex.match(self.code, self._index)
                if m:
                    token = Token(tag, self._line, self._pos, m.group())
                    self._pos += m.end() - m.start()
                    self._index = m.end()
                    return token
            if not self._is_end():
                raise SyntaxError(f"Lexical analysis error on ({self._line}, {self._pos})")
        return None

    def tokens(self):
        while True:
            token = self._next()
            if token is None:
                break
            if token.tag in self.redundant:
                continue
            yield token


if __name__ == "__main__":
    with open("compiler/data/test_lex.txt", "r") as code:
        lexer = Lexer()
        lexer.init(code.read())
        tokens = lexer.tokens()
        for token in tokens:
            print(token)