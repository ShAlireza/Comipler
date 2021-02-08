class ScopeStack:
    def __init__(self):
        self._stack = []

    def pop(self, count=1):
        if len(self._stack) < count:
            raise ValueError('Pop size bigger than stack size')
        for i in range(count):
            self._stack.pop()

    def push(self, value):
        self._stack.append(value)

    def top(self, count=1):
        return self._stack[-count]


class symbol_table:
    def __init__(self):
        self.scope_stack = ScopeStack()
