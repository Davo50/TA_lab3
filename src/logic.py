from ply.lex import LexToken


class ValueMixin:

    @property
    def value(self):
        return self.token


class AST:
    pass


class ArrayDecl(AST):
    def __init__(self, var_name, size_expr):
        self.var_name = var_name
        self.size_expr = size_expr


class PointerDecl(AST):
    def __init__(self, var_type, var_name, init_value=None, mutable=False):
        self.var_type = var_type
        self.var_name = var_name
        self.init_value = init_value
        self.mutable = mutable


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
    def __init__(self, left, op: LexToken, right):
        self.left = left
        self.op = op
        self.right = right


class Num(AST, ValueMixin):
    def __init__(self, token):
        self.token = token


class Str(AST, ValueMixin):
    def __init__(self, token):
        self.token = token


class Var(AST, ValueMixin):
    def __init__(self, token):
        self.token = token


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
        self.params: list[str] = params
        self.body = body


class FunctionCall(AST):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class ArrayAssignment(AST):
    def __init__(self, array_name, index, value):
        self.array_name = array_name
        self.index = index
        self.value = value


class AddressOf(AST):
    def __init__(self, name):
        self.name = name


class LenOf(AST):
    def __init__(self, expr):
        self.expr = expr


class Unarop(AST):
    def __init__(self, expr):
        self.expr = expr
