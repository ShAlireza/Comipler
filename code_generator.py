from scanner import findaddr, get_temp, increase_data_pointer, symbol_table, get_stack_temp
from semantic_stack import SemanticStack
from help import function_table


class CodeGenerator:

    def __init__(self, semantic_stack: SemanticStack):
        self.semantic_stack = semantic_stack
        self.pb = ['0'] * 1005
        self.index = 1
        self.function_table = function_table()
        self.inside_if = False
        self.break_bool = False
        self.func_number_of_args = -1
        self.arg_counter = -1
        self.func_names = None
        self.ra = []
        self.main_seen = False
        self.retrun_temp = get_temp()
        self.retrun_stack = []
        self.current_function_address = None

    def __call__(self, action, **kwargs):
        return getattr(self, '_' + action)(**kwargs)

    def _pop(self, **kwargs):
        count = kwargs.get('count', 1)
        self.semantic_stack.pop(count)

    def _main(self, **kwargs):
        self.pb[0] = f"(ASSIGN, #0, {self.retrun_temp}, )"
        self.semantic_stack.push(self.index)
        self.index += 1
        self._output()

    def _output(self, **kwargs):
        self.pb[self.index] = f'(PRINT, 30004, ,)'
        self.function_table.func_declare('output', 30000, 'void')
        self.function_table.add_param(30000, 'ABOLFAZL', 'int', 30004, False)
        self.function_table.funcs[30000]['start_address'] = self.index
        self.index += 1
        self.pb[self.index] = f"(JP, @{self.retrun_temp}, , )"
        self.index += 1

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

    def _case(self, **kwargs):
        result = get_temp()
        self.pb[self.index] = f"(EQ, {self.semantic_stack.top(1)}, {self.semantic_stack.top(2)}, {result})"
        self.semantic_stack.pop()
        self.index += 1
        self.semantic_stack.push(result)

    def _jp_case(self, **kwargs):
        address = self.semantic_stack.top()
        self.semantic_stack.pop()
        self.pb[address] = f"(JPF, {self.semantic_stack.top()}, {self.index}, )"
        self.semantic_stack.pop()

    def _break_temp(self, **kwargs):
        temp = get_temp()
        self.semantic_stack.push(temp)
        self._save()
        self.break_bool = True

    def _break(self, **kwargs):
        if self.break_bool:
            if self.inside_if:
                self.pb[self.index] = f"(JP, @{self.semantic_stack.top(7)}, , )"
                self.index += 1
                self.inside_if = False
            else:
                self.pb[self.index] = f"(JP, @{self.semantic_stack.top(5)}, , )"
                self.index += 1
            self.break_bool = False
        else:
            pass
            ### todo (#lineno: Semantic Error! No 'while' or 'switch' found for 'break')

    def _set_break_temp(self, **kwargs):
        self.pb[self.semantic_stack.top()] = f"(ASSIGN, #{self.index}, {self.semantic_stack.top(2)}, )"
        self.semantic_stack.pop(2)

    def _if(self, **kwargs):
        self.inside_if = True


#########################################################

    def _func_declared(self, **kwargs):
        names = None
        for q in symbol_table:
            if symbol_table[q]['address'] == self.semantic_stack.top():
                names = symbol_table[q]['token']
                break
        self.function_table.func_declare(names, self.semantic_stack.top(), 'void')
        name = self.function_table.get_function_name(self.semantic_stack.top())
        if name == 'main':
            self.pb[1] = f'(JP, #{self.index}, , )'
            self.main_seen = True
        if self.semantic_stack.top(2) == 1:
            self.function_table.func_declare(name, self.semantic_stack.top(), 'int')
        else:
            self.function_table.func_declare(name, self.semantic_stack.top(), 'void')
        self.current_function_address = self.semantic_stack.top()

    def _push_int(self, **kwargs):
        self.semantic_stack.push('int')

    def _push_void(self, **kwargs):
        if not self.main_seen:
            self.semantic_stack.push('void')

    def _param_added(self, **kwargs):
        func = self.semantic_stack.top(3)
        param_name = None
        for names in symbol_table:
            if symbol_table[names]['address'] == self.semantic_stack.top():
                param_name = names
                break
        self.function_table.add_param(func, param_name, self.semantic_stack.top(2), self.semantic_stack.top(),
                                      False)

        self.semantic_stack.pop(2)

    def _param_array_added(self, **kwargs):
        func = self.semantic_stack.top(3)
        param_name = None
        for names in symbol_table:
            if symbol_table[names]['address'] == self.semantic_stack.top():
                param_name = names
                break
        self.function_table.add_param(func, param_name, self.semantic_stack.top(2), self.semantic_stack.top(),
                                      True)
        self.semantic_stack.pop(2)

    def _void_parameter_added(self, **kwargs):
        self.semantic_stack.pop()

    def _set_func_start(self, **kwargs):
        if self.main_seen:
            return
        self.function_table.funcs[self.semantic_stack.top()]['start_address'] = self.index
        print(self.function_table.funcs[self.semantic_stack.top()])

    def _func_call_started(self, **kwargs):
        func_name = self.semantic_stack.top()
        print("FUNC CALL STARTED")
        print(self.semantic_stack._stack)
        print(func_name)
        print(self.function_table.funcs)
        self.func_number_of_args = len(self.function_table.funcs[func_name]['params'])
        self.arg_counter = 0
        self.current_function_address = func_name

    def _func_call_ended(self, **kwargs):
        self.current_function_address = self.semantic_stack.top()
        stack_temp = get_stack_temp()
        self.retrun_stack.append(stack_temp)
        self.pb[self.index] = f"(ASSIGN, #0, {self.current_function_address}, )"
        self.index += 1
        self.pb[self.index] = f"(ASSIGN, #0, {stack_temp}, )"
        self.index += 1
        self.pb[self.index] = f"(ASSIGN, {self.retrun_temp}, {stack_temp}, )"
        self.index += 1
        self.pb[self.index] = f"(ASSIGN, #{self.index + 2}, {self.retrun_temp}, )"
        self.index += 1
        self.pb[self.index] = f"(JP, #{self.function_table.funcs[self.current_function_address]['start_address']}, , )"
        self.index += 1
        self.pb[self.index] = f"(ASSIGN, {self.retrun_stack.pop()}, {self.retrun_temp},  )"
        self.index += 1

    def _push_arg(self, **kwargs):
        self.semantic_stack.push(self.function_table.funcs[self.current_function_address]['params_address'][self.arg_counter])
        self.arg_counter += 1

    def _assign_arg(self, **kwargs):
        if self.function_table.funcs[self.current_function_address]['params_array']:
            self.pb[self.index] = (f'(ASSIGN, '
                                   f'@{self.semantic_stack.top()}, '
                                   f'{self.semantic_stack.top(2)},)')
            self.semantic_stack.pop()
            self.index += 1
        else:
            self._assign()

    def _assign_to_func(self, **kwargs):
        print(self.semantic_stack._stack, "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        self.pb[self.index] = f'(ASSIGN, {self.semantic_stack.top()}, {self.semantic_stack.top(3)}, )'  # todo why 3 work?
        self.index += 1
        self.semantic_stack.pop()


    def _return(self, **kwargs):
        if self.main_seen:
            return
        self.current_function_address = self.semantic_stack.top()
        self.pb[self.index] = f"(JP, @{self.retrun_temp}, , )"
        self.index += 1
