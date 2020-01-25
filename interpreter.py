INTEGER, OPERATOR, EOF = 'INTEGER', 'OPERATOR', 'EOF'
OPERATORS = ['+', '-']

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

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self) -> Token:
        text = self.text

        if self.pos > len(text)-1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token
        
        if current_char in OPERATORS:
            token = Token(OPERATOR, current_char)
            self.pos += 1
            return token

        #Recurse the function until whitespace not found
        if current_char == ' ':
            self.pos += 1
            return self.get_next_token()
            
        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        left, right = [], []
        self.current_token = self.get_next_token()

        #Find left integer
        while True:
            if self.current_token.type == INTEGER:
                left.append(self.current_token.value)
                self.eat(INTEGER)
            else:
                break
        
        op = self.current_token
        self.eat(OPERATOR)

        #Find right integer
        while True:
            if self.current_token.type == INTEGER:
                right.append(self.current_token.value)
                self.eat(INTEGER)
            else:
                break

        left_total_digit = len(left)
        right_total_digit = len(right)

        left_val = 0
        for idx, num in enumerate(left):
            left_val += (10 ** (left_total_digit - idx - 1)) * num

        right_val = 0
        for idx, num in enumerate(right):
            right_val += (10 ** (right_total_digit - idx - 1)) * num

        result = None
        if op.value == '+':
            result = left_val + right_val
        elif op.value == '-':
            result = left_val - right_val
        
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