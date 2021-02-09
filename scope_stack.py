class ScopeStack:

    def __init__(self):
        self._stack = []
        self._stack.append(-1)

    def pop(self, count=1):
        if len(self._stack) < count:
            raise ValueError('Pop size bigger than stack size')

        if self._stack[-1] == -1:
            return -1

        for i in range(count):
            self._stack.pop()

    def push(self, value):
        self._stack.append(value)

    def top(self, count=1):
        return self._stack[-count]
