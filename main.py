class Box:
    box = []
    pass

    def write_on_file(self):
        raise NotImplementedError("Method not implemented")


class ErrorBox(Box):

    def __init__(self, file_name='lexical_errors', extension='txt'):
        self.file_name = file_name
        self.extension = extension

    def generate_error(self, description):
        pass

    def write_on_file(self):
        pass


class SymbolBox(Box):

    def write_on_file(self):
        pass


class TokenBox(Box):

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
