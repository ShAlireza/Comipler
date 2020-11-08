from anytree import Node, RenderTree


class Stack:
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


class Tree:
    def __init__(self):
        self.id = 0
        self.parents_stack = Stack()
        self.children_stack = Stack()
        self.root = Node('Program')
        self.current_node = self.root

    def add_node_to_tree(self):
        print(f'Adding node {self.children_stack.peak()} to tree')
        print(self.children_stack.show_all(), self.parents_stack.show_all())
        child = self.children_stack.pop()
        child.parent = self.parents_stack.pop()
        print(child, child.parent)
        self.current_node = self.children_stack.peak()
        print("#####################")
        print(RenderTree(self.root))

    def add_nodes_to_stacks(self, node_names):
        print(node_names, '<=== node names')
        for node_name in node_names:
            self.children_stack.push(Node(node_name))
            self.parents_stack.push(self.current_node)
        print(self.parents_stack.show_all(), '<==== parents')
        self.current_node = self.children_stack.peak()

    def write_tree(self):
        with open('parse_tree.txt', 'w', newline='', encoding="utf-8") as csv_file:
            csv_file.write(RenderTree(self.root).__str__())
