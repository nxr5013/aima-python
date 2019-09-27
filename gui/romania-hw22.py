from tkinter import *
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import *
from search import breadth_first_tree_search as bfts, depth_first_tree_search as dfts, uniform_cost_search as ucs
from gui.tree_node import *
import random
root = None
romania_problem = None
start = None
goal = None

def bfs2():
    global romania_problem, start, goal
    romania_problem = GraphProblem(start.get(), goal.get(), romania_map)
    final_path = [start.get()]
    totalPath = 0
    result, visited_count, tree_size = bfts(romania_problem)
    if result != None:
        final_path += result.solution()
        for i in range(len(final_path) - 1):
            totalPath += romania_map.get(final_path[i], final_path[i + 1])

    return totalPath, visited_count, tree_size

def dfs2():
    global romania_problem, start, goal
    romania_problem = GraphProblem(start.get(), goal.get(), romania_map)
    final_path = [start.get()]
    totalPath = 0
    result, visited_count, tree_size = dfts(romania_problem)
    if result != None:
        final_path += result.solution()
        for i in range(len(final_path) - 1):
            totalPath += romania_map.get(final_path[i], final_path[i + 1])

    return totalPath, visited_count, tree_size


def ucs2():
    global romania_problem, start, goal
    romania_problem = GraphProblem(start.get(), goal.get(), romania_map)
    final_path = [start.get()]
    totalPath = 0
    result, visited_count, tree_size = ucs(romania_problem)
    if result != None:
        final_path += result.solution()
        for i in range(len(final_path) - 1):
            totalPath += romania_map.get(final_path[i], final_path[i + 1])

    return totalPath, visited_count, tree_size


def main():
    global start, goal, next_button, romania_map
    root = Tk()
    start = StringVar(root)
    goal = StringVar(root)
    places = ["Oradea", "Zerind", "Arad", "Timisoara", "Lugoj",
                "Mehadia", "Drobeta", "Craiova", "Rimnicu", "Sibiu",
                "Fagaras", "Pitesti", "Bucharest", "Giurgiu", "Urziceni",
                "Hisova", "Eforie", "Vaslui", "lasi", "Neamt"]
    searches = ["Breadth-First Tree Search", "Depth-First Tree Search", "Uniform Cost Search"]

    data = dict()
    count = 0
    for search in searches:
        data[search] = list()
        for i in range(5):
            start.set(places[random.randint(0, len(places) - 1)])
            goal.set(places[random.randint(0, len(places) - 1)])
            if count == 0:
                data[search].append(bfs2())
            elif count == 1:
                data[search].append(dfs2())
            else:
                data[search].append(ucs2())
        count += 1
    for key in data:
        print("key:", key, ":", data[key])


if __name__ == "__main__":
    main()
