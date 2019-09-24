from tkinter import Tk, Canvas, Scrollbar, HORIZONTAL, BOTTOM, VERTICAL, X, Y, BOTH, LEFT, RIGHT
from math import floor

root = None
current = None
front = []
visited_count = 0
tree_size = 0

window = Tk()
window.geometry('800x800')
canvas = Canvas(window, width=500, height=500, scrollregion=(0,0,10000,10000))
hbar=Scrollbar(window,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)

vbar=Scrollbar(window,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.xview_moveto(0.45)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

canvas.pack(side=LEFT,expand=True,fill=BOTH)


class TreeNode:
    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.children = []
        self.status = 'f'
        self.width = 40
        self.x = None
        self.y = None

    def draw(self):
        global canvas
        if self.x is None and self.y is None:
            self.x = self.width / 2.0 + 4900
            self.y = 100.0

        canvas.create_oval(self.x + 20, self.y + 20, self.x - 20, self.y - 20, fill=self.color())
        canvas.create_text(self.x, self.y, text=self.data[0])

        if self.parent is not None:
            canvas.create_line(self.parent.x, self.parent.y + 20, self.x, self.y - 20)

        location = self.x - (self.width / 2)
        for child in self.children:
            location += child.width / 2
            child.x = location
            child.y = self.y + 60
            location += child.width / 2
            location += 20

        for child in self.children:
            child.draw()

    def calculate_horizontal_distance(self):
        if not self.children:
            return 40

        total = 0
        for child in self.children:
            total += child.calculate_horizontal_distance()

        self.width = total + ((len(self.children) - 1) * 20)
        return self.width

    def color(self):
        if self.status == 'f':
            return 'orange'
        elif self.status == 'e':
            return 'red'
        elif self.status == 'd':
            return 'grey'
        elif self.status == 't':
            return 'green'

    def find_right_spot(self, node):
        if self.data == node.parent.state:
            match = True
            for child in self.children:
                if child.data == node.state:
                    match = False
                    break
            if match:
                return self
            else:
                for child in self.children:
                    spot = child.find_right_spot(node)
                    if spot is not None:
                        return spot
        else:
            for child in self.children:
                spot = child.find_right_spot(node)
                if spot is not None:
                    return spot


def draw_tree():
    global root
    clear()
    root.calculate_horizontal_distance()
    root.draw()


def clear():
    canvas.delete('all')


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
    global front, current
    for n in front:
        if n.data == node.state:
            if n == root or n.parent.data == node.parent.state:
                n.status = 'e'
                current = n
                front.remove(n)
                break


def mark_explored(node):
    global current, visited_count
    current.status = 'd'
    visited_count += 1


def set_path(node):
    node.status = 't'
    if node.parent:
        set_path(node.parent)


def mark_target(node):
    global current, root, front

    if current.data == node.state:
        set_path(current)

    else:
        for child in front:
            if child.data == node.state:
                if child == root or child.parent.data == node.parent.state:
                    set_path(child)
                    return
        add_node(node)
        set_path(front[-1])


def reset_tree():
    global root, current, front, visited_count, tree_size
    root = None
    current = None
    front = []
    visited_count = 0
    tree_size = 0
