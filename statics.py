DIGITS = '0123456789'
ALPHABETS = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
WHITESPACES = ' \t\n\r\v\f'
PUNCTUATIONS = ';:,[](){}+-*=<\\'
COMMENTS = '/'
LANGUAGE = DIGITS + ALPHABETS + PUNCTUATIONS + COMMENTS

RESERVED_WORDS = ('if', 'else', 'void', 'int', 'while', 'break', 'switch',
                  'default', 'case', 'return')


NUM = 'NUM'
ID = 'ID'
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
COMMENT = 'COMMENT'
