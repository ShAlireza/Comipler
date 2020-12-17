from scanner import findaddr, get_temp
from semantic_stack import SemanticStack


class CodeGenerator:

    def __init__(self, semantic_stack: SemanticStack):
        self.semantic_stack = semantic_stack
        self.pb = ['0'] * 10000
        self.index = 0

    def __call__(self, action, **kwargs):
        return getattr(self, action)(**kwargs)

    def _pop(self, **kwargs):
        count = kwargs.get('count', 1)
        self.semantic_stack.pop(count)

    def _pid(self, **kwargs):
        _input = kwargs.get('_input')
        if not _input:
            raise ValueError('No input provided')
        value = findaddr(_input)
        if not value:
            raise ValueError('Input not found in symbol table')
        self.semantic_stack.push(value)

    def _save(self, **kwargs):
        self.semantic_stack.push(self.index)
        self.index += 1

    def _label(self, **kwargs):
        self.semantic_stack.push(self.index)

    def _jp(self, **kwargs):
        self.pb[self.index] = (f'(JP, '
                               f'{self.semantic_stack.top(2)}, '
                               f', )')
        self.index += 1
        self.semantic_stack.pop()

    def _assign(self, **kwargs):
        self.pb[self.index] = (f'(ASSIGN, '
                               f'{self.semantic_stack.top()}, '
                               f'{self.semantic_stack.top(2)}, )')
        self.semantic_stack.pop()
        self.index += 1

    def _compare(self, **kwargs):
        temp = get_temp()
        operator = 'EQ'
        if self.semantic_stack.top(2) == 1:
            operator = '<'

        self.pb[self.index] = (f'({operator}, '
                               f'{self.semantic_stack.top(3)}, '
                               f'{self.semantic_stack.top()}, '
                               f'{temp})')
        self.index += 1
        self.semantic_stack.pop(3)
        self.semantic_stack.push(temp)

    def _push_1(self, **kwargs):
        self.semantic_stack.push(1)

    def _push_2(self, **kwargs):
        self.semantic_stack.push(2)

    def _add(self, **kwargs):
        temp = get_temp()
        operator = 'ADD'
        if self.semantic_stack.top(2) == 2:
            operator = 'SUB'

        self.pb[self.index] = (f'({operator}, '
                               f'{self.semantic_stack.top(3)}, '
                               f'{self.semantic_stack.top()}, '
                               f'{temp})')
        self.semantic_stack.pop(3)
        self.semantic_stack.push(temp)

    def _multiply(self, **kwargs):
        temp = get_temp()
        self.pb[self.index] = (f'(MUL, '
                               f'{self.semantic_stack.top(2)}, '
                               f'{self.semantic_stack.top()}, '
                               f'{temp})')
        self.index += 1
        self.semantic_stack.pop(2)
        self.semantic_stack.push(temp)

    def _minus_sign(self, **kwargs):
        temp = get_temp()
        self.pb[self.index] = (f'(SUB, #0, '
                               f'{self.semantic_stack.top()}, '
                               f'{temp})')
        self.index += 1
        self.semantic_stack.pop()
        self.semantic_stack.push(temp)

    def _pnum(self, **kwargs):
        _input = kwargs.get('_input')
        self.semantic_stack.push(int(_input))

    def _jpf_save(self, **kwargs):
        self.pb[self.semantic_stack.top()] = (f'(JPF, '
                                              f'{self.semantic_stack.top(2)}, '
                                              f'{self.index + 1}, )')
        self.semantic_stack.pop(2)
        self.semantic_stack.push(self.index)
        self.index += 1

    def _while(self, **kwargs):
        self.pb[self.semantic_stack.top()] = (f'(JPF, '
                                              f'{self.semantic_stack.top(2)}, '
                                              f'{self.index + 1}, )')
        self.pb[self.index] = (f'(JP, '
                               f'{self.semantic_stack.top(2)}, , ')
        self.index += 1
        self.semantic_stack.pop(3)

    def _set_array_address(self, **kwargs):
        temp = get_temp()
        offset, base = self.semantic_stack.top(), self.semantic_stack.top(2)

        self.pb[self.index] = (f'(ASSIGN, '
                               f'{base + offset}, '
                               f'{temp}, )')
        self.index += 1
        self.semantic_stack.pop(2)
        self.semantic_stack.push(temp)
