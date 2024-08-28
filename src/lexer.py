import ply.lex as lex

__all__ = ["tokens", "get_lexer"]


TYPES = {
    "pointer": "POINTER_TYPE",
    "mutable": "MUTABLE",
    "array": "ARRAY_TYPE",
    "integer": "INTEGER_TYPE",
    "string": "STRING_TYPE",
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
    "print": "PRINT",
    "instead": "INSTEAD",
}
tokens = [
    "NUMBER",
    "STRING",
    "IDENTIFIER",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "EQ",
    "NE",
    "LT",
    "GT",
    "LE",
    "GE",
    "LPAREN",
    "RPAREN",
    "LSQUARE",
    "RSQUARE",
    "LBRACE",
    "RBRACE",
    "SEMI",
    "COMMA",
    "ASSIGN",
    "AMPERSAND",
    "QUESTION_MARK",
    "EMPTY_ARRAY",
] + list(TYPES.values())

t_PLUS = r"\+"
t_MINUS = r"-"
t_MUL = r"\*"
t_DIV = r"/"
t_EQ = r"="
t_NE = r"!="
t_LT = r"<"
t_GT = r">"
t_LE = r"<="
t_GE = r">="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LSQUARE = r"\["
t_RSQUARE = r"\]"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_SEMI = r";"
t_COMMA = r","
t_ASSIGN = r":="
t_AMPERSAND = r"&"
t_QUESTION_MARK = r"\?"
t_EMPTY_ARRAY = r"\[\]"


def t_NUMBER(t):
    r"\d+(\.\d*)?"
    t.value = int(t.value) if "." not in t.value else float(t.value)
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remove the quotes
    return t


def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = TYPES.get(t.value, "IDENTIFIER")
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise Exception(f"Illegal character '{t.value[0]}'")


# Игнорируем пробелы
t_ignore = " \t"


def get_lexer() -> lex.Lexer:
    return lex.lex()
