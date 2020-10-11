class Token:

    def __init__(self, token_type, token_char, line_found):
        self.token_type = token_type
        self.token_char = token_char
        self.line_found = line_found


class Table:
    table = {}
    pass

    def write_on_file(self):
        raise NotImplementedError("Method not implemented")


class ErrorTable(Table):

    def __init__(self, file_name='lexical_errors', extension='txt'):
        self.file_name = file_name
        self.extension = extension

    def generate_error(self, description):
        pass

    def write_on_file(self):
        pass


class SymbolTable(Table):

    def __init__(self):
        self.__identifiers = {}
        self.id = 0
        self.__init()

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

    def write_on_file(self):
        pass


class Buffer:

    def __init__(self, file):
        pass

    def __call__(self, *args, **kwargs):
        pass


class Scanner:

    def __init__(self, file_path):
        self.file_path = file_path
        try:
            self.file = open(file_path, 'r')
        except FileNotFoundError as e:

            pass

    def get_next_token(self, ):
        pass
