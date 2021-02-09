from scanner import get_temp, line_num


class function_table:
    def __init__(self):
        self.funcs = {}
        self.params = {}

    def func_declare(self, name, address, return_type):
        ln = line_num
        self.funcs[address] = {'name': name, 'address': address,
                               'return_type': return_type, 'symbol_table': {},
                               'scope': 0, 'line_num': ln, 'params': [],
                               'params_type': [], 'params_address': [], 'params_array': [], 'return_addresses': []}

    def add_param(self, func, param_name, param_type, param_address, is_array):
        self.funcs[func]['params'].append(param_name)
        self.funcs[func]['params_type'].append(param_type)
        self.funcs[func]['params_address'].append(param_address)
        self.funcs[func]['params_array'].append(is_array)

    def get_function_name(self, address):
        return self.funcs[address]['name']

    def get_function_address(self, name):
        for ad in self.funcs:
            if name == self.get_function_name(ad):
                return ad

    def get_parameter(self, func_name, param_name):
        return self.params.get(func_name + '_' + param_name)
