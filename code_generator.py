from scanner import findaddr, get_temp, increase_data_pointer
from semantic_stack import SemanticStack


class CodeGenerator:

    def __init__(self, semantic_stack: SemanticStack):
        self.semantic_stack = semantic_stack
        self.pb = ['0'] * 1000
        self.index = 0

    def __call__(self, action, **kwargs):
        return getattr(self, '_' + action)(**kwargs)

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
        self.pb[self.semantic_stack.top()] = (f'(JP, '
                                              f'{self.index}, '
                                              f',)')
        self.semantic_stack.pop()

    def _assign(self, **kwargs):
        self.pb[self.index] = (f'(ASSIGN, '
                               f'{self.semantic_stack.top()}, '
                               f'{self.semantic_stack.top(2)},)')
        self.semantic_stack.pop()
        self.index += 1

    def _compare(self, **kwargs):
        temp = get_temp()
        operator = 'EQ'
        if self.semantic_stack.top(2) == 1:
            operator = 'LT'

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
        self.index += 1
        self.semantic_stack.pop(3)
        self.semantic_stack.push(temp)

    def _mult(self, **kwargs):
        temp = get_temp()
        self.pb[self.index] = (f'(MULT, '
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
        self.semantic_stack.push(f'#{_input}')

    def _jpf_save(self, **kwargs):
        self.pb[self.semantic_stack.top()] = (f'(JPF, '
                                              f'{self.semantic_stack.top(2)}, '
                                              f'{self.index + 1},)')
        self.semantic_stack.pop(2)
        self.semantic_stack.push(self.index)
        self.index += 1

    def _while(self, **kwargs):
        self.pb[self.semantic_stack.top()] = (f'(JPF, '
                                              f'{self.semantic_stack.top(2)}, '
                                              f'{self.index + 1},)')
        self.pb[self.index] = (f'(JP, '
                               f'{self.semantic_stack.top(3)}, ,)')
        self.index += 1
        self.semantic_stack.pop(3)

    def _set_array_address(self, **kwargs):
        temp = get_temp()
        offset, base = self.semantic_stack.top(), self.semantic_stack.top(2)

        self.pb[self.index] = (f'(ADD, '
                               f'#{base}, '
                               f'{offset}, '
                               f'{temp})')

        self.index += 1
        self.semantic_stack.pop(2)
        self.semantic_stack.push(f'@{temp}')

    def _output(self, **kwargs):
        self.pb[self.index] = (f'(PRINT, '
                               f'{self.semantic_stack.top()}, ,)')
        self.semantic_stack.pop()
        self.index += 1

    def _init_var(self, **kwargs):
        self.pb[self.index] = (f'(ASSIGN, '
                               f'#0, '
                               f'{self.semantic_stack.top()},)')
        self.index += 1
        self.semantic_stack.pop(2)

    def _init_array(self, **kwargs):
        size = self.semantic_stack.top()
        if '#' in size:
            size = int(size[1:])
        for i in range(int(size)):
            self.pb[self.index] = (f'(ASSIGN, '
                                   f'#0, '
                                   f'{self.semantic_stack.top(2) + i * 4})')
            self.index += 1
        increase_data_pointer(size - 1)
