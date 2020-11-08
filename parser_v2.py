import scanner

import tree


class Table:

    def log(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def write_on_file(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")


class ErrorTable(Table):
    TEMPLATE = '#{line} : syntax error, {message}'

    def __init__(self, file_name='syntax_errors', extension='txt'):
        self.file_name = file_name
        self.extension = extension
        self.id = 0
        self.table = {}

    def log(self, error_message, line_number):
        message = self.TEMPLATE.format(line=line_number,
                                       message=error_message)
        try:
            self.table[line_number].append(message)
        except KeyError as e:
            self.table[line_number] = []
            self.table[line_number].append(message)

    def write_on_file(self):
        with open(f'{self.file_name}.{self.extension}', 'w') as file:
            if len(self.table.items()) == 0:
                file.write("There is no syntax error.")
            for values in self.table.values():
                for value in values:
                    file.write(f'{value}\n')


error_table = ErrorTable()


class Parser:

    def __init__(self):
        self.error_table = ErrorTable()
        self.current_token = scanner.get_next_token_for_parser()
        self.parse_table = {}
        self.firsts = {}
        self.follows = {}
        self.parse_tree = tree.Tree()

        self.stack_parse = tree.Stack()
        self.non_terminals = []
        self.terminals = ['if', 'else', 'void', 'int', 'while', 'break',
                          'switch',
                          'default', 'case', 'return', 'ID', 'NUM', ';', ':',
                          ',',
                          '[', ']',
                          '(', ')', '{', '}', '+', '-', '*', '=',
                          '<', '==', '$', '/']
        self.fill_follow_dict()
        self.fill_first_dict()
        self.initial_parse_table()
        self.stack_parse.push('$')
        self.stack_parse.push('program')

    def parse(self):
        self.parse()
        self.error_table.write_on_file()
        self.parse_tree.write_tree()

    def __parse(self):
        while True:
            if self.current_token[0] == '$' and self.stack_parse.peak() == '$':
                break
            elif self.current_token[0] == self.stack_parse.peak():
                self.stack_parse.pop()
                self.parse_tree.add_node_to_tree()
                self.current_token = scanner.get_next_token_for_parser()
            elif self.stack_parse.peak() in self.non_terminals:
                if self.current_token[0] in \
                        self.parse_table[self.stack_parse.peak()]:
                    if self.parse_table[self.stack_parse.peak()
                    ][self.current_token[0]] == 'synch':
                        self.parse_tree.add_node_to_tree()
                        self.error_table.log(
                            error_message=f'missing {self.current_token}',
                            line_number=scanner.line_num)
                    else:
                        NT = self.stack_parse.pop()
                        states = self.parse_table[NT][self.current_token[0]]
                        self.parse_tree.add_node_to_tree()
                        states = states[::-1]  # states.inverse
                        for k in states:
                            self.parse_tree.add_nodes_to_stacks(k)
                            self.stack_parse.push(k)
                else:
                    pass
                    self.error_table.log(
                        error_message=f'illegal {self.current_token}',
                        line_number=scanner.line_num)
            else:
                self.parse_tree.add_node_to_tree()
                term = (self.current_token
                        if self.current_token != '$' else 'EOF')
                self.error_table.log(error_message=f'unexpected {term}',
                                     line_number=scanner.line_num)

    def compute_first(self, expression):
        # expression would be something like "[ NoneTerminal ] +"
        words = expression.split()
        answer = []
        flag = True
        for word in words:
            answer.append(self.firsts[word])
            answer.remove('ε')
            if 'ε' not in self.firsts[word]:
                flag = False
                break
        if flag:
            answer.append('ε')
        return answer

    def fill_follow_dict(self):
        with open("Follows.csv", 'r') as file:
            for line in file.readlines():
                words = line.strip().split(' ')
                self.follows[words[0]] = words[1:]
                self.non_terminals.append(words[0])

    def fill_first_dict(self):
        with open("Firsts.csv", 'r') as file:
            for line in file.readlines():
                words = line.strip().split(' ')
                self.firsts[words[0]] = words[1:]

    def initial_parse_table(self):
        for NT in self.non_terminals:
            self.parse_table[NT] = {}
            # for T in terminals:
            #     parse_table[NT][T] = None
        with open('Grammar.csv', 'r') as file:
            for line in file.readlines():
                words = line.strip().split()
                for i in range(1, len(words)):
                    for ter in self.compute_first(str(*words[1:])):
                        if ter != 'ε':
                            self.parse_table[words[0]][ter] = ' '.join(words)
                        else:
                            for t in self.follows[words[0]]:
                                self.parse_table[words[0]][t] = ' '.join(words)
        for NT in self.non_terminals:
            for t_prime in self.follows[NT]:
                if t_prime not in self.follows[NT]:
                    self.follows[NT][t_prime] = 'synch'


parser = Parser()
parser.parse()
