INTEGER, OPERATOR, EOF = 'INTEGER', 'OPERATOR', 'EOF'
OPERATORS = ['+', '-', '*', '/']

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self) -> Token:
        text = self.text

        if self.pos >= len(text) or self.current_char is None:
            return Token(EOF, None)

        if self.current_char.isdigit():
            return Token(INTEGER, self.integer())
        
        if self.current_char in OPERATORS:
            token = Token(OPERATOR, self.current_char)
            self.advance()
            return token

        #Recurse the function until whitespace is not found
        if self.current_char.isspace():
            self.advance()
            return self.get_next_token()
            
        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text): #End of the text
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def expr(self):
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token.type == OPERATOR:
            if self.current_token.value == '+':
                self.eat(OPERATOR)
                result = result + self.term()
            elif self.current_token.value == '-':
                self.eat(OPERATOR)
                result = result - self.term()
            elif self.current_token.value == '*':
                self.eat(OPERATOR)
                result = result * self.term()
            elif self.current_token.value == '/':
                self.eat(OPERATOR)
                result = result / self.term()
        
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break

        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

main()