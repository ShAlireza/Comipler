import string

DIGITS = string.digits
ALPHABETS = string.ascii_letters
WHITESPACES = string.whitespace
PUNCTUATIONS = ';:,[](){}+-*=<\\'
COMMENTS = '/'
LANGUAGE = DIGITS + ALPHABETS + PUNCTUATIONS + COMMENTS

RESERVED_WORDS = ('if', 'else', 'void', 'int', 'while', 'break', 'switch',
                  'default', 'case', 'return')
