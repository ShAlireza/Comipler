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


class function_table:
    def __init__(self):
        self.funcs = {}
        self.params = {}

    def func_declare(self, name, address, return_type):
        self.funcs[name] = {'address': address, 'type': return_type,
                            'params': [], 'params_type': [], 'params_address': [], 'params_array': []}

    def add_param(self, func_name, param_name, param_type, param_address, is_array):
        print(self.funcs)
        self.funcs[func_name]['params'].append(param_name)
        self.funcs[func_name]['params_type'].append(param_type)
        self.funcs[func_name]['params_address'].append(param_address)
        self.funcs[func_name]['params_array'].append(is_array)
        print(self.funcs)

    def get_function(self, name):
        return self.funcs.get(name)

    def get_parameter(self, func_name, param_name):
        return self.params.get(func_name+'_'+param_name)
