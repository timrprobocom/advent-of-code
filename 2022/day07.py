import sys

test = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day07.txt').readlines()]

DEBUG = 'debug' in sys.argv

class Node:
    def __init__(self, name=''):
        self.name = name
        self.children = {}
        self.size = 0
        self.allsize = 0
    def __repr__(self):
        return f"<Node {self.name} has {len(self.children)} children, size {self.size}, allsize {self.allsize}"

def find(node,path):
    for c in path:
        node = node.children[c]
    return node

sumx = 0

def part1(data):
    root = Node('/')
    leaf = root
    cd = []
    for line in data:
        parts = line.split()
        if parts[0] == '$':
            if parts[1] == 'cd':
                if parts[2] == '/':
                    cd = []
                    leaf = root
                elif parts[2] == '..':
                    cd.pop()
                    leaf = find(root,cd)
                else:
                    cd.append( parts[2] )
                    leaf = leaf.children[parts[2]]
        elif parts[0] == 'dir':
            leaf.children[parts[1]] = Node(parts[1])
        else:
            leaf.size += int(parts[0])

    # Make a list in depth order.

    q = [root]
    i = 0
    while i < len(q):
        q.extend(list(q[i].children.values()))
        i += 1

    # Unroll that, accumulating the sizes, summing those below 100000.

    qsum = 0
    while q:
        node = q.pop()
        if node.children:
            node.allsize = node.size + sum( n.allsize for n in node.children.values() )
        else:
            node.allsize = node.size
        if node.allsize <= 100000:
            qsum += node.allsize
    if DEBUG:
        print(qsum)

    assert root.allsize > 40000000
    need = root.allsize - 40000000

    # Now do a top-down, remembering all sizes larger than "need".

    q = [root]
    poss = []
    while q:
        node = q.pop(0)
        if node.allsize >= need:
            poss.append(node.allsize)
        q.extend(list(node.children.values()))
    if DEBUG:
        print(poss)

    return qsum, min(poss)

print("Part 1, 2:", part1(data))
