class CodeGenerator:

    def __init__(self, semantic_stack):
        self._routines = dict()
        self.semantic_stack = semantic_stack

    def _pop(self, count=1):
        self.semantic_stack.pop(count)

    def _push(self, value):
        self.semantic_stack.push(value)
