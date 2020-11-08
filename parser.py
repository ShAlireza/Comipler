from anytree import Node

import scanner

import tree


stack_parse = tree.stack()
non_terminals = []
terminals = ['if', 'else', 'void', 'int', 'while', 'break', 'switch',
             'default', 'case', 'return', 'ID', 'NUM', ';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=',
             '<', '==', '$', '/']
parse_table = {}
firsts = {}
follows = {}
parse_tree = tree.tree()


# besides that it computes terminal states ####
def fill_follow_dict():
    with open("Follows.csv", 'r') as file:
        for line in file.readlines():
            words = line.strip().split(' ')
            follows[words[0]] = words[1:]
            non_terminals.append(words[0])


def fill_first_dict():
    with open("Firsts.csv", 'r') as file:
        for line in file.readlines():
            words = line.strip().split(' ')
            firsts[words[0]] = words[1:]


def compute_first(expression):  # expression would be something like "[ NoneTerminal ] +"
    words = expression.split()
    answer = []
    flag = True
    for word in words:
        answer.append(firsts[word])
        answer.remove('ε')
        if 'ε' not in firsts[word]:
            flag = False
            break
    if flag:
        answer.append('ε')
    return answer


def initial_parse_table():
    for NT in non_terminals:
        parse_table[NT] = {}
        # for T in terminals:
        #     parse_table[NT][T] = None
    with open('Grammar.csv', 'r') as file:
        for line in file.readlines():
            words = line.strip().split()
            for i in range(1, len(words)):
                for ter in compute_first(str(*words[1:])):
                    if ter != 'ε':
                        parse_table[words[0]][ter] = ' '.join(words)
                    else:
                        for t in follows[words[0]]:
                            parse_table[words[0]][t] = ' '.join(words)
    for NT in non_terminals:
        for t_prime in follows[NT]:
            if t_prime not in follows[NT]:
                follows[NT][t_prime] = 'synch'


fill_follow_dict()
fill_first_dict()
initial_parse_table()
stack_parse.push('$')
stack_parse.push('program')
current_token = scanner.get_next_token_for_parser()

while True:
    if current_token[0] == '$' and stack_parse.peak() == '$':
        break
    elif current_token[0] == stack_parse.peak():
        stack_parse.pop()
        parse_tree.add_node_to_tree()
        current_token = scanner.get_next_token_for_parser()
    elif stack_parse.peak() in non_terminals:
        if current_token[0] in parse_table[stack_parse.peak()]:
            if parse_table[stack_parse.peak()][current_token[0]] == 'synch':
                pass  # \todo
                continue
            else:
                NT = stack_parse.pop()
                states = parse_table[NT][current_token[0]]
                parse_tree.add_node_to_tree()
                states = states[::-1]  # states.inverse
                for k in states:
                    parse_tree.add_nodes_to_stacks(k)
                    stack_parse.push(k)
        else:
            pass
            #  \todo
    else:
        pass
        #  \todo
