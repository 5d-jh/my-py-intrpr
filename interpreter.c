/*
  char -> [lexer] -> token -> [parser|interpreter] -> result
*/

#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

enum TokenTypes {_EOF, OPERATOR, INTEGER};
enum Operators {ADD, SUBTRACT, MULTIPLY, DIVIDE};

struct Token {
    enum TokenTypes type;
    int value;
};

struct Token get_next_token();

int position;
int string_len;
char current_char;
char *input_string;
struct Token current_token;

void init(char *string)
{
    position = 0;
    current_char = string[position];
    string_len = strlen(string);

    input_string = calloc(string_len, sizeof(char));
    strcpy(input_string, string);
    free(string);
}

struct Token token(enum TokenTypes token_type, int value)
{
    struct Token tk;
    tk.type = token_type;
    tk.value = value;
    return tk;
}

_Bool isoperator(char ch)
{
    char operator_syms[] = {'+', '-', '*', '/'};
    for (size_t i = 0; i < 4; i++)
    {
        if (operator_syms[i] == ch)
        {
            return 1;
        }
    }
    return 0;
}

void advance()
{
    position++;
    if (position <= string_len)
    {
        current_char = input_string[position];
    }
}

int parse_int()
{
    int result = 0;
    while (isdigit(current_char))
    {
        result *= 10;
        result += current_char - '0';
        advance();
    }
    return result;
}

struct Token get_next_token()
{
    if (position >= string_len)
    {
        return token(_EOF, 0);
    }

    if (isdigit(current_char))
    {
        return token(INTEGER, parse_int());
    }

    if (isoperator(current_char))
    {
        struct Token tk;
        switch (current_char)
        {
        case '+':
            tk = token(OPERATOR, ADD);
            break;
        case '-':
            tk = token(OPERATOR, SUBTRACT);
            break;
        case '*':
            tk = token(OPERATOR, MULTIPLY);
            break;
        case '/':
            tk = token(OPERATOR, DIVIDE);
            break;
        default:
            break;
        }
        advance();
        return tk;
    }

    advance();
    return get_next_token();
}

void eat(enum TokenTypes token_type)
{
    if (token_type == current_token.type)
    {
        current_token = get_next_token();
    }
}

int term()
{
    int val = current_token.value;
    eat(INTEGER);
    return val;
}

int parse()
{
    current_token = get_next_token();

    int result = term();
    while (current_token.type == OPERATOR)
    {
        switch (current_token.value)
        {
        case ADD:
            eat(OPERATOR);
            result = result + term();
            break;

        case SUBTRACT:
            eat(OPERATOR);
            result = result - term();
            break;

        case MULTIPLY:
            eat(OPERATOR);
            result = result * term();
            break;
        
        case DIVIDE:
            eat(OPERATOR);
            result = result / term();
            break;
        
        default:
            break;
        }
    }
    return result;
}

int main(void)
{
    while (1)
    {
        char *input = calloc(100, sizeof(char));
        printf("calc> ");
        scanf("%[^\n]%*c", input);
        init(input);
        printf("%d\n", parse());
    }
}