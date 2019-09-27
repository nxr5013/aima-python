from tkinter import *
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import *
from search import breadth_first_tree_search as bfts, depth_first_tree_search as dfts, uniform_cost_search as ucs
from gui.tree_node import *

root = None
romania_problem = None
start = None
goal = None

def bfs2():
    global romania_problem, start, goal
    romania_problem = GraphProblem(start.get(), goal.get(), romania_map)
    final_path = [start.get()]
    result, visited_count, tree_size = bfts(romania_problem)
    final_path += result.solution()
    totalPath = 0
    for i in range(len(final_path) - 1):
        totalPath += romania_map.get(final_path[i], final_path[i + 1])

    return totalPath, visited_count, tree_size

def dfs2():
    global romania_problem, start, goal
    romania_problem = GraphProblem(start.get(), goal.get(), romania_map)
    final_path = [start.get()]
    result, visited_count, tree_size = dfts(romania_problem)
    final_path += result.solution()
    totalPath = 0
    for i in range(len(final_path) - 1):
        totalPath += romania_map.get(final_path[i], final_path[i + 1])

    return totalPath, visited_count, tree_size


def ucs2():
    global romania_problem, start, goal
    romania_problem = GraphProblem(start.get(), goal.get(), romania_map)
    final_path = [start.get()]
    result, visited_count, tree_size = ucs(romania_problem)
    final_path += result.solution()
    totalPath = 0
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

    s1 = 0
    s2 = 1
    data = dict()
    for search in searches:
        data[search] = list()
        for i in range(5):
            if s1 != s2:
                start.set(places[2])
                goal.set(places[11])
                data[search].append(ucs2())
                if s2 < len(places):
                    s2 += 1
                else:
                    s1 += 1
                    s2 = 0
    for key in data:
        print(data[key])


if __name__ == "__main__":
    main()
