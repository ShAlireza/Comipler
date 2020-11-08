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
        self.stack_parse.push('Program')

    def parse(self):
        self.__parse()
        self.error_table.write_on_file()
        self.parse_tree.write_tree()

    def __parse(self):
        while True:
            if self.current_token[0] == '$' and self.stack_parse.peak() == '$':
                break
            elif self.stack_parse.peak() in self.terminals:
                if self.current_token[0] == 'ID' or self.current_token[0] == 'NUM':
                    if self.stack_parse.peak() == self.current_token[0]:
                        self.stack_parse.pop()
                        self.parse_tree.add_node_to_tree()
                    else:
                        self.parse_tree.add_node_to_tree()
                        term = (self.current_token
                                if self.current_token != '$' else 'EOF')
                        self.error_table.log(error_message=f'unexpected {term}',
                                             line_number=scanner.line_num)

                else:
                    if self.stack_parse.peak() == self.current_token[1]:
                        self.stack_parse.pop()
                        self.parse_tree.add_node_to_tree()
                    else:
                        self.parse_tree.add_node_to_tree()
                        term = (self.current_token
                                if self.current_token != '$' else 'EOF')
                        self.error_table.log(error_message=f'unexpected {term}',
                                             line_number=scanner.line_num)

            elif self.stack_parse.peak() in self.non_terminals:
                if self.current_token[0] == 'ID' or self.current_token[0] == 'NUM':
                    if self.current_token[0] in self.parse_table[self.stack_parse.peak()]:
                        if self.parse_table[self.stack_parse.peak()][self.current_token[0]] == 'synch':
                            self.parse_tree.add_node_to_tree()
                            self.stack_parse.pop()
                            self.error_table.log(
                                error_message=f'missing {self.current_token}',
                                line_number=scanner.line_num)
                        else:
                            NT = self.stack_parse.pop()
                            states = self.parse_table[NT][self.current_token[1]]
                            if NT != 'Program':
                                self.parse_tree.add_node_to_tree()
                            states = list(states.split())
                            ste = [0] * len(states)
                            for i in range(len(states)):
                                ste[i] = states[len(states) - i - 1]
                            self.parse_tree.add_nodes_to_stacks(ste)
                            for k in ste:
                                self.stack_parse.push(k)
                    else:
                        self.current_token = scanner.get_next_token_for_parser()
                        self.error_table.log(
                            error_message=f'illegal {self.current_token}',
                            line_number=scanner.line_num)
                if self.current_token[0] == 'KEYWORD' or self.current_token[0] == 'SYMBOL':
                    if self.current_token[1] in self.parse_table[self.stack_parse.peak()]:
                        if self.parse_table[self.stack_parse.peak()][self.current_token[1]] == 'synch':
                            self.parse_tree.add_node_to_tree()
                            self.stack_parse.pop()
                            self.error_table.log(
                                error_message=f'missing {self.current_token}',
                                line_number=scanner.line_num)
                        else:
                            NT = self.stack_parse.pop()
                            states = self.parse_table[NT][self.current_token[1]]
                            if NT != 'Program':
                                self.parse_tree.add_node_to_tree()
                            states = list(states.split())
                            ste = [0] * len(states)
                            for i in range(len(states)):
                                ste[i] = states[len(states) - i - 1]
                            self.parse_tree.add_nodes_to_stacks(ste)
                            for k in ste:
                                self.stack_parse.push(k)
                    else:
                        self.current_token = scanner.get_next_token_for_parser()
                        self.error_table.log(
                            error_message=f'illegal {self.current_token}',
                            line_number=scanner.line_num)

    def compute_first(self, expression):
        # expression would be something like "[ NoneTerminal ] +"
        words = expression.split()
        answer = []
        flag = True
        for word in words:
            if '$' in word or '#&' in word:
                continue
            for x in self.firsts[word]:
                answer.append(x)
            if '#&' in answer:
                answer.remove('#&')
            if '#&' not in self.firsts[word]:
                flag = False
                break
        if flag:
            answer.append('#&')
        answer = set(answer)
        answer = list(answer)
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
        for x in self.terminals:
            self.firsts[x] = x

    def initial_parse_table(self):
        for NT in self.non_terminals:
            self.parse_table[NT] = {}
            # for T in terminals:
            #     parse_table[NT][T] = None
        with open('Grammar.csv', 'r') as file:
            for line in file.readlines():
                words = line.strip().split()
                for i in range(1, len(words)):
                    f = self.compute_first(' '.join(words[1:]))
                    for ter in f:
                        if ter != '#&':
                            self.parse_table[words[0]][ter] = ' '.join(words[1:])
                        else:
                            for t in self.follows[words[0]]:
                                self.parse_table[words[0]][t] = ' '.join(words[1:])
        for NT in self.non_terminals:
            for t_prime in self.follows[NT]:
                self.parse_table[NT][t_prime] = 'synch'


parser = Parser()
parser.parse()
