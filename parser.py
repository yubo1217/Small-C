from lexer import Lexer

# ===== AST =====
class AST:
    pass

# --- Expression ---
class Expr(AST):
    pass

class Number(Expr):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class Char(Expr):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Char('{self.value}')"

class Identifier(Expr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Identifier({self.name})"

class UnaryOp(Expr):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    def __repr__(self):
        return f"UnaryOp({self.op}, {self.operand})"

class BinOp(Expr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class AddressOf(Expr):
    def __init__(self, target):
        self.target = target
    def __repr__(self):
        return f"AddressOf({self.target})"

class Deref(Expr):
    def __init__(self, pointer):
        self.pointer = pointer
    def __repr__(self):
        return f"Deref({self.pointer})"

class Call(Expr):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self):
        return f"Call({self.name}, {self.args})"

class ArrayAccess(Expr):
    def __init__(self, array, index):
        self.array = array
        self.index = index
    def __repr__(self):
        return f"ArrayAccess({self.array}, {self.index})"

# --- Statement ---
class Stmt(AST):
    pass

class VarDecl(Stmt):
    def __init__(self, var_type, name, value=None, is_pointer=False):
        self.var_type = var_type
        self.name = name
        self.value = value
        self.is_pointer = is_pointer
    def __repr__(self):
        return f"VarDecl({self.var_type}, {self.name}, {self.value}, pointer={self.is_pointer})"

class ArrayDecl(Stmt):
    def __init__(self, var_type, name, size, value=None):
        self.var_type = var_type
        self.name = name
        self.size = size
        self.value = value
    def __repr__(self):
        return f"ArrayDecl({self.var_type}, {self.name}, size={self.size}, value={self.value})"

class Assignment(Stmt):
    def __init__(self, target, value):
        self.target = target
        self.value = value
    def __repr__(self):
        return f"Assignment({self.target}, {self.value})"

class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Block({self.statements})"

class Return(Stmt):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Return({self.value})"

class IfStmt(Stmt):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    def __repr__(self):
        return f"IfStmt({self.condition}, {self.then_branch}, {self.else_branch})"

class WhileStmt(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f"WhileStmt({self.condition}, {self.body})"

class DoWhileStmt(Stmt):
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition
    def __repr__(self):
        return f"DoWhileStmt({self.body}, {self.condition})"

class ForStmt(Stmt):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body
    def __repr__(self):
        return f"ForStmt({self.init}, {self.condition}, {self.update}, {self.body})"

class BreakStmt(Stmt):
    def __repr__(self):
        return "BreakStmt()"

class ContinueStmt(Stmt):
    def __repr__(self):
        return "ContinueStmt()"

class ErrorStmt(Stmt):
    def __init__(self, message, token):
        self.message = message
        self.token = token
    def __repr__(self):
        return f"ErrorStmt({self.message}, {self.token})"

class FuncDef(Stmt):
    def __init__(self, ret_type, name, params, body):
        self.ret_type = ret_type
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self):
        return f"FuncDef({self.ret_type}, {self.name}, {self.params}, {self.body})"

# --- Program ---
class Program(AST):
    def __init__(self, decls):
        self.decls = decls
    def __repr__(self):
        return f"Program({self.decls})"


# ===== Parser =====
class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.tokens = list(self.lexer.generate_tokens())
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    # ----- 工具 -----
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token}")

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def peek2(self):
        if self.pos + 2 < len(self.tokens):
            return self.tokens[self.pos + 2]
        return None

    # ----- 容錯 -----
    def error(self, msg):
        tok = self.current_token
        while tok.type not in ("SEMI", "RBRACE", "EOF"):
            self.pos += 1
            if self.pos < len(self.tokens):
                tok = self.tokens[self.pos]
            else:
                break
        if tok.type == "SEMI":
            self.eat("SEMI")
        return ErrorStmt(msg, tok)

    # ----- 入口 -----
    def parse(self):
        decls = []
        while self.current_token.type != "EOF":
            decls.append(self.declaration())
        return Program(decls)

    # ----- declaration -----
    def declaration(self):
        if self.current_token.type == "TYPE":
            if self.peek() and self.peek().type == "ID" and self.peek2() and self.peek2().type == "LPAREN":
                return self.func_def()
            else:
                return self.var_decl()
        return self.statement()

    # ----- statement -----
    def statement(self):
        try:
            tok = self.current_token
            if tok.type == "IF":
                return self.if_stmt()
            if tok.type == "WHILE":
                return self.while_stmt()
            if tok.type == "FOR":
                return self.for_stmt()
            if tok.type == "DO":
                return self.do_while_stmt()
            if tok.type == "RETURN":
                return self.return_stmt()
            if tok.type == "BREAK":
                self.eat("BREAK")
                self.eat("SEMI")
                return BreakStmt()
            if tok.type == "CONTINUE":
                self.eat("CONTINUE")
                self.eat("SEMI")
                return ContinueStmt()
            if tok.type == "LBRACE":
                return self.block()
            expr = self.expr()
            self.eat("SEMI")
            return expr
        except Exception as e:
            return self.error(str(e))

    # ----- block -----
    def block(self):
        self.eat("LBRACE")
        stmts = []
        while self.current_token.type != "RBRACE" and self.current_token.type != "EOF":
            if self.current_token.type == "TYPE":
                stmts.append(self.var_decl())
            else:
                stmts.append(self.statement())
        self.eat("RBRACE")
        return Block(stmts)

    # ----- block_or_stmt -----
    def block_or_stmt(self):
        if self.current_token.type == "LBRACE":
            return self.block()
        stmt = self.statement()
        return Block([stmt])

    # ----- var_decl -----
    def var_decl(self):
        var_type = self.current_token.value
        self.eat("TYPE")
        is_pointer = False
        if self.current_token.type == "MUL":
            is_pointer = True
            self.eat("MUL")
        name = self.current_token.value
        self.eat("ID")

        if self.current_token.type == "LBRACKET":
            return self.array_decl(var_type, name)

        value = None
        if self.current_token.type == "ASSIGN":
            self.eat("ASSIGN")
            value = self.expr()

        self.eat("SEMI")
        return VarDecl(var_type, name, value, is_pointer)

    def array_decl(self, var_type, name):
        self.eat("LBRACKET")
        size = self.expr()
        self.eat("RBRACKET")

        value = None
        if self.current_token.type == "ASSIGN":
            self.eat("ASSIGN")
            self.eat("LBRACE")
            value = []
            if self.current_token.type != "RBRACE":
                value.append(self.expr())
                while self.current_token.type == "COMMA":
                    self.eat("COMMA")
                    value.append(self.expr())
            self.eat("RBRACE")

        self.eat("SEMI")
        return ArrayDecl(var_type, name, size, value)

    # ----- func_def -----
    def func_def(self):
        ret_type = self.current_token.value
        self.eat("TYPE")
        name = self.current_token.value
        self.eat("ID")
        self.eat("LPAREN")
        params = []
        if self.current_token.type != "RPAREN":
            params.append(self.param())
            while self.current_token.type == "COMMA":
                self.eat("COMMA")
                params.append(self.param())
        self.eat("RPAREN")
        body = self.block()
        return FuncDef(ret_type, name, params, body)

    def param(self):
        var_type = self.current_token.value
        self.eat("TYPE")
        is_pointer = False
        if self.current_token.type == "MUL":
            is_pointer = True
            self.eat("MUL")
        name = self.current_token.value
        self.eat("ID")
        return VarDecl(var_type, name, None, is_pointer)

    # ----- if / while / do / for -----
    def if_stmt(self):
        self.eat("IF")
        self.eat("LPAREN")
        cond = self.expr()
        self.eat("RPAREN")
        then_branch = self.block_or_stmt()
        else_branch = None
        if self.current_token.type == "ELSE":
            self.eat("ELSE")
            else_branch = self.block_or_stmt()
        return IfStmt(cond, then_branch, else_branch)

    def while_stmt(self):
        self.eat("WHILE")
        self.eat("LPAREN")
        cond = self.expr()
        self.eat("RPAREN")
        body = self.block_or_stmt()
        return WhileStmt(cond, body)

    def do_while_stmt(self):
        self.eat("DO")
        body = self.block_or_stmt()
        self.eat("WHILE")
        self.eat("LPAREN")
        cond = self.expr()
        self.eat("RPAREN")
        self.eat("SEMI")
        return DoWhileStmt(body, cond)

    def for_stmt(self):
        self.eat("FOR")
        self.eat("LPAREN")

        init = None
        if self.current_token.type == "TYPE":
            init = self.var_decl()
        elif self.current_token.type != "SEMI":
            init = self.expr()
            self.eat("SEMI")
        else:
            self.eat("SEMI")

        condition = None
        if self.current_token.type != "SEMI":
            condition = self.expr()
        self.eat("SEMI")

        update = None
        if self.current_token.type != "RPAREN":
            update = self.expr()
        self.eat("RPAREN")

        body = self.block_or_stmt()
        return ForStmt(init, condition, update, body)

    # ----- return -----
    def return_stmt(self):
        self.eat("RETURN")
        val = self.expr()
        self.eat("SEMI")
        return Return(val)

    # ----- expressions -----
    def expr(self):
        return self.assignment()

    # assignment : logic_or (ASSIGN | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN) assignment?
    def assignment(self):
        node = self.logic_or()
        if self.current_token.type in ("ASSIGN", "ADD_ASSIGN", "SUB_ASSIGN", "MUL_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN"):
            op = self.current_token.type
            self.eat(op)
            value = self.assignment()
            return Assignment(node, value)  # op info 可以加到 Assignment 如果需要
        return node

    # logic_or : logic_and ('||' logic_and)*
    def logic_or(self):
        node = self.logic_and()
        while self.current_token.type == "OR_OR":
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.logic_and())
        return node

    # logic_and : bit_or ('&&' bit_or)*
    def logic_and(self):
        node = self.bit_or()
        while self.current_token.type == "AND_AND":
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.bit_or())
        return node

    # bit_or : bit_xor ('|' bit_xor)*
    def bit_or(self):
        node = self.bit_xor()
        while self.current_token.type == "BIT_OR":
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.bit_xor())
        return node

    # bit_xor : bit_and ('^' bit_and)*
    def bit_xor(self):
        node = self.bit_and()
        while self.current_token.type == "BIT_XOR":
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.bit_and())
        return node

    # bit_and : equality ('&' equality)*
    def bit_and(self):
        node = self.equality()
        while self.current_token.type == "BIT_AND":
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.equality())
        return node

    # equality : rel (('==' | '!=') rel)*
    def equality(self):
        node = self.rel()
        while self.current_token.type in ("EQ", "NEQ"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.rel())
        return node

    # rel : shift ('<' | '>' | '<=' | '>=') shift
    def rel(self):
        node = self.shift()
        while self.current_token.type in ("LT", "GT", "LE", "GE"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.shift())
        return node

    # shift : add (('<<' | '>>') add)*
    def shift(self):
        node = self.add()
        while self.current_token.type in ("LSHIFT", "RSHIFT"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.add())
        return node

    # add : mul ('+' | '-')*
    def add(self):
        node = self.mul()
        while self.current_token.type in ("PLUS", "MINUS"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.mul())
        return node

    # mul : unary ('*' | '/' | '%')*
    def mul(self):
        node = self.unary()
        while self.current_token.type in ("MUL", "DIV", "MOD"):
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.unary())
        return node

    # unary : ('+' | '-' | '!' | '~' | '*' | '&' | '++' | '--') unary | primary | post_inc_dec
    def unary(self):
        tok = self.current_token
        if tok.type in ("PLUS", "MINUS", "NOT", "BIT_NOT", "MUL", "AMP"):
            self.eat(tok.type)
            if tok.type == "PLUS":
                return UnaryOp("PLUS", self.unary())
            elif tok.type == "MINUS":
                return UnaryOp("MINUS", self.unary())
            elif tok.type == "NOT":
                return UnaryOp("NOT", self.unary())
            elif tok.type == "BIT_NOT":
                return UnaryOp("BIT_NOT", self.unary())
            elif tok.type == "MUL":
                return Deref(self.unary())
            elif tok.type == "AMP":
                return AddressOf(self.unary())
        if tok.type in ("INC", "DEC"):  # 前置 ++x / --x
            self.eat(tok.type)
            return UnaryOp(tok.type, self.unary())
        return self.primary()

    # primary : NUMBER | CHAR | ID | ID '(' args ')' | ID '[' expr ']' | '(' expr ')' | post_inc_dec
    def primary(self):
        tok = self.current_token
        if tok.type == "NUMBER":
            self.eat("NUMBER")
            node = Number(tok.value)
        elif tok.type == "CHAR":
            self.eat("CHAR")
            node = Char(tok.value)
        elif tok.type == "ID":
            name = tok.value
            self.eat("ID")
            node = Identifier(name)
            if self.current_token.type == "LPAREN":  # 函式呼叫
                self.eat("LPAREN")
                args = []
                if self.current_token.type != "RPAREN":
                    args.append(self.expr())
                    while self.current_token.type == "COMMA":
                        self.eat("COMMA")
                        args.append(self.expr())
                self.eat("RPAREN")
                node = Call(Identifier(name), args)
            if self.current_token.type == "LBRACKET":  # 陣列
                self.eat("LBRACKET")
                index = self.expr()
                self.eat("RBRACKET")
                node = ArrayAccess(Identifier(name), index)
        elif tok.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
        else:
            return self.error(f"Unexpected token {tok}")

        # 後置 ++ / --
        if self.current_token.type in ("INC", "DEC"):
            op = self.current_token.type
            self.eat(op)
            node = UnaryOp(op+"_POST", node)
        return node