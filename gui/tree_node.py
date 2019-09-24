from tkinter import Tk, Canvas, Scrollbar, HORIZONTAL, BOTTOM, VERTICAL, X, Y, BOTH, LEFT, RIGHT
from math import floor

root = None
current = None
front = []

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

        if self.children:
            middle_idx = len(self.children) // 2

            if len(self.children) % 2 != 0:
                middle_child = self.children[middle_idx]
                middle_child.x = self.x
                middle_child.y = self.y + 60
                middle_child.draw()

                for idx in range(0, middle_idx):
                    self.draw_odd_child(idx, middle_idx)

                for idx in range(middle_idx + 1, len(self.children)):
                    self.draw_odd_child(idx, middle_idx)

            else:
                for idx in range(0, len(self.children)):
                    self.draw_even_child(idx, middle_idx)

    def draw_odd_child(self, idx, middle_idx):
        child = self.children[idx]
        padding = 0
        if idx < middle_idx:
            for i in range(idx + 1, middle_idx):
                padding += self.children[i].width
            padding += floor(len(self.children) // 2) * 20
            padding += self.children[middle_idx].width / 2.0
            padding += child.width / 2.0
            child.x = self.x - padding
            child.y = self.y + 60
        elif idx > middle_idx:
            for i in range(middle_idx + 1, idx):
                padding += self.children[i].width
            padding += floor(len(self.children) // 2) * 20
            padding += self.children[middle_idx].width / 2.0
            padding += child.width / 2.0
            child.x = self.x + padding
            child.y = self.y + 60
        child.draw()

    def draw_even_child(self, idx, middle_idx):
        child = self.children[idx]
        padding = 0
        if idx < middle_idx:
            for i in range(idx + 1, middle_idx):
                padding += self.children[i].width
            padding += ((len(self.children) // 2) - idx - 1) * 20
            padding += 10
            padding += child.width / 2
            child.x = self.x - padding
            child.y = self.y + 60
        else:
            for i in range(middle_idx, idx):
                padding += self.children[i].width
            padding += (idx - (len(self.children) // 2)) * 20
            padding += 10
            padding += child.width / 2
            child.x = self.x + padding
            child.y = self.y + 60
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
    global current, root, front
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


def remove_node(node):
    global front, root
    for leaf in front:
        if leaf.data == node.state:
            if leaf == root or leaf.parent.data == node.parent:
                papi = leaf.parent
                papi.children.remove(leaf)
                front.remove(leaf)
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
    global current
    current.status = 'd'


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
    global root, current, front
    root = None
    current = None
    front = []


def main():
    # root = TreeNode("root", None)
    # parent1 = TreeNode("parent1", root)
    # child1 = TreeNode("child1", parent1)
    # child2 = TreeNode("child2", parent1)
    # child3 = TreeNode("child3", parent1)
    # child4 = TreeNode("child4", parent1)
    #
    # parent2 = TreeNode("parent2", root)
    # child5 = TreeNode("child5", parent2)
    # child6 = TreeNode("child6", parent2)
    # child7 = TreeNode("child7", parent2)
    # child8 = TreeNode('child8', parent2)
    # # child10 = SearchNode('child10', parent1)
    #
    # grandchild1 = TreeNode("grandchild1", child6)
    # grandchild2 = TreeNode("grandchild2", child7)
    # # child9 = SearchNode('child9', parent3)
    # root.children = [parent1, parent2]
    # parent1.children = [child1, child2, child3, child4]
    # parent2.children = [child5, child6, child7, child8]
    # child6.children = [grandchild1]
    # child7.children = [grandchild2]
    #
    # print(root.horizontal_distance())
    window.mainloop()


if __name__ == '__main__':
    main()
