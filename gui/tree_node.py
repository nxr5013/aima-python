from tkinter import Tk, Canvas, Scrollbar, HORIZONTAL, BOTTOM, VERTICAL, X, Y, BOTH, LEFT, RIGHT
from math import floor

root = None
current = None
front = []
visited_count = 0
tree_size = 0

class TreeNode:
    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.children = []
        self.status = 'f'
        self.width = 40
        self.x = None
        self.y = None


def add_node(node):
    global current, root, front, tree_size
    if current is None:
        root = TreeNode(data=node.state, parent=None)
        front.append(root)
    else:
        if current.data == node.parent.state:
            new_node = TreeNode(data=node.state, parent=current)
            current.children += [new_node]
            front.append(new_node)

        else:
            parent = root.find_right_spot(node)
            new_node = TreeNode(data=node.state, parent=parent)
            parent.children.append(new_node)
            front.append(new_node)

    tree_size += 1


def remove_node(node):
    global front, root, tree_size
    for leaf in front:
        if leaf.data == node.state:
            if leaf == root or leaf.parent.data == node.parent:
                papi = leaf.parent
                papi.children.remove(leaf)
                front.remove(leaf)
                tree_size -= 1
                break


def mark_exploring(node):
    global front, current, visited_count
    for n in front:
        if n.data == node.state:
            if n == root or n.parent.data == node.parent.state:
                n.status = 'e'
                current = n
                front.remove(n)
                visited_count += 1
                break


def mark_explored(node):
    global current, visited_count
    current.status = 'd'


def set_path(node):
    node.status = 't'
    if node.parent:
        set_path(node.parent)


def mark_target(node):
    global current, root, front, tree_size, visited_count

    if current.data == node.state:
        set_path(current)

    else:
        for child in front:
            if child.data == node.state:
                if child == root or child.parent.data == node.parent.state:
                    set_path(child)
                    return visited_count, tree_size
        add_node(node)
        set_path(front[-1])
        tree_size += 1
        # visited_count += 1
    return visited_count, tree_size


def reset_tree():
    global root, current, front, visited_count, tree_size
    root = None
    current = None
    front = []
    visited_count = 0
    tree_size = 0
