from copy import copy
import sys
from typing import TypeAlias
from src.exception import InterpError
from src.parser import get_parser
from src.lexer import get_lexer
from src.logic import *


class NodeVisitor:
    def visit(self, node):
        if isinstance(node, str):
            print(node)
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


Id2Var: TypeAlias = dict[int, str]
Var2Id: TypeAlias = dict[str, int]


# [x] id -> to any variable
# [x] name -> from stack -> val
# [x] name -> from stack -> id
#
# Varibale creation:
# return явный и неявный
# неявный return -> expr


class Variables:
    STACK_MAX_DEPTH = 1000

    def __init__(self):
        self.counter = 0
        self.skopes: list[Var2Id] = [{} for _ in range(self.STACK_MAX_DEPTH)]
        self.ids: Id2Var = dict()

    def init_var(self, var_name: str, skope: int = 0):
        _id = self.counter
        self.counter += 1
        cur_sckope = self.skopes[skope]
        self.ids[_id] = var_name
        cur_sckope[var_name] = _id

    @classmethod
    def parse_name(cls, var_name: str) -> tuple[int, str]:
        s, n = var_name.split(":", 1)
        return int(s), n

    @classmethod
    def calc_name(cls, name: str, stack: list) -> str:
        return f"{len(stack)}:{name}"

    def get_id_by_name(self, var_name: str) -> int:
        skope, name = self.parse_name(var_name)
        return self.skopes[skope][name]  # Exception

    def get_name_by_id(self, vid: int) -> str:
        return self.ids[vid]  # Exception


class Interpreter(NodeVisitor):
    def __init__(self, robot: Robot):
        self.robot: Robot = robot
        self.global_env = {}
        self.current_env = self.global_env
        self.variables = Variables()
        self.call_stack = []  # Стек вызовов функций

    def visit_LenOf(self, node):
        # Получаем выражение из узла
        expr = self.visit(node.expr)

        if isinstance(expr, (int, float, str)):
            return 1
        elif isinstance(expr, list):
            return len(expr)
        else:
            raise Exception(
                "Cannot determine the size of the given expression."
            )

    def visit_Print(self, node):
        value = self.visit(node.expr)
        print(value)
        return value

    def visit_AddressOf(self, node: AddressOf) -> int:
        var_name = Variables.calc_name(node.name, self.call_stack)
        return self.variables.get_id_by_name(var_name)

    def visit_ArrayAssignment(self, node: ArrayAssignment):
        # Access the array using the correct attribute
        array = self.global_env.get(node.array_name)
        index = self.visit(node.index)
        value = self.visit(node.value)

        if array is None:
            raise NameError(f"Name '{node.array_name}' is not defined")

        # Assuming array is a list or a similar structure
        arr_size = len(array)
        if index >= arr_size:
            raise InterpError(
                f"var (array) `{node.array_name}` has max length of"
                f" {arr_size}, but got index {index}"
            )
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

    def visit_ArrayDecl(self, node: ArrayDecl):
        var_name = node.var_name
        if node.size_expr is not None:
            if isinstance(node.size_expr, (Num, Var, BinOp)):
                size = self.visit(node.size_expr)
            else:
                size = node.size_expr
            # Прямое использование, так как это число
        # Обновление глобальной среды
        if size <= 0:
            raise InterpError(f"Illegal array size. Got {size}")
        self.global_env[var_name] = [0] * size
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

    def visit_Move(self, node: Move):
        direction = node.direction
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

        # print(f"BinOp: left={left}, right={right}, op={node.op.type}")

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

    def visit_Num(self, node: Num):
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
        self.variables.init_var(var_name, len(self.call_stack))
        return self.current_env[var_name]

    def visit_Unarop(self, node: Unarop):
        uid = self.visit(node.expr)

        name = self.variables.get_name_by_id(uid)
        if name in self.current_env:
            return self.current_env[name]
        elif name in self.global_env[name]:
            return self.global_env[name]
        raise InterpError(f"Incorrect addr: {uid}")

    def visit_VarDecl(self, node: VarDecl):
        var_name = node.var_name
        if node.init_value:
            self.current_env[var_name] = self.visit(node.init_value)
            self.variables.init_var(var_name, len(self.call_stack))
        else:
            self.current_env[var_name] = None
        return self.current_env[var_name]

    def visit_FunctionDecl(self, node: FunctionDecl):
        # print(f"Defining function {node.name}")
        self.global_env[node.name] = node
        return node

    def visit_FunctionCall(self, node: FunctionCall):
        func: FunctionDecl = self.global_env.get(node.name)
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

    def visit_If(self, node: If):
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

    def interpret(self, tree: list[AST]):
        try:
            if tree is None:
                print("AST is None. No code to interpret.")
                return
            result = None
            self.current_env = self.global_env
            for node in tree:
                result = self.visit(node)
        except InterpError as e:
            print(f"[error] {str(e)}", file=sys.stderr)
        except Exception:
            raise
        return result


def test_interpreter(code):
    robot = Robot(grid=[[0] * 5 for _ in range(5)])
    interpreter = Interpreter(robot)
    parser = get_parser()
    result = interpreter.interpret(
        parser.parse(code, lexer=get_lexer(), debug=True)
    )
    return result
