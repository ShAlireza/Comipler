class CompileError(Exception):
    pass


class BufferSizeExceeded(CompileError):

    def __init__(self, max_size=4096, message='buffer maximum size exceeded,'
                                              ' max size is {}'):
        self.max_size = max_size
        self.message = message.format(self.max_size)
        super().__init__(self.message)


class RegexNotMatchError(CompileError):
    def __init__(self, message='regex match failed'):
        self.message = message
        super().__init__(self.message)


class WrongSyntaxError(CompileError):

    def __init__(self, line_number, message='wrong syntax in line {}'):
        self.line_number = line_number
        self.message = message.format(line_number)
        super().__init__(self.message)


class FirstOfFileError(CompileError):
    def __init__(self, line_number, message='not able to reach beginning of file in line {}'):
        self.line_number = line_number
        self.message = message.format(line_number)
        super().__init__(self.message)

