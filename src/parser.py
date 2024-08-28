import ply.yacc as yacc

from src.lexer import *
from src.logic import *

# Определяем приоритеты операций
precedence = (
    # ("nonassoc", "LESSTHAN", "GREATERTHAN"),
    ("left", "PLUS", "MINUS"),
    ("left", "MUL", "DIV"),
    ("right", "UMINUS"),
    ("right", "QUESTION_MARK", "AMPERSAND", "UMUL"),
)


def p_program(p):
    """program : statement_list"""
    p[0] = p[1]


def p_statement_list(p):
    """statement_list : statement
    | statement_list statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """statement : assignment
    | print_statement
    | if_statement
    | while_statement
    | return_statement
    | move_statement
    | function_decl
    | array_decl
    | pointer_decl
    | address_of
    | function_call_stmt"""
    p[0] = p[1]


def p_assignment(p):
    """assignment : IDENTIFIER ASSIGN expr SEMI
    | IDENTIFIER LSQUARE expr RSQUARE ASSIGN expr SEMI
    | IDENTIFIER ASSIGN function_call SEMI"""
    if len(p) == 5:
        p[0] = Assign(Var(p[1]), p[2], p[3])
    else:
        p[0] = ArrayAssignment(p[1], p[3], p[6])


def p_print_statement(p):
    """print_statement : PRINT LPAREN expr RPAREN SEMI"""
    p[0] = Print(p[3])


def p_if_statement(p):
    """if_statement : IF LPAREN expr RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
    | IF LPAREN expr RPAREN LBRACE statement_list RBRACE"""
    if len(p) == 12:
        p[0] = If(p[3], p[6], p[10])
    else:
        p[0] = If(p[3], p[6])


def p_while_statement(p):
    """while_statement : WHILE LPAREN expr RPAREN LBRACE statement_list RBRACE
    | WHILE LPAREN expr RPAREN LBRACE statement_list RBRACE INSTEAD LBRACE statement_list RBRACE
    """
    if len(p) == 8:
        p[0] = While(p[3], p[6])
    else:
        p[0] = While(p[3], p[6], p[10])


def p_return_statement(p):
    """return_statement : RETURN expr SEMI"""
    p[0] = Return(p[2])


def p_move_statement(p):
    """move_statement : direction SEMI"""
    p[0] = Move(p[1])


def p_direction(p):
    """direction : TOP
    | BOTTOM
    | LEFT
    | RIGHT
    | TIMESHIFT"""
    p[0] = p[1]


def p_function_decl(p):
    """function_decl : FUNCTION IDENTIFIER LPAREN params RPAREN LBRACE statement_list RBRACE
    | FUNCTION IDENTIFIER LPAREN RPAREN LBRACE statement_list RBRACE"""
    if len(p) == 9:
        p[0] = FunctionDecl(p[2], p[4], p[7])
    else:
        p[0] = FunctionDecl(p[2], [], p[6])


def p_function_args_expr(p):
    """function_args : expr
    | function_call"""
    p[0] = p[1]


def p_function_args_list(p):
    """function_args_list : function_args
    | function_args COMMA function_args_list"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_function_call(p):
    """function_call : IDENTIFIER LPAREN function_args_list RPAREN
    | IDENTIFIER LPAREN RPAREN"""
    if len(p) == 5:
        p[0] = FunctionCall(p[1], p[3])
    else:
        p[0] = FunctionCall(p[1], [])


def p_function_call_stmt(p):
    """function_call_stmt : function_call SEMI"""
    p[0] = p[1]


def p_params(p):
    """params : IDENTIFIER
    | IDENTIFIER COMMA params"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_array_decl1(p):
    """array_decl : ARRAY_TYPE INTEGER_TYPE OF IDENTIFIER expr SEMI
    | ARRAY_TYPE INTEGER_TYPE OF IDENTIFIER SEMI"""
    if len(p) == 7:
        p[0] = ArrayDecl(p[4], p[5])
    else:
        p[0] = ArrayDecl(p[4], Num(10))


def p_pointer_decl(p):
    """pointer_decl : POINTER_TYPE INTEGER_TYPE IDENTIFIER ASSIGN expr SEMI
    | POINTER_TYPE IDENTIFIER SEMI"""
    if len(p) == 7:
        p[0] = PointerDecl(p[1], p[3], p[5])
    else:
        p[0] = PointerDecl(p[1], p[2])


def p_expr_binop(p: yacc.YaccProduction):
    """expr : expr PLUS expr
    | expr MINUS expr
    | expr MUL expr
    | expr DIV expr
    | expr EQ expr
    | expr NE expr
    | expr LT expr
    | expr GT expr
    | expr LE expr
    | expr GE expr"""
    p[0] = BinOp(p[1], p.slice[2], p[3])


def p_expr_group(p):
    """expr : LPAREN expr RPAREN"""
    p[0] = p[2]


def p_expr_num(p):
    """expr : NUMBER"""
    p[0] = Num(p[1])


def p_expr_uminus(p):
    "expr : MINUS expr %prec UMINUS"
    t = LexToken()
    t.type = "MUL"
    t.value = "*"
    p[0] = BinOp(Num(-1), t, p[2])


def p_expr_umul(p):
    "expr : MUL expr %prec UMUL"
    p[0] = Unarop(p[2])


def p_expr_questionmark(p):
    """expr : QUESTION_MARK IDENTIFIER"""
    p[0] = LenOf(Var(p[2]))


def p_address_of(p):
    """address_of : AMPERSAND IDENTIFIER"""
    p[0] = AddressOf(p[2])


def p_expr_str(p):
    """expr : STRING"""
    p[0] = Str(p[1])


def p_expr_var(p):
    """expr : IDENTIFIER
    | function_call
    | address_of"""
    if isinstance(p[1], (FunctionCall, AddressOf)):
        p[0] = p[1]
    else:
        p[0] = Var(p[1])


def p_error(p):
    raise Exception(f"Syntax error at '{p.value if p else 'EOF'}'")


def get_parser() -> yacc.LRParser:
    return yacc.yacc()
