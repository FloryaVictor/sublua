from .lexer import Token
from .ast import *


class ParsingError(Exception):
    def __init__(self, token: Token):
        self.token = token 

    def __str__(self):
        return f'Unexpected symbol at ({self.token.line}, {self.token.pos}) with value: {self.token.value}'


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.tokens.append(Token("EOF", tokens[-1].line, tokens[-1].pos + 1, "EOF"))
        self.pos = 0
    

    def __next(self) -> Token:
        cur =  self.tokens[self.pos] 
        self.pos += 1
        return cur


    def __lookup(self) -> Token:
        return self.tokens[self.pos]


    def __consume(self, symbol: str) -> None:
        cur = self.tokens[self.pos]
        if cur.value != symbol:
            raise ParsingError(cur)
        self.pos += 1

    def __isEOF(self):
        return self.pos == len(self.tokens) - 1
    

    def parse(self) -> Program:
        return self.__program()


    def __program(self):
        statements = self.__statementList()
        self.__consume("EOF")
        return Program(statements=statements)

    def __statementList(self):
        statements = []
        while self.__lookup().value in ["if", "while", "return", "break", "function"] or self.__lookup().tag == "id":
            statements.append(self.__statement()) 
        return StatementList(statements)

    def __statement(self):
        cur = self.__lookup()
        if cur.value == "if":
            return self.__ifStatement()
        elif cur.value == "while":
            return self.__whileStatement()
        elif cur.value == "return":
            return self.__reutrnStatement()
        elif cur.value == "break":
            return self.__breakStatement()
        elif cur.value == "function":
            return self.__declaration()
        elif  cur.tag == "id":
            if self.tokens[self.pos + 1].value == "(":
                return self.__callExpr()
            return self.__declaration()
        else:
            raise ParsingError(token=cur)


    def __expr(self):
        return self.__orExpr()


    def __orExpr(self):
        andExprs = [self.__andExpr()]
        while self.__lookup().value == "or":
            self.__next()
            andExprs.append(self.__andExpr())
        return OrExpr(andExprs)


    def __andExpr(self):
        eqExprs = [self.__eqExpr()]
        while self.__lookup().value == "and":
            self.__next()
            eqExprs.append(self.__eqExpr())
        return AndExpr(eqExprs)


    def __eqExpr(self):
        cmpExprs = [self.__cmpExpr()]
        ops = []
        while self.__lookup().value in ["==", "~="]:
            ops.append(self.__next().value)
            cmpExprs.append(self.__cmpExpr())
        return EqExpr(cmpExprs, ops)


    def __cmpExpr(self):
        addExprs = [self.__addExpr()]
        ops = []
        while self.__lookup().value in ["<", "<=", ">", ">="]:
            ops.append(self.__next().value)
            addExprs.append(self.__addExpr())
        return CmpExpr(addExprs, ops)


    def __addExpr(self):
        mulExprs = [self.__mulExpr()]
        ops = []
        while self.__lookup().value in ["+", "-"]:
            ops.append(self.__next().value)
            mulExprs.append(self.__mulExpr())
        return AddExpr(mulExprs, ops)


    def __mulExpr(self):
        unaryExprs = [self.__unaryExpr()]
        ops = []
        while self.__lookup().value in ["*", "/", "%"]:
            ops.append(self.__next().value)
            unaryExprs.append(self.__unaryExpr())
        return MulExpr(unaryExprs, ops)


    def __unaryExpr(self):
        ops = []
        while self.__lookup().value in ["+", "-", "not"]:
            ops.append(self.__next().value)
        valueExpr = self.__valueExpr()
        return UnaryExpr(valueExpr, ops)


    def __valueExpr(self):
        cur = self.__lookup()
        if cur.tag == "id":
            if self.tokens[self.pos + 1].value == "(":
                return ValueExpr(self.__callExpr(), type="call")
            else:
                return ValueExpr(self.__next().value, type="id")
        elif cur.tag in ["boolean", "number", "string"] or cur.value == "nil":
            return ValueExpr(self.__value(), "value")
        elif cur.value == "(":
            self.__consume("(")
            value = self.__expr()
            self.__consume(")")
            return ValueExpr(value, type="expr")
        else:
            raise ParsingError(token=cur)


    def __value(self):
        cur = self.__lookup()
        if cur.tag in ["boolean", "number", "string"]:
            return Value(self.__next().value, cur.tag)
        elif cur.value == "nil":
            return Value(self.__next().value, cur.value)
        else:
            raise ParsingError(token=cur)


    def __callExpr(self):
        if self.__lookup().tag != "id":
            raise ParsingError(token=self.__lookup())
        name = self.__next().value
        self.__consume("(")
        args = []
        if self.__lookup().value != ")":
            args.append(self.__expr())
            while self.__lookup().value != ")" and not self.__isEOF():
                self.__consume(",")
                args.append(self.__expr())
        self.__consume(")")
        return CallExpr(name, args)
 

    def __ifStatement(self):
        self.__consume("if")
        cond = self.__expr()
        thenBr = None
        elseBr = StatementList([])
        self.__consume("then")        
        thenBr = self.__statementList()
        if self.__lookup().value != "end":
            self.__consume("else")
            elseBr = self.__statementList()
        self.__consume("end")
        return IfStatement(cond, thenBr, elseBr)


    def __whileStatement(self):
        self.__consume("while")
        cond = self.__expr()
        self.__consume("do")
        statements = self.__statementList()
        self.__consume("end")
        return WhileStatement(cond, statements)


    def __reutrnStatement(self):
        result = None
        self.__consume("return")
        cur = self.__lookup()
        if cur.value in ["+", "-", "not", "(", "nil"] or cur.tag in ["id", "boolean", "number", "string"]:
            if cur.tag != "id": 
                result = self.__expr()
            elif cur.tag == "id" and self.tokens[self.pos + 1].value != "=":
                result = self.__expr()
        return ReturnStatement(result)


    def __breakStatement(self):
        self.__consume("break")
        return BreakStatement()


    def __declaration(self):
        if self.__lookup().value == "function":
            return self.__functionDeclaration()
        else:
            return self.__varDeclaration()


    def __varDeclaration(self):
        if self.__lookup().tag != "id":
            raise ParsingError(self.__lookup())
        name = self.__next().value
        self.__consume("=")
        value = self.__expr()
        return VarDeclaration(name, value)



    def __functionDeclaration(self):
        self.__consume("function")
        if self.__lookup().tag != "id":
            raise ParsingError(self.__lookup())
        name = self.__next().value
        args = []
        self.__consume("(")
        if self.__lookup().value != ")":
            if self.__lookup().tag != "id":
                raise ParsingError(self.__lookup())
            args.append(self.__next().value)
            while self.__lookup().value != ")":
                self.__consume(",")
                if self.__lookup().tag != "id":
                    raise ParsingError(self.__lookup())
                args.append(self.__next().value)
        self.__consume(")")
        body = self.__statementList()
        body.statements.append(ReturnStatement(None))
        self.__consume("end")
        return FunctionDeclaration(name, args, body)