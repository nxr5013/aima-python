from tkinter import *
import os.path
from search import *
from search import breadth_first_tree_search as bfts, depth_first_tree_search as dfts, uniform_cost_search as ucs
from gui.tree_node import *
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
root = None
romania_problem = None
start = None
goal = None


def perform_search(search):
    global romania_problem, start, goal
    romania_problem = GraphProblem(start.get(), goal.get(), romania_map)
    final_path = [start.get()]
    total_cost = 0

    target_node, visited_count, tree_size = search(romania_problem)
    if target_node is not None:
        final_path += target_node.solution()
        for i in range(len(final_path) - 1):
            total_cost += romania_map.get(final_path[i], final_path[i + 1])

        return total_cost, visited_count, tree_size

    else:
        return None


def main():
    global start, goal
    start = StringVar(root)
    goal = StringVar(root)
    places = ["Oradea", "Zerind", "Arad", "Timisoara", "Lugoj", "Mehadia", "Drobeta", "Craiova", "Rimnicu", "Sibiu",
              "Fagaras", "Pitesti", "Bucharest", "Giurgiu", "Urziceni", "Hisova", "Eforie", "Vaslui", "lasi", "Neamt"]
    searches = {'bfs': bfts, 'dfs': dfts, 'ucs': ucs}

    path_costs = {'bfs': [], 'dfs': [], 'ucs': []}
    visited_counts = {'bfs': [], 'dfs': [], 'ucs': []}
    tree_sizes = {'bfs': [], 'dfs': [], 'ucs': []}

    for search in searches:
        search_function = searches[search]
        i = 0
        while i < 50:
            start.set(places[random.randint(0, len(places) - 1)])
            goal.set(places[random.randint(0, len(places) - 1)])

            results = perform_search(search_function)
            if results is not None:
                path_costs[search].append(results[0])
                visited_counts[search].append(results[1])
                tree_sizes[search].append(results[2])
                i += 1

    for search in searches:
        print(search)
        print('path_costs = ', path_costs[search])
        print('visited_counts = ', visited_counts[search])
        print('tree_sizes = ', tree_sizes[search])


if __name__ == "__main__":
    main()
