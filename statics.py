import string
from enum import Enum

# class Symbols(Enum):
#     ID = 0
#     KEYWORD = 1
#     SEMICOLON = 2
#     COLON = 3
#     COMMA = 4
#     LEFT_BRACKET = 5
#     RIGHT_BRACKET = 6
#     LEFT_PARA = 7
#     RIGHT_PARA = 8
#     LEFT_CURL = 9
#     RIGHT_CURL = 10
#     PLUS = 11
#     MINUS = 12
#     MUL = 13
#     ASSIGN = 14
#     LT = 15
#     EQ = 16

DIGITS = string.digits
ALPHABETS = string.ascii_letters
WHITESPACES = string.whitespace
PUNCTUATIONS = ';:,[](){}+-*=</\\'

RESERVED_WORDS = ('if', 'else', 'void', 'int', 'while', 'break', 'switch',
                  'default', 'case', 'return')
