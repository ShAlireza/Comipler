from statics import ALPHABETS, DIGITS, PUNCTUATIONS, WHITESPACES, COMMENTS
from statics import NUM, ID, KEYWORD, SYMBOL, COMMENT

from .exceptions import RegexNotMatchError


class Token:

    def __init__(self, token_type, token_string):
        self.token_type = token_type
        self.token_string = token_string


class Regex:

    def check(self, char, string):
        raise NotImplementedError


class NumRegex(Regex):

    def check(self, char, string):
        return Token(token_type=NUM, token_string=string)  # Return Example


class IdKeyWordRegex(Regex):

    def check(self, char, string):
        pass


class SymbolRegex(Regex):

    def check(self, char, string):
        pass


class CommentRegex(Regex):

    def check(self, char, string):
        pass


class WhiteSpaceRegex(Regex):

    def check(self, char, string):
        pass


class DFA:

    def __init__(self):
        self.number = NumRegex()
        self.identifier = IdKeyWordRegex()
        self.symbol = SymbolRegex()
        self.comment = CommentRegex()
        self.white_space = WhiteSpaceRegex()
        self.current_regex = self.identifier

    def __call__(self, current_char, current_string,
                 is_first_char=False, *args, **kwargs):
        if is_first_char:
            self.__set_identifier(
                char=current_char
            )
        else:
            self.identifier.check(
                char=current_char,
                string=current_string
            )

    def __set_identifier(self, char):
        if char in ALPHABETS:
            self.current_regex = self.identifier
        elif char in DIGITS:
            self.current_regex = self.number
        elif char in PUNCTUATIONS:
            self.current_regex = self.symbol
        elif char in WHITESPACES:
            self.current_regex = self.white_space
        elif char in COMMENTS:
            self.current_regex = self.comment
        else:
            raise RegexNotMatchError
