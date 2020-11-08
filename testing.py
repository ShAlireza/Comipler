from anytree import Node, RenderTree

p = Node('start', children=[Node('1'), Node('2'), Node('3')])
x = Node('khar', line=1, parent=p)

for pre, _, node in RenderTree(p):
    print("%s%s" % (pre, node.name))

with open('parse_tree.txt', 'w', newline='', encoding="utf-8") as csv_file:
    csv_file.write(RenderTree(p).__str__())



