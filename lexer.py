from .exceptions import (BufferSizeExceeded, RegexNotMatchError,
                         WrongSyntaxError)
from .automata import DFA


class Token:

    def __init__(self, token_type, token_char, line_found):
        self.token_type = token_type
        self.token_char = token_char
        self.line_found = line_found


class Table:

    def log(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def write_on_file(self):
        raise NotImplementedError("Method not implemented")


class ErrorTable(Table):
    TEMPLATE = 'Error in line {line_number}: {msg}'

    def __init__(self, file_name='lexical_errors', extension='txt'):
        self.file_name = file_name
        self.extension = extension
        self.id = 0
        self.errors = []

    def log(self, exception, line_number):
        message = self.TEMPLATE.format(line_number=line_number,
                                       msg=exception.message)
        self.errors.append(message)

    def write_on_file(self):
        pass


class SymbolTable(Table):

    def __init__(self):
        self.__identifiers = {}
        self.id = 0
        self.__init()

    def log(self):
        pass

    def write_on_file(self):
        pass

    def __contains__(self, item):
        return item in self.__identifiers.values()

    def install(self, item):
        if item not in self:
            self.__identifiers[self.id] = item
            self.id += 1
        return True

    def __init(self):
        from statics import RESERVED_WORDS

        for word in RESERVED_WORDS:
            self.install(word)


class TokenTable(Table):

    def log(self):
        pass

    def write_on_file(self):
        pass


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

    def __read_char(self):
        if len(self.current_string) >= self.max_size:
            raise BufferSizeExceeded
        self.current_char = self.file.read(1)
        self.current_string += self.current_string
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

    def get_next_token(self):
        try:
            self.__get_next_token()
        except RegexNotMatchError as e:
            self.error_table.log(e, self.line_number)

    def __get_next_token(self, ):
        while True:
            try:
                char = self.buffer()
                self.dfa.run(char=char, )
            except RegexNotMatchError as e:
                raise WrongSyntaxError(line_number=self.line_number)
