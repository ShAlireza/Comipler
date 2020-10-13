from .exceptions import (BufferSizeExceeded, RegexNotMatchError,
                         WrongSyntaxError, FirstOfFileError)
from statics import ALPHABETS, DIGITS, PUNCTUATIONS, WHITESPACES, COMMENTS, LANGUAGE, RESERVED_WORDS, NUM, ID_KEYWORD, \
    SYMBOL, COMMENT


class Scanner:
    def __init__(self, file_path):
        self.file_path = file_path
        try:
            self.file = open(file_path, 'r')
        except FileNotFoundError as e:
            raise e

        self.dfa = CompilerDFA()
        self.line_number = 1
        self.current_char = ''
        self.current_string = ''
        self.error_table = ErrorTable()
        self.symbol_table = SymbolTable()
        self.token_table = TokenTable()

    def get_next_token(self):
        try:
            self.read_char()
            token_found, token_type = self.dfa(current_char=self.current_char, current_string=self.current_string,
                                               look_ahead_char=self.look_ahead_char())
            if token_found:
                if token_type == WHITESPACES:
                    if self.current_string == '\n':
                        self.line_number += 1
                    return str(token_type, self.current_string)
                elif token_type == NUM:
                    return str(token_type), self.current_string
                elif token_type == COMMENT:
                    if self.current_char == '\n':
                        self.line_number += 1
                    return str(token_type), self.current_string
                elif token_type == SYMBOL:
                    return str(token_type), self.current_string
                elif ID_KEYWORD == token_type:
                    if self.current_string in RESERVED_WORDS:
                        return 'KEYWORD', self.current_string
                    else:
                        return 'ID', self.current_string
                elif token_type == COMMENT:
                    return str(COMMENT), self.current_string
                self.clear()

            return self.get_next_token()
        except RegexNotMatchError as e:
            raise WrongSyntaxError(line_number=self.line_number)

    def look_ahead_char(self):
        c = self.file.read(1)
        self.seek_back()
        return c

    def read_char(self):
        self.current_char = self.file.read(1)
        self.current_string += self.current_char
        return

    def seek_back(self):
        if self.file.tell() > 0:
            self.file.seek(self.file.tell() - 1)
        else:
            raise FirstOfFileError

    def clear(self):
        self.current_char = ''
        self.current_string = ''


class CompilerDFA:
    def __init__(self):
        self.states = {0: 'start', 1: 'one_letter', 2: 'id_keyword_found', 3: 'one_digit', 4: 'digit_found',
                       5: 'symbols_except_=_found', 6: '=', 7: '==_found', 8: '*', 9: '*_as_symbol_found',
                       'a': '/', 'b': '//', 'c': 'comment_found', 'd': '/*', 'e': '/*_comment', 'f': 'white_space_found'
                       }
        self.current_state = self.states[0]

    def __call__(self, current_char, current_string, look_ahead_char, is_first_char=False, *args, **kwargs):
        if self.current_state == self.states[0]:
            if current_char in ALPHABETS:
                self.current_state = self.states[1]
                if look_ahead_char not in DIGITS or look_ahead_char not in ALPHABETS:
                    if look_ahead_char in LANGUAGE:
                        self.current_state = self.states[0]
                        return True, ID_KEYWORD
                    else:
                        pass  # todo
            if current_char in DIGITS:
                self.current_state = self.states[3]
                if look_ahead_char not in DIGITS:
                    if look_ahead_char in LANGUAGE:
                        self.current_state = self.states[0]
                        return True, NUM
                    else:
                        pass  # todo
            if current_char in ':;,[](){}+-<':
                self.reset_dfa()
                return True, SYMBOL
            if current_char in '=':
                self.current_state = self.states[6]
                if look_ahead_char != '=' and look_ahead_char in LANGUAGE:
                    return True, SYMBOL
                else:
                    pass  # todo
            if current_char in '*':
                self.current_state = self.states[8]
                if look_ahead_char != '/' and look_ahead_char in LANGUAGE:
                    return True, SYMBOL
                else:
                    pass
                    # todo
            if current_char in '/':
                self.current_state = self.states['a']
            if current_char in WHITESPACES:
                self.current_state = self.states['f']
                self.reset_dfa()
                return True, WHITESPACES
            # todo to write invalid character
        if self.current_state == self.states[1]:
            if current_char in LANGUAGE:
                if current_char in DIGITS or current_char in ALPHABETS:
                    self.current_state = self.states[1]
                    if look_ahead_char not in DIGITS or look_ahead_char not in ALPHABETS:
                        if look_ahead_char in LANGUAGE:
                            self.current_state = self.states[0]
                            return True, ID_KEYWORD
                        else:
                            pass  # todo
                else:
                    self.current_state = self.states[2]
                return False, None
            else:
                pass  # todo
        if self.current_state == self.states[3]:
            if current_char in DIGITS:
                self.current_state = self.states[3]
            if look_ahead_char not in DIGITS and look_ahead_char in LANGUAGE:
                self.current_state = self.states[0]
                return True, NUM
            else:
                pass  # todo
            return False, None
        if self.current_state == self.states[6]:
            if current_char == '=':
                return True, SYMBOL
            else:
                pass  # doubt \todo
        if self.current_state == self.states['a']:
            if current_char == '/':
                self.current_state = self.states['b']
                if look_ahead_char == '\n':
                    self.reset_dfa()
                    return True, COMMENT
            elif current_char == '*':
                self.current_state = self.states['d']
                return False, None
            else:
                pass
        if self.current_state == self.states['b']:
            if look_ahead_char == '\n':
                self.reset_dfa()
                return True, COMMENT  # todo end of file did not count!
            else:
                return False, None
        if self.current_state == self.states['d']:
            if current_char == '*':
                self.current_state = self.states['e']
                return False, None
        if self.current_state == self.states['e']:
            if current_char == '/':
                self.reset_dfa()
                return True, COMMENT
            elif current_char != '*':
                self.current_state = self.states['d']
                return False, None

    def reset_dfa(self):
        self.current_state = self.states[0]


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
