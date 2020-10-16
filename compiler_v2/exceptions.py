class CompileError(Exception):
    pass


class BufferSizeExceeded(CompileError):

    def __init__(self, max_size=4096, message='buffer maximum size exceeded,'
                                              ' max size is {}'):
        self.max_size = max_size
        self.message = message.format(self.max_size)
        super().__init__(self.message)


class WrongSyntaxError(CompileError):

    def __init__(self, line_number=0, word='',
                 message=''):
        self.line_number = line_number
        self.word = word
        default_message = 'wrong syntax in line {}, word {}'
        self.message = (default_message.format(line_number, word)
                        if not message else message)
        super().__init__(self.message)
