from tkinter import *
import os.path
from search import *
from search import breadth_first_tree_search as bfts, depth_first_tree_search as dfts, uniform_cost_search as ucs
from gui.tree_node import *
import random
import matplotlib.pyplot as plt

import numpy as np


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
romania_problem = None


def perform_search(search, start, goal):
    global romania_problem
    romania_problem = GraphProblem(start, goal, romania_map)
    final_path = [start]
    total_cost = 0

    target_node, visited_count, tree_size = search(romania_problem)
    if target_node is not None:
        final_path += target_node.solution()
        for i in range(len(final_path) - 1):
            total_cost += romania_map.get(final_path[i], final_path[i + 1])

        return total_cost, visited_count, tree_size

    else:
        return None


def plot_boxplots(data, title):
    labels = ["Breadth First Search", "Depth First Search", "Uniform Cost Search"]
    plt.boxplot(data, labels=labels)
    plt.title(title)
    plt.show()


def average(data):
    avg = 0
    for num in data:
        avg += num
    return avg / len(data)


def populate_missing_data(data):
    for search in data.keys():
        lst = data[search]
        if len(lst) < 50:
            avg = average(lst)
            lst += [avg] * (50 - len(lst))


def main():

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
            start = (places[random.randint(0, len(places) - 1)])
            goal = (places[random.randint(0, len(places) - 1)])

            results = perform_search(search_function, start, goal)
            if results is not None:
                path_costs[search].append(results[0])
                visited_counts[search].append(results[1])
                tree_sizes[search].append(results[2])
            i += 1

    populate_missing_data(path_costs)
    populate_missing_data(visited_counts)
    populate_missing_data(tree_sizes)

    for search in searches:
        print(search)
        print('path_costs = ', path_costs[search])
        print('visited_counts = ', visited_counts[search])
        print('tree_sizes = ', tree_sizes[search])

    plot_boxplots([np.asarray(path_costs['bfs']), np.asarray(path_costs['dfs']), np.asarray(path_costs['ucs'])], 'Path Costs')
    plot_boxplots([np.asarray(visited_counts['bfs']), np.asarray(visited_counts['dfs']), np.asarray(visited_counts['ucs'])], 'Visited Counts')
    plot_boxplots([np.asarray(tree_sizes['bfs']), np.asarray(tree_sizes['dfs']), np.asarray(tree_sizes['ucs'])], 'Tree Size')


if __name__ == "__main__":
    main()
