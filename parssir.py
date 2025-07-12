import dataclasses
import enum
import re

OPERATORS = {
    "+", "-", "*", "/", "%", "**", "//", "and", "or", "not", "==", "!=", "<", ">", "<=", ">=", "(", ")"
}

class TokenType(enum.Enum):
    ATOM = enum.auto()
    OP = enum.auto()     # Operators
    EOF = enum.auto()    # End of file


@dataclasses.dataclass
class Token:
    type: TokenType
    value: str

    def __repr__(self):
        return f"{self.type}: {self.value}"


class Lexer:
    def __init__(self, expression: str = ''):
        self.tokens = []

        self.lexicalize(expression)

    def _is_atom(self, token: str) -> bool:
        """
        Tell whether a string is an atom token
        """
        return bool(re.fullmatch(r'\d+|[a-zA-Z_][a-zA-Z0-9_]*', token)) and token not in OPERATORS

    def _is_operator(self, token: str) -> bool:
        """
        Tell whether a string is an operator token
        """
        return token in OPERATORS

    def display_tokens(self) -> None:
        """
        Print the current tokens by reversing the token list again.
        """
        print(list(reversed(self.tokens)))

    def lexicalize(self, expression: str) -> list:
        """
        Lexicalize input into a list of tokens.
        """
        tokens = []
        for lex in re.findall(r'\d+|[a-zA-Z_]+|[+*/()-,]', expression):
            if self._is_atom(lex):
                tokens.append(Token(TokenType.ATOM, lex))
            elif self._is_operator(lex):
                tokens.append(Token(TokenType.OP, lex))
            else:
                tokens.append(Token(TokenType.EOF, lex))

        tokens.append(Token(TokenType.EOF, 'EOF'))
        self.tokens = list(reversed(tokens)) # reversing for easier popping in next()

    def next(self) -> Token:
        """
        Return the next token, and omit it in self.tokens
        """
        return self.tokens.pop()

    def peek(self) -> Token:
        """
        Peek or view the next token without popping
        """
        return self.tokens[-1]

class Expression:

    class Atom:
        def __init__(self, value: TokenType.ATOM):
            self.value = value
        def __repr__(self):
            return f"Atom({self.value})"

    class Operation:
        def __init__(self, op: TokenType.OP, operands: list):
            self.op = op
            self.operands = operands
        def __repr__(self):
            # return f"Op({self.operands[0]} {self.op} {self.operands[1]})"
            return f"{self.op} [1. {self.operands[0]}; 2. {self.operands[1]}]"

class Parser:
    def __init__(self, expression):
        self.lexer = Lexer(expression)
        self.lexer.display_tokens()

    def infix_binding_power(self, op: Token):
        table = {
            '+': (10, 11),
            '-': (10, 11),
            '*': (20, 21),
            '/': (20, 21),
        }
        return table[op.value]

    def parse_expression(self, min_bp=0):
        lhs = None
        token = self.lexer.next()

        match token.type:
            case TokenType.ATOM:
                lhs = Expression.Atom(token)
            case TokenType.OP:
                raise SyntaxError("Operation cannot be the first symbol in an expression")
            case TokenType.EOF:
                return


        while True:
            next_token = self.lexer.peek()
            if next_token.type == TokenType.EOF:
                break

            op = None
            match next_token.type:
                case TokenType.ATOM:
                    raise SyntaxError("Expect an operation, not an atom")
                case TokenType.OP:
                    pass
                case TokenType.EOF:
                    break

            op = next_token
            l_bp, r_bp = self.infix_binding_power(op)
            if l_bp < min_bp:
                break

            self.lexer.next()  # consume the operator
            rhs = self.parse_expression(r_bp)
            lhs = Expression.Operation(op, [lhs, rhs])    

        return lhs


if __name__ == '__main__':
    # print(lexer.lexicalize("13 *13 + a * b"))
    # print(lexer.lexicalize("1 + 2 * (3 - 4)"))

    parser = Parser("1 + 2 * 3")
    print(parser.parse_expression())

