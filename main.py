from copy import copy
import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ""
        while self.current_char is not None and (
            self.current_char.isdigit() or self.current_char == "."
        ):
            result += self.current_char
            self.advance()
        if "." in result:
            return float(result)
        else:
            return int(result)

    def string(self):
        result = ""
        self.advance()  # Skip the opening double quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip the closing double quote
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == "[":
                self.advance()
                if self.current_char == "]":
                    self.advance()
                    return Token("EMPTY_ARRAY", "[]")
                else:
                    return Token("LSQUARE", "[")
            if self.current_char == "]":
                self.advance()
                return Token("RSQUARE", "]")
            if self.current_char.isdigit() or self.current_char == ".":
                return Token("NUMBER", self.number())
            if self.current_char == '"':
                return Token("STRING", self.string())
            if self.current_char.isalpha():
                result = ""
                while (
                    self.current_char is not None
                    and self.current_char.isalnum()
                ):
                    result += self.current_char
                    self.advance()
                return self.keyword_or_identifier(result)
            if self.current_char == ":":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("ASSIGN", ":=")
            if self.current_char == "+":
                self.advance()
                return Token("PLUS", "+")
            if self.current_char == "-":
                self.advance()
                return Token("MINUS", "-")
            if self.current_char == "*":
                self.advance()
                return Token("MUL", "*")
            if self.current_char == "/":
                self.advance()
                return Token("DIV", "/")
            if self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("LE", "<=")
                return Token("LT", "<")
            if self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("GE", ">=")
                return Token("GT", ">")
            if self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                return Token("NE", "!=")
            if self.current_char == "=":
                self.advance()
                return Token("EQ", "=")
            if self.current_char == ";":
                self.advance()
                return Token("SEMI", ";")
            if self.current_char == ",":
                self.advance()
                return Token("COMMA", ",")
            if self.current_char == "(":
                self.advance()
                return Token("LPAREN", "(")
            if self.current_char == ")":
                self.advance()
                return Token("RPAREN", ")")
            if self.current_char == "{":
                self.advance()
                return Token("LBRACE", "{")
            if self.current_char == "}":
                self.advance()
                return Token("RBRACE", "}")
            if self.current_char == "&":
                self.advance()
                return Token("AMPERSAND", "&")
            if self.current_char == "?":
                self.advance()
                return Token("QUESTION_MARK", "?")
            raise Exception(f"Invalid character: {self.current_char}")
        return Token("EOF", None)

    def keyword_or_identifier(self, result):
        keywords = {
            "mutable": "MUTABLE",
            "integer": "INTEGER_TYPE",
            "string": "STRING_TYPE",
            "pointer": "POINTER_TYPE",
            "array": "ARRAY_TYPE",
            "of": "OF",
            "function": "FUNCTION",
            "if": "IF",
            "else": "ELSE",
            "while": "WHILE",
            "return": "RETURN",
            "top": "TOP",
            "bottom": "BOTTOM",
            "left": "LEFT",
            "right": "RIGHT",
            "timeshift": "TIMESHIFT",
            "bind": "BIND",
            "print": "PRINT",
            "instead": "INSTEAD",
        }
        return Token(keywords.get(result, "IDENTIFIER"), result)

class AST:
    pass

class ArrayDecl:
    def __init__(self, var_name, size_expr):
        self.var_name = var_name
        self.size_expr = size_expr

class PointerDecl(AST):
    def __init__(
        self,
        var_type,
        var_name,
        init_value=None,
        mutable=False,
        obj_mutable=False,
    ):
        self.var_type = var_type
        self.var_name = var_name
        self.init_value = init_value
        self.mutable = mutable
        self.obj_mutable = obj_mutable

class ArrayAccess(AST):
    def __init__(self, array_name, index_expr):
        self.array_name = array_name
        self.index_expr = index_expr

class SizeOf(AST):
    def __init__(self, identifier):
        self.identifier = identifier

class Move(AST):
    def __init__(self, direction):
        self.direction = direction

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Str(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Return(AST):
    def __init__(self, expr):
        self.expr = expr

class VarDecl(AST):
    def __init__(self, var_type, var_name, init_value=None, mutable=False):
        self.var_type = var_type
        self.var_name = var_name
        self.init_value = init_value
        self.mutable = mutable

class If(AST):
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

class While(AST):
    def __init__(self, condition, body, instead_body=None):
        self.condition = condition
        self.body = body
        self.instead_body = instead_body 

class Print(AST):
    def __init__(self, expr):
        self.expr = expr

class FunctionDecl(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(AST):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class IfStatement(AST):
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

class ArrayAssignment(AST):
    def __init__(self, array_name, index, value):
        self.array_name = array_name
        self.index = index
        self.value = value

class AddressOf(AST):
    def __init__(self, expr):
        self.expr = expr

class Len(AST):
    def __init__(self, expr):
        self.expr = expr


class Parser:

    def address_of(self):
        self.eat("AMPERSAND")
        expr = self.expr()  
        self.eat("SEMI")
        return AddressOf(expr)
    
    def Return_Len(self):
        self.eat("QUESTION_MARK")
        expr = self.expr()  
        self.eat("SEMI")
        return Len(expr)
    
    def assignment(self):
        left = self.current_token

        if left.type == "IDENTIFIER":
            self.eat("IDENTIFIER")

            # Если следующий токен - LSQUARE, то это доступ к элементу массива
            if self.current_token.type == "LSQUARE":
                self.eat("LSQUARE")
                index = self.expr()
                self.eat("RSQUARE")

                # Ожидаем оператор присваивания
                self.eat("ASSIGN")
                value = self.expr()
                self.eat("SEMI")
                return ArrayAssignment(
                    array_name=left.value, index=index, value=value
                )
            else:
                # Обычное присваивание переменной
                self.eat("ASSIGN")
                right = self.expr()
                self.eat("SEMI")
                return Assign(
                    left=Var(left), op=self.current_token, right=right
                )

    def print_statement(self):
        self.eat("PRINT")
        self.eat("LPAREN")
        expr = self.expr()  # Парсим выражение, которое нужно вывести
        self.eat("RPAREN")
        self.eat("SEMI")
        return Print(expr)

    def array_assignment(self):
        var_name = self.current_token.value
        self.eat("IDENTIFIER")
        self.eat("LSQUARE")
        index = (
            self.expr()
        )  # предполагается, что expr возвращает значение индекса
        self.eat("RSQUARE")
        self.eat("ASSIGN")
        value = (
            self.expr()
        )  # предполагается, что expr возвращает значение для присваивания
        self.eat("SEMI")
        return ArrayAssignment(var_name, index, value)

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    '''
    def pointer_decl(self):
        print(
            f"Current token: {self.current_token}"
        )  # добавьте это для отладки
        mutable = False
        if self.current_token.type == "MUTABLE":
            self.eat("MUTABLE")
            mutable = True
        self.eat("POINTER_TYPE")
        obj_mutable = False
        if self.current_token.type == "MUTABLE":
            self.eat("MUTABLE")
            obj_mutable = True
        var_type = self.current_token.value
        self.eat("IDENTIFIER")
        init_value = None
        if self.current_token.type == "ASSIGN":
            self.eat("ASSIGN")
            init_value = self.expr()
        return PointerDecl(
            var_type=var_type,
            var_name=self.current_token.value,
            init_value=init_value,
            mutable=mutable,
            obj_mutable=obj_mutable,
        )
    '''
    def pointer_decl(self):
        mutable = False
        if self.current_token.type == "MUTABLE":
            self.eat("MUTABLE")
            mutable = True
        
        
        self.eat("POINTER_TYPE")
        
        obj_mutable = False
        if self.current_token.type == "MUTABLE":
            self.eat("MUTABLE")
            obj_mutable = True
        
       
        var_type = self.current_token.value
        self.eat(self.current_token.type)  
        
       
        var_name = self.current_token.value
        self.eat("IDENTIFIER")
        
        
        init_value = None
        if self.current_token.type == "ASSIGN":
            self.eat("ASSIGN")
            init_value = self.expr()

        self.eat("SEMI")
        
        return PointerDecl(var_type=var_type, var_name=var_name, init_value=init_value, mutable=mutable, obj_mutable=obj_mutable)


    def array_decl(self):
        self.eat("ARRAY_TYPE")
        self.eat("INTEGER_TYPE")
        self.eat("OF")
        var_name = self.current_token.value
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        size_expr = self.current_token.value
        self.eat("NUMBER")
        self.eat("RPAREN")
        self.eat("SEMI")
        return ArrayDecl(var_name=var_name, size_expr=size_expr)

    def array_access(self):
        array_name = self.current_token.value
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        index_expr = self.expr()
        self.eat("RPAREN")
        return ArrayAccess(array_name=array_name, index_expr=index_expr)

    def move_statement(self):
        direction = self.current_token
        if direction.type in ("TOP", "BOTTOM", "LEFT", "RIGHT"):
            self.eat(direction.type)
            self.eat("SEMI")
            return Move(direction)
        else:
            self.error()

    def error(self):
        raise Exception(
            f"Invalid syntax: Unexpected token {self.current_token.type} with"
            f" value {self.current_token.value}"
        )

    def eat(self, token_type):
        print(
            f"Eating token: {self.current_token.type} with value"
            f" {self.current_token.value}"
        )
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == "NUMBER":
            self.eat("NUMBER")
            return Num(token)
        elif token.type == "STRING":
            self.eat("STRING")
            return Str(token)
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            if self.current_token.type == "LPAREN":  # Это вызов функции
                return self.function_call_with_identifier(token)
            return Var(token)
        elif token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
            return node

    def function_call_with_identifier(self, token):
        func_name = token.value
        self.eat("LPAREN")
        arguments = []
        if self.current_token.type != "RPAREN":
            arguments.append(self.expr())
            while self.current_token.type == "COMMA":
                self.eat("COMMA")
                arguments.append(self.expr())
        self.eat("RPAREN")
        return FunctionCall(name=func_name, arguments=arguments)

    def term(self):
        node = self.factor()
        while self.current_token.type in ("MUL", "DIV"):
            token = self.current_token
            if token.type == "MUL":
                self.eat("MUL")
            elif token.type == "DIV":
                self.eat("DIV")
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (
            "PLUS",
            "MINUS",
            "GT",
            "LT",
            "GE",
            "LE",
            "EQ",
            "NE",
        ):
            token = self.current_token
            if token.type == "PLUS":
                self.eat("PLUS")
            elif token.type == "MINUS":
                self.eat("MINUS")
            elif token.type == "GT":
                self.eat("GT")
            elif token.type == "LT":
                self.eat("LT")
            elif token.type == "GE":
                self.eat("GE")
            elif token.type == "LE":
                self.eat("LE")
            elif token.type == "EQ":
                self.eat("EQ")
            elif token.type == "NE":
                self.eat("NE")
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def comparison(self):
        node = self.expr()
        while self.current_token.type in ("LT", "GT", "EQ"):
            token = self.current_token
            if token.type == "LT":
                self.eat("LT")
            elif token.type == "GT":
                self.eat("GT")
            elif token.type == "EQ":
                self.eat("EQ")
            node = BinOp(left=node, op=token, right=self.expr())
        return node

    def return_statement(self):
        self.eat("RETURN")
        expr_node = self.expr()
        self.eat("SEMI")
        return Return(expr_node)

    def statement(self):
        if self.current_token.type == "FUNCTION":
            return self.function_decl()
        elif self.current_token.type == "IF":
            return self.if_statement()
        elif self.current_token.type == "WHILE":
            return self.while_statement()
        elif self.current_token.type == "PRINT":
            return self.print_statement()
        elif self.current_token.type in ("TOP", "BOTTOM", "LEFT", "RIGHT"):
            return self.move_statement()
        elif (
            self.current_token.type == "IDENTIFIER"
            and self.peek().type == "LPAREN"
        ):
            return self.function_call()
        elif self.current_token.type == "RETURN":
            return self.return_statement()
        elif self.current_token.type =="AMPERSAND":
            return self.address_of()
        elif self.current_token.type == "QUESTION_MARK":
            return self.Return_Len()
        elif self.current_token.type == "POINTER_TYPE":
            return self.pointer_decl()
        elif self.current_token.type == "IDENTIFIER":
            return self.assignment()
        elif self.current_token.type == "ARRAY_TYPE":
            return self.array_decl()
        elif (
            self.current_token.type == "IDENTIFIER"
            and self.peek().type == "LSQUARE"
        ):
            return self.array_assignment()
        else:
            self.error()

    def function_decl(self):
        self.eat("FUNCTION")
        func_name = self.current_token.value
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        params = []
        if self.current_token.type == "IDENTIFIER":
            params.append(self.current_token.value)
            self.eat("IDENTIFIER")
            while self.current_token.type == "COMMA":
                self.eat("COMMA")
                params.append(self.current_token.value)
                self.eat("IDENTIFIER")
        self.eat("RPAREN")
        self.eat("LBRACE")
        body = []
        while self.current_token.type != "RBRACE":
            body.append(self.statement())
        self.eat("RBRACE")
        return FunctionDecl(name=func_name, params=params, body=body)

    def function_call(self):
        func_name = self.current_token.value
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        arguments = []
        if self.current_token.type in ("NUMBER", "STRING", "IDENTIFIER"):
            arguments.append(self.expr())
            while self.current_token.type == "COMMA":
                self.eat("COMMA")
                arguments.append(self.expr())
        self.eat("RPAREN")
        self.eat("SEMI")
        return FunctionCall(name=func_name, arguments=arguments)

    def variable(self):
        var_node = Var(self.current_token)
        self.eat("IDENTIFIER")
        return var_node

    def if_statement(self):
        self.eat("IF")  # Ожидаем ключевое слово 'if'
        self.eat("LPAREN")  # Ожидаем '('
        condition = self.expr()  # Парсим выражение условия
        self.eat("RPAREN")  # Ожидаем ')'
        self.eat("LBRACE")  # Ожидаем '{'

        # Парсим тело if-блока
        if_body = []
        while self.current_token.type != "RBRACE":
            if_body.append(self.statement())
        self.eat("RBRACE")  # Ожидаем '}'

        # Парсим else-блок, если он есть
        else_body = []
        if self.current_token.type == "ELSE":
            self.eat("ELSE")
            self.eat("LBRACE")
            while self.current_token.type != "RBRACE":
                else_body.append(self.statement())
            self.eat("RBRACE")
        # return {'type': 'IF_STATEMENT', 'condition': condition, 'if_body': if_body, 'else_body': else_body}
        return IfStatement(condition, if_body, else_body)

    def while_statement(self):
        self.eat("WHILE")
        self.eat("LPAREN")  # This was missing in the original implementation
        # Parse the condition inside the parentheses
        condition = self.comparison()
        self.eat("RPAREN")  # This was missing in the original implementation
        self.eat("LBRACE")
        body = []
        while self.current_token.type != "RBRACE":
            body.append(self.statement())
        self.eat("RBRACE")

        # Check for the optional 'instead' block
        instead_body = None
        if self.current_token.type == "INSTEAD":
            self.eat("INSTEAD")
            self.eat("LBRACE")
            instead_body = []
            while self.current_token.type != "RBRACE":
                instead_body.append(self.statement())
            self.eat("RBRACE")

        return While(condition=condition, body=body, instead_body=instead_body)

    def parse(self):
        statements = []
        while self.current_token.type != "EOF":
            statements.append(self.statement())
        return statements

    def peek(self):
        pos = self.lexer.pos
        current_char = self.lexer.current_char
        token = self.lexer.get_next_token()
        self.lexer.pos = pos
        self.lexer.current_char = current_char
        return token

class NodeVisitor:
    def visit(self, node):
        #print(f"Visiting node: {node}")
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def print_ast(self, node, indent=""):
        if isinstance(node, list):
            for n in node:
                self.print_ast(n, indent)
        else:
            print(f"{indent}{type(node).__name__}: {self.node_to_dict(node)}")
            indent += "  "
            for child in self.node_to_dict(node).values():
                if isinstance(child, (AST, list)):
                    self.print_ast(child, indent)

    def node_to_dict(self, node):
        if hasattr(node, "__dict__"):
            return vars(node)
        elif hasattr(node, "__slots__"):
            return {
                slot: getattr(node, slot)
                for slot in getattr(node, "__slots__")
            }
        else:
            return {}

class Robot:
    def __init__(self, grid, start_position=(0, 0)):
        # grid - это двумерный список, представляющий карту. 0 - свободная клетка, 1 - препятствие.
        self.grid = grid
        self.position = start_position  # Текущая позиция робота (x, y)

    def move_top(self):
        x, y = self.position
        if y > 0 and self.grid[y - 1][x] == 0:
            self.position = (x, y - 1)
            return 1
        print(f"Cannot move top from position {self.position}")
        return 0

    def move_bottom(self):
        x, y = self.position
        if y < len(self.grid) - 1 and self.grid[y + 1][x] == 0:
            self.position = (x, y + 1)
            return 1
        print(f"Cannot move bottom from position {self.position}")
        return 0

    def move_left(self):
        x, y = self.position
        if x > 0 and self.grid[y][x - 1] == 0:
            self.position = (x - 1, y)
            return 1
        print(f"Cannot move left from position {self.position}")
        return 0

    def move_right(self):
        x, y = self.position
        if x < len(self.grid[0]) - 1 and self.grid[y][x + 1] == 0:
            self.position = (x + 1, y)
            return 1
        print(f"Cannot move right from position {self.position}")
        return 0


class Interpreter(NodeVisitor):
    def __init__(self, robot):
        self.robot = robot
        self.global_env = {}
        self.current_env = self.global_env
        self.call_stack = []  # Стек вызовов функций

    def visit_Len(self, node):
        # Получаем выражение из узла
        expr = self.visit(node.expr)

        if isinstance(expr, int):  
            return 1
        elif isinstance(expr, float): 
            return 1
        elif isinstance(expr, str):  
            return 1
        elif isinstance(expr, list):  
            return len(expr) 
        else:
            raise Exception("Cannot determine the size of the given expression.")

    def visit_Print(self, node):
        value = self.visit(node.expr)
        print(value)
        return value
    
    def visit_AddressOf(self, node):
        value = self.visit(node.expr)
        if isinstance(value, list):
            return f"Address of array element: {id(value)}"
        elif isinstance(value, (int, float, str)):
            return f"Address of value: {id(value)}"
        else:
            raise Exception("Cannot get address of the given expression.")
    '''
    def visit_AddressOf(self, node):
        # Предполагаем, что node.expr это строка, представляющая ключ
        key = node.expr
        
        # Проверяем, есть ли ключ в глобальном словаре
        if key in global_env:
            value = global_env[key]
            # Возвращаем адрес значения из глобального словаря
            return f"Address of value with key '{key}': {id(value)}"
        else:
            raise Exception(f"Key '{key}' not found in global environment.")
    '''
    def visit_ArrayAssignment(self, node):
        # Access the array using the correct attribute
        array = self.global_env.get(node.array_name)
        index = self.visit(node.index)
        value = self.visit(node.value)

        if array is None:
            raise NameError(f"Name '{node.array_name}' is not defined")

        # Assuming array is a list or a similar structure
        array[index] = value

        return value

    def visit_Assignment(self, node):
        self.global_env[node.left.value] = self.visit(node.right)

    def visit_PointerDecl(self, node):
        var_name = node.var_name
        if node.init_value:
            self.global_env[var_name] = self.visit(node.init_value)
        else:
            self.global_env[var_name] = None
        return self.global_env[var_name]

    def visit_ArrayDecl(self, node):
        var_name = node.var_name
        if node.size_expr is not None:
            size = node.size_expr  # Прямое использование, так как это число
        else:
            size = 10  # Default size

        # Обновление глобальной среды
        self.global_env[var_name] = [None] * size
        return self.global_env[var_name]

    def visit_ArrayAccess(self, node):
        array = self.global_env.get(node.array_name)
        if array is None:
            raise Exception(f"Array {node.array_name} not found.")
        index = self.visit(node.index_expr)
        if not 0 <= index < len(array):
            raise Exception(f"Index {index} out of bounds.")
        return array[index]

    def visit_SizeOf(self, node):
        identifier = node.identifier
        if identifier in self.global_env:
            value = self.global_env[identifier]
            if isinstance(value, list):
                return len(value)
            else:
                return 1
        raise Exception(f"Undefined identifier: {identifier}")

    def visit_Move(self, node):
        direction = node.direction.value
        try:
            if direction == "top":
                result = self.robot.move_top()
            elif direction == "bottom":
                result = self.robot.move_bottom()
            elif direction == "left":
                result = self.robot.move_left()
            elif direction == "right":
                result = self.robot.move_right()
            else:
                raise Exception(f"Unknown direction: {direction}")
            print(
                f"Moved {direction}. Current position: {self.robot.position}"
            )
            return result
        except Exception as e:
            print(f"Error during movement: {e}")

    def visit_BinOp(self, node: BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)

        #print(f"BinOp: left={left}, right={right}, op={node.op.type}")

        if left is None or right is None:
            raise Exception(
                f"Unexpected None value: left={left}, right={right}"
            )

        if node.op.type == "PLUS":
            return left + right
        elif node.op.type == "MINUS":
            return left - right
        elif node.op.type == "MUL":
            return left * right
        elif node.op.type == "DIV":
            return left / right
        elif node.op.type == "LT":
            return left < right
        elif node.op.type == "GT":
            return left > right
        elif node.op.type == "EQ":
            return left == right

    def visit_Num(self, node):
        return node.value

    def visit_Str(self, node):
        return node.value

    def visit_Var(self, node):
        var_name = node.value
        if var_name in self.current_env:
            return self.current_env[var_name]
        elif var_name in self.global_env:
            return self.global_env[var_name]
        else:
            raise Exception(f"Undefined variable: {var_name}")

    def visit_Assign(self, node):
        var_name = node.left.value
        self.current_env[var_name] = self.visit(node.right)
        return self.current_env[var_name]

    def visit_VarDecl(self, node):
        var_name = node.var_name
        if node.init_value:
            self.current_env[var_name] = self.visit(node.init_value)
        else:
            self.current_env[var_name] = None
        return self.current_env[var_name]

    def visit_FunctionDecl(self, node):
        #print(f"Defining function {node.name}")
        self.global_env[node.name] = node
        return node

    def visit_FunctionCall(self, node):
        func = self.global_env.get(node.name)
        if not func:
            raise Exception(f"Function {node.name} is not defined")

        # Создание новой локальной среды для вызова функции
        local_env = {}
        for param, arg in zip(func.params, node.arguments):
            local_env[param] = self.visit(arg)

        # Выполнение тела функции в локальной среде
        tmp = copy(self.current_env)
        self.call_stack.append(self.current_env)
        self.current_env = tmp | local_env
        result = None
        for statement in func.body:
            result = self.visit(statement)
            if isinstance(result, Return):
                result = self.visit(
                    result.expr
                )  # Извлечение возвращаемого значения
                break
        self.current_env = self.call_stack.pop()
        return result

    def visit_Return(self, node):
        # return self.visit(node.expr)
        value = self.visit(node.expr)
        if value is None:
            raise Exception("Return value is None")
        return value

    def visit_IfStatement(self, node):
        condition_result = self.visit(node.condition)
        res = None
        if condition_result:
            for stmt in node.true_branch:
                res = self.visit(stmt)
        elif node.false_branch:
            for stmt in node.false_branch:
                res = self.visit(stmt)
        return res

    def visit_While(self, node):
        res = None
        c = 0
        while self.visit(node.condition):  # Проверка условия
            c += 1
            for statement in node.body:  # Выполнение тела цикла
                res = self.visit(statement)
        if c > 0:
            return res

        # Если цикл не выполнялся ни разу и есть альтернативное тело, выполняем его
        res = None
        if node.instead_body:
            for statement in node.instead_body:
                res = self.visit(statement)
        return res

    def interpret(self, tree):
        if tree is None:
            print("AST is None. No code to interpret.")
            return
        result = None
        self.current_env = self.global_env
        for node in tree:
            result = self.visit(node)
        return result


# Пример сетки с препятствиями
grid = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0],
]

# Пример начальной позиции
start_position = (2, 2)

# Инициализация робота
robot = Robot(grid=grid, start_position=start_position)

# Код для тестирования перемещений
test_code = """
top;
left;
bottom;
right;

function add(x, y) {
    return x + y;
}

function multiply(x, y) {
    return x * y;
}

function subtract(x, y) {
    return x - y;
}

function divide(x, y) {
    return x / y;
}

function div(x, y) {
    if (y > 0) {
        return x / y;
    } else {
        return 1;
    }
}

add(5, 10);
multiply(2, 3);
subtract(10, 9);
divide(10, 5);
div(1, 2);

function moveRobot() {
    top;
    top;
    left;
    bottom;
    right;
    right;
}

moveRobot();

array integer of myArray (5);
myArray[2] := 2;
myArray[1] := 1;
myArray[0] := 0;

function factorial(n) {
    if (n = 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

print(factorial(5));

function testWhile(x) {
    while (x < 5) {
        x := x + 1;
    } instead {
        x := 122;
    }
    return x;
}

print(testWhile(2));
pointer integer p := 1234;

function xuy(x){
    if(x <= 1){
        return 0;
    }else{
        return 1;
    }
}
print(xuy(1));
"""

test ="""
pointer integer p := 1234;
&p;
x := 10;
?x;
array integer of myArray (5);
myArray[2] := 2;
myArray[1] := 1;
myArray[0] := 0;
?myArray;
"""

lexer = Lexer(test)
parser = Parser(lexer)
ast = parser.parse()

print("AST:")
visitor = NodeVisitor()
if ast is not None:
    visitor.print_ast(ast)

interpreter = Interpreter(robot)
result = interpreter.interpret(ast)
print("Interpreter result:", result)
print("Global Environment:", interpreter.global_env)
print(f"Робот находится на позиции: {robot.position}")
