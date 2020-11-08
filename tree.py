from anytree import Node, RenderTree


class stack:
    def __init__(self):
        self.data = []

    def push(self, x):
        return self.data.append(x)

    def pop(self):
        return self.data.pop()

    def peak(self):
        return self.data[-1]

    def contains(self, x):
        return self.data.count(x)

    def show_all(self):
        return self.data

    def length(self):
        return len(self.data)


class tree:
    def __init__(self):
        self.id = 0
        self.parents_stack = stack()
        self.children_stack = stack()
        self.root = Node('program')
        self.current_node = self.root

    def add_node_to_tree(self):
        self.children_stack.pop().parent = self.parents_stack.pop()

    def add_nodes_to_stacks(self, node_name):
        self.children_stack.push(Node(node_name))
        self.parents_stack.push(self.current_node)
        self.current_node = self.children_stack.peak()

    def write_tree(self):
        with open('parse_tree.txt', 'wb') as file:
            file.write(RenderTree(self.root))