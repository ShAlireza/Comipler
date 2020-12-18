class SemanticStack:
    INF = 100000

    def __init__(self, max_size=0):
        self.max_size = max_size if max_size else self.INF
        self._stack = []

    def pop(self, count=1):
        if len(self._stack) < count:
            raise ValueError('Pop size bigger than stack size')

        for i in range(count):
            self._stack.pop()

    def push(self, value):
        if len(self._stack) + 1 > self.max_size:
            raise ValueError('Stack is full')
        self._stack.append(value)

    def top(self, count=1):
        return self._stack[-count]
