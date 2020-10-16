DIGITS = '0123456789'
ALPHABETS = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHANUMERICS = ALPHABETS + DIGITS
WHITESPACES = ' \t\n\r\v\f'
PUNCTUATIONS = ';:,[](){}+-*=<\\'
COMMENTS = '/'
LANGUAGE = DIGITS + ALPHABETS + PUNCTUATIONS + COMMENTS + WHITESPACES

RESERVED_WORDS = ('if', 'else', 'void', 'int', 'while', 'break', 'switch',
                  'default', 'case', 'return')

NUM = 'NUM'
ID = 'ID'
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
COMMENT = 'COMMENT'
WHITESPACE = 'WHITESPACE'

EOF = ''
END = 'EOF'
