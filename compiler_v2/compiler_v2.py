from statics import *
from exceptions import *


class Token:

    def __init__(self, token_type, token_string):
        self.token_type = token_type
        self.token_string = token_string

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'({self.token_type}, {self.token_string})'


class Table:

    def log(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def write_on_file(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")


class ErrorTable(Table):
    TEMPLATE = '({word}, {msg})'

    def __init__(self, file_name='lexical_errors', extension='txt'):
        self.file_name = file_name
        self.extension = extension
        self.id = 0
        self.table = {}

    def log(self, exception, line_number):
        message = self.TEMPLATE.format(word=exception.word,
                                       msg=exception.message)
        try:
            self.table[line_number].append(message)
        except KeyError as e:
            self.table[line_number] = []
            self.table[line_number].append(message)

    def write_on_file(self):
        with open(f'{self.file_name}.{self.extension}', 'w') as file:
            for k, values in self.table.items():
                file.write(f'line {k}: ')
                for value in values:
                    file.write(f'{value} ')
                file.write('\n')


class SymbolTable(Table):
    TEMPLATE = '{word}'

    def __init__(self, file_name='symbol_table', extension='txt'):
        self.file_name = file_name
        self.extension = extension
        self.__identifiers = {}
        self.table = {}
        self.id = 1
        self.__init()

    def log(self, item):
        if item not in self.__identifiers.values():
            message = self.TEMPLATE.format(word=item)
            self.table[self.id] = message
            self.__install(item)

    def write_on_file(self):
        with open(f'{self.file_name}.{self.extension}', 'w') as file:
            for k, value in self.table.items():
                file.write(f'{k}: {value}\n')

    def __install(self, item):
        self.__identifiers[self.id] = item
        self.id += 1
        return True

    def __init(self):
        from statics import RESERVED_WORDS

        for word in RESERVED_WORDS:
            self.log(word)

    @staticmethod
    def is_keyword(token):
        return token in RESERVED_WORDS


class TokenTable(Table):
    TEMPLATE = '({token_type}, {token_string})'

    def __init__(self, file_name='token_table', extension='txt'):
        self.file_name = file_name
        self.extension = extension
        self.table = {}

    def log(self, token: Token, line_number):
        message = self.TEMPLATE.format(
            token_type=token.token_type,
            token_string=token.token_string.encode('unicode_escape')
        )
        try:
            self.table[line_number].append(message)
        except KeyError as e:
            self.table[line_number] = []
            self.table[line_number].append(message)

    def write_on_file(self):
        with open(f'{self.file_name}.{self.extension}', 'w') as file:
            for k, values in self.table.items():
                file.write(f'{k}: ')
                for value in values:
                    file.write(f'{value} ')
                file.write('\n')


class DFA:

    def __init__(self):
        self.start_char = ''
        self.comment_type = 0

    def __call__(self, current_char, current_string,
                 is_first_char=False, *args, **kwargs):
        if is_first_char:
            self.start_char = current_char
        answer = self.__find(
            current_char=current_char,
            current_string=current_string
        )
        return answer

    def __find(self, current_char, current_string):
        if self.start_char not in LANGUAGE:
            raise WrongSyntaxError
        if self.start_char == EOF:
            return None, False

        if self.start_char in ALPHABETS:
            return self.__id_keyword_regex(
                current_char=current_char,
                current_string=current_string
            )
        if self.start_char in DIGITS:
            return self.__num_regex(
                current_char=current_char,
                current_string=current_string
            )
        if self.start_char in PUNCTUATIONS:
            return self.__symbol_regex(
                current_char=current_char,
                current_string=current_string
            )
        if self.start_char in WHITESPACES:
            return self.__white_space_regex(
                current_char=current_char,
                current_string=current_string
            )
        if self.start_char in COMMENTS:
            return self.__comment_regex(
                current_char=current_char,
                current_string=current_string
            )

    def __num_regex(self, current_char, current_string):
        if current_char in DIGITS:
            return None, False
        if current_char not in ALPHABETS and current_string not in LANGUAGE:
            return Token(token_type=NUM,
                         token_string=current_string[:-1]), True
        raise WrongSyntaxError(word=current_string,
                               message='Invalid number')

    def __id_keyword_regex(self, current_char, current_string):
        if current_char in ALPHANUMERICS:
            return None, False
        if current_char in LANGUAGE:
            if SymbolTable.is_keyword(current_string[:-1]):
                return Token(token_type=KEYWORD,
                             token_string=current_string[:-1]), True
            return Token(token_type=ID,
                         token_string=current_string[:-1]), True
        raise WrongSyntaxError(word=current_string,
                               message='Invalid input')

    def __symbol_regex(self, current_char, current_string):
        if current_char != '=' and current_char != '*':
            return Token(token_type=SYMBOL,
                         token_string=current_string), False
        if current_char == '/' and self.start_char == '*':
            raise WrongSyntaxError(word=current_string,
                                   message='Unmatched comment')

        if current_string == '*':
            return None, False

        if self.start_char == '=' and current_string == '=':
            return None, False

        if current_string == '==':
            return Token(token_type=SYMBOL,
                         token_string=current_string), False

        if current_char != '/' and len(current_string) == 2 and \
                current_string != '*/':
            return Token(token_type=SYMBOL,
                         token_string='*'), True

        if self.start_char == '=' and current_string != '=' \
                and current_char in LANGUAGE:
            return Token(token_type=SYMBOL,
                         token_string='='), True

        raise WrongSyntaxError(word=current_string,
                               message='Invalid input')

    def __comment_regex(self, current_char, current_string):
        if self.start_char == '/' and current_string == '//':
            self.comment_type = 1
        if self.start_char == '/' and current_string == '/*':
            self.comment_type = 2
        if self.start_char == '/' and len(current_string) == 2 \
                and current_string not in ['//', '/*']:
            self.comment_type = 0
            raise WrongSyntaxError(word=current_string,
                                   message='Invalid input')

        if self.comment_type == 1 and current_char in ['\n', EOF]:
            self.comment_type = 0
            return Token(token_type=COMMENT,
                         token_string=current_string[:-1]), True
        if self.comment_type == 2 and current_char == '/' and \
                current_string[-2:] == '*/':
            self.comment_type = 0
            return Token(token_type=COMMENT,
                         token_string=current_string), False
        if self.comment_type == 2 and current_char == EOF:
            self.comment_type = 0
            raise WrongSyntaxError(word=current_string[:11] + '...',
                                   message='Unclosed comment')
        return None, False

    def __white_space_regex(self, current_char, current_string):
        return Token(token_type=WHITESPACE,
                     token_string=current_string), False


class Buffer:

    def __init__(self, file, max_size=4096):
        self.file = file
        self.max_size = max_size
        self.current_char = ''
        self.current_string = ''
        pass

    def __call__(self, *args, **kwargs):
        return self.__read_char()

    def clear(self):
        self.current_char = ''
        self.current_string = ''

    @property
    def is_first_char(self):
        return len(self.current_string) == 1

    def __read_char(self):
        if len(self.current_string) >= self.max_size:
            raise BufferSizeExceeded
        self.current_char = self.file.read(1)
        self.current_string += self.current_char
        return self.current_char

    def seek_prev(self):
        self.file.seek(self.file.tell() - 1)


class Scanner:

    def __init__(self, file_path):
        self.file_path = file_path
        try:
            self.file = open(file_path, 'r')
        except FileNotFoundError as e:
            raise e
        self.buffer = Buffer(file=self.file, max_size=4096)
        self.dfa = DFA()
        self.line_number = 1

        self.error_table = ErrorTable()
        self.symbol_table = SymbolTable()
        self.token_table = TokenTable()

        self.finished = False

    def simulate(self):
        while True:
            token = self.get_next_token(simulation=True)
            if self.finished:
                self.__finish()
                break

    def get_next_token(self, simulation=False):
        try:
            if self.finished:
                return None
            token, new_line = self.__get_next_token()
            if token.token_type == ID:
                self.symbol_table.log(token.token_string)
            if token.token_type not in [WHITESPACE, COMMENT]:
                self.token_table.log(token=token, line_number=self.line_number)
            self.buffer.clear()
            if token.token_type == END:
                self.finished = True
            if new_line:
                self.line_number += 1
            return token
        except WrongSyntaxError as e:
            self.buffer.clear()
            self.error_table.log(e, self.line_number)

    def __get_next_token(self):
        while True:
            try:
                new_line = False
                char = self.buffer()
                token, look_ahead = self.dfa(
                    current_char=char,
                    current_string=self.buffer.current_string,
                    is_first_char=self.buffer.is_first_char
                )
                if char == EOF and not token:
                    return Token(token_type=END, token_string=char), new_line

                if char == '\n' and not look_ahead:
                    new_line = True
                if look_ahead:
                    self.buffer.seek_prev()
                if token:
                    return token, new_line
            except WrongSyntaxError as e:
                raise WrongSyntaxError(
                    line_number=self.line_number,
                    word=e.word,
                    message=e.message
                )

    def __finish(self):
        self.token_table.write_on_file()
        self.error_table.write_on_file()
        self.symbol_table.write_on_file()


scanner = Scanner('../test.txt')
scanner.simulate()
