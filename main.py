from src.interpreter import test_interpreter
from src.lexer import get_lexer


def get_prog_from_file(filename: str = "test/parser.test") -> str:

    with open(filename, "r") as inp:
        s = inp.read()
    return s


def test_lexer(s: str):

    lexer = get_lexer()
    lexer.input(s)
    # parser = get_parser()
    print("started")
    while token := lexer.token():
        print(token)
        # result = parser(s)
    print("done!")


def main():
    s = get_prog_from_file()
    test_interpreter(s)


if __name__ == "__main__":
    main()
