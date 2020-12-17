"""
Abolfazl Rahimi 97105941
Alireza Shateri 97106035
"""
import scanner
import tree

from code_generator import CodeGenerator
from semantic_stack import SemanticStack


class Table:

    def log(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def write_on_file(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")


class ErrorTable(Table):
    TEMPLATE = '#{line} : Syntax Error, {message}'

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
        self.semantic_stack = SemanticStack()
        self.code_generator = CodeGenerator(self.semantic_stack)

    def parse(self):
        self.__parse()
        self.error_table.write_on_file()
        self.parse_tree.write_tree()

    def __parse(self):
        while True:
            if '#' in self.stack_parse.peak():
                if self.current_token[0] == 'ID' or self.current_token[
                    0] == 'NUM':
                    self.code_generator('_' + self.stack_parse.pop()[1:],
                                        _input=self.current_token[1])
                else:
                    self.code_generator('_' + self.stack_parse.pop()[1:],
                                        _input=self.current_token[1])
            elif self.current_token[
                0] == '$' and self.stack_parse.peak() == '$':
                self.parse_tree.add_node_to_tree(None)
                break
            elif self.stack_parse.peak() in self.terminals:
                if self.current_token[0] == 'ID' or self.current_token[
                    0] == 'NUM':
                    if self.stack_parse.peak() == self.current_token[0]:
                        self.parse_tree.add_node_to_tree(self.current_token)
                        self.current_token = scanner.get_next_token_for_parser()
                        self.stack_parse.pop()
                    else:
                        self.parse_tree.delete()
                        self.error_table.log(
                            error_message=f'missing {self.stack_parse.peak()}',
                            line_number=scanner.line_num)
                        self.stack_parse.pop()
                else:
                    if self.stack_parse.peak() == self.current_token[1]:
                        self.stack_parse.pop()
                        self.parse_tree.add_node_to_tree(self.current_token)
                        self.current_token = scanner.get_next_token_for_parser()
                    else:
                        self.parse_tree.delete()
                        self.error_table.log(
                            error_message=f'missing {self.stack_parse.peak()}',
                            line_number=scanner.line_num)
                        self.stack_parse.pop()
            elif self.stack_parse.peak() in self.non_terminals:
                if self.current_token[0] == 'ID' or self.current_token[
                    0] == 'NUM':
                    if self.current_token[0] in self.parse_table[
                        self.stack_parse.peak()]:
                        if self.parse_table[self.stack_parse.peak()][
                            self.current_token[0]] == 'synch':
                            self.parse_tree.delete()
                            self.error_table.log(
                                error_message=f'missing {self.stack_parse.peak()}',
                                line_number=scanner.line_num)
                            self.stack_parse.pop()
                            # break
                        else:
                            NT = self.stack_parse.pop()
                            states = self.parse_table[NT][
                                self.current_token[0]]
                            states = list(states.split())
                            ste = [0] * len(states)
                            for i in range(len(states)):
                                ste[i] = states[len(states) - i - 1]
                            if NT != 'Program':
                                self.parse_tree.add_node_to_tree(None)
                            if "eps" in ste:
                                self.parse_tree.add_nodes_to_stacks(
                                    ['epsilon'])
                                self.parse_tree.add_node_to_tree(None)
                                continue
                            self.parse_tree.add_nodes_to_stacks(ste)
                            for k in ste:
                                self.stack_parse.push(k)
                            # break
                    else:
                        self.error_table.log(
                            error_message=f'illegal {self.current_token[0]}',
                            line_number=scanner.line_num)
                        self.current_token = scanner.get_next_token_for_parser()
                        # break
                elif self.current_token[0] == 'KEYWORD' or self.current_token[
                    0] == 'SYMBOL':
                    if self.current_token[1] in self.parse_table[
                        self.stack_parse.peak()]:
                        if self.parse_table[self.stack_parse.peak()][
                            self.current_token[1]] == 'synch':
                            self.parse_tree.delete()
                            self.error_table.log(
                                error_message=f'missing {self.stack_parse.peak()}',
                                line_number=scanner.line_num)
                            self.stack_parse.pop()
                            # break
                        else:
                            NT = self.stack_parse.pop()
                            states = self.parse_table[NT][
                                self.current_token[1]]
                            states = list(states.split())
                            ste = [0] * len(states)
                            for i in range(len(states)):
                                ste[i] = states[len(states) - i - 1]
                            if NT != 'Program':
                                self.parse_tree.add_node_to_tree(None)
                            if "eps" in ste:
                                self.parse_tree.add_nodes_to_stacks(
                                    ['epsilon'])
                                self.parse_tree.add_node_to_tree(None)
                                continue
                            self.parse_tree.add_nodes_to_stacks(ste)
                            for k in ste:
                                self.stack_parse.push(k)
                            # break

                    else:
                        if self.current_token[0] == '$':
                            self.error_table.log(
                                error_message=f'Unexpected {"EOF"}',
                                line_number=scanner.line_num)
                            break
                        self.error_table.log(
                            error_message=f'illegal {self.current_token[1]}',
                            line_number=scanner.line_num)
                        self.current_token = scanner.get_next_token_for_parser()
                else:
                    if self.current_token[1] in self.parse_table[
                        self.stack_parse.peak()]:
                        if self.parse_table[self.stack_parse.peak()][
                            self.current_token[1]] == 'synch':
                            self.parse_tree.delete()
                            self.error_table.log(
                                error_message=f'Missing {self.stack_parse.peak()}',
                                line_number=scanner.line_num)
                            self.stack_parse.pop()
                            # break
                        else:
                            NT = self.stack_parse.pop()
                            states = self.parse_table[NT][
                                self.current_token[1]]
                            states = list(states.split())
                            ste = [0] * len(states)
                            for i in range(len(states)):
                                ste[i] = states[len(states) - i - 1]
                            if NT != 'Program':
                                self.parse_tree.add_node_to_tree(None)
                            if "eps" in ste:
                                self.parse_tree.add_nodes_to_stacks(
                                    ['epsilon'])
                                self.parse_tree.add_node_to_tree(None)
                                continue
                            self.parse_tree.add_nodes_to_stacks(ste)
                            for k in ste:
                                self.stack_parse.push(k)
                            # break

                    else:
                        self.error_table.log(
                            error_message=f'Unexpected {"EOF"}',
                            line_number=scanner.line_num)
                        break

                        # break

    def compute_first(self, expression):
        # expression would be something like "[ NoneTerminal ] +"
        words = expression.split(' ')
        answer = []
        flag = True
        for word in words:
            if '#' in word:
                continue
            if word == 'eps':
                continue
            for x in self.firsts[word]:
                answer.append(x)
            if 'eps' in answer:
                answer.remove('eps')
            if 'eps' not in self.firsts[word]:
                flag = False
                break
        if flag:
            answer.append('eps')
        # print('**********************FIRST OF EXPRESSION STARTS*****************************')
        # print(words, list(answer))
        # print('**********************FIRST OF EXPRESSION ENDS*****************************')
        return list(answer)

    def fill_follow_dict(self):
        with open("Follows.csv", 'r') as file:
            for line in file.readlines():
                words = line.strip().split(' ')
                self.follows[words[0]] = words[1:]
                self.non_terminals.append(words[0])
        # print("-------------------FOLLOW DICTIONARY--------------------------------------")
        # for x in self.follows:
        #     print(x, self.follows[x])
        # print("-------------------FOLLOW DICTIONARY END----------------------------------")

    def fill_first_dict(self):
        with open("Firsts.csv", 'r') as file:
            for line in file.readlines():
                words = line.strip().split(' ')
                self.firsts[words[0]] = words[1:]
        for x in self.terminals:
            self.firsts[x] = [x]
        # print("-------------------FIRST DICTIONARY--------------------------------------")
        # for x in self.firsts:
        #     print(self.firsts[x])
        # print("-------------------FIRST DICTIONARY END----------------------------------")

    def initial_parse_table(self):
        for NT in self.non_terminals:
            self.parse_table[NT] = {}
            # for T in terminals:
            #     parse_table[NT][T] = None
        with open('Grammar1.csv', 'r') as file:
            w = file.readlines()
            for line in w:
                words = line.strip().split()
                f = self.compute_first(' '.join(words[1:]))
                for i in range(1, len(words)):
                    for ter in f:
                        if ter != 'eps':
                            if ter in self.terminals:
                                self.parse_table[words[0]][ter] = ' '.join(
                                    words[1:])
                            if '$' in self.follows[words[0]]:
                                self.parse_table[words[0]][ter] = ' '.join(
                                    words[1:])
                        else:
                            for t in self.follows[words[0]]:
                                self.parse_table[words[0]][t] = ' '.join(
                                    words[1:])
        for NT in self.non_terminals:
            for t_prime in self.follows[NT]:
                if t_prime not in self.parse_table[NT]:
                    self.parse_table[NT][t_prime] = 'synch'


parser = Parser()
parser.parse()

for code in parser.code_generator.pb:
    if code != '0':
        print(code)

with open('output.txt', 'w') as file:
    for i, code in enumerate(parser.code_generator.pb):
        if code == '0':
            break
        file.write(f'{i}\t{code}\n')
