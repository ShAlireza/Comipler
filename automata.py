from statics import ALPHABETS, DIGITS, PUNCTUATIONS, WHITESPACES, COMMENTS

from .exceptions import RegexNotMatchError


class Regex:
    pass


class NumRegex(Regex):
    pass


class IdKeyWordRegex(Regex):
    pass


class SymbolRegex(Regex):
    pass


class CommentRegex(Regex):
    pass


class WhiteSpaceRegex(Regex):
    pass


class DFA:

    def __init__(self):
        self.number = NumRegex()
        self.identifier = IdKeyWordRegex()
        self.symbol = SymbolRegex()
        self.comment = CommentRegex()
        self.white_space = WhiteSpaceRegex()

        self.current_regex = self.identifier

    def run(self, char):
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
