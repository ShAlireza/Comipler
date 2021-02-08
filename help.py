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

    def add_function(self, name, address, params, return_type, params_type, params_addresses):
        self.funcs[name] = {'address': address, 'params': [], 'type': return_type}
        for i in range(len(params)):
            self.funcs[name]['params'].append(name + '_' + params[i])
            self.params[name + '_' + params[i]] = {'address': params_addresses[i], 'type': params_type[i]}

    def get_function(self, name):
        return self.funcs.get(name)

    def get_parameter(self, func_name, param_name):
        return self.params.get(func_name+'_'+param_name)








