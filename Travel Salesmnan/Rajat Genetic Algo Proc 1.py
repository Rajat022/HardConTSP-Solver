#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import random
import time
import matplotlib.pyplot as plt

def read_tsp_file(filename):
    tsp = {}
    with open(filename) as f:
        for line in f:
            if line.startswith("DIMENSION"):
                tsp["n"] = int(line.split(":")[1])
            elif line.startswith("NODE_COORD_SECTION"):
                tsp["cities"] = {}
                for i in range(tsp["n"]):
                    x, y = map(float, next(f).split()[1:])
                    tsp["cities"][i] = (x, y)
    return tsp

def generate_random_tour(tsp):
    tour = list(range(tsp["n"]))
    random.shuffle(tour)
    return tour

def nearest_neighbor(tsp):
    cities = tsp["cities"]
    start_city = random.choice(list(cities.keys()))
    tour = [start_city]
    unvisited_cities = set(cities.keys())
    unvisited_cities.remove(start_city)
    while unvisited_cities:
        nearest_city = min(unvisited_cities, key=lambda city: distance(cities, tour[-1], city))
        tour.append(nearest_city)
        unvisited_cities.remove(nearest_city)
    return tour, 0

def distance(cities, i, j):
    """
    Calculate the Euclidean distance between two cities
    """
    xi, yi = cities[i]
    xj, yj = cities[j]
    return math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

def evaluate_tour(tour, tsp):
    """
    Calculate the total distance of the tour
    """
    n = len(tour)
    total_distance = 0
    for i in range(n):
        j = (i + 1) % n
        city_i = tour[i]
        city_j = tour[j]
        x_i, y_i = tsp["cities"][city_i]
        x_j, y_j = tsp["cities"][city_j]
        total_distance += distance(tsp["cities"], city_i, city_j)
    return total_distance

def evaluate_relative_length(tour_length, tsp_file, best_known_solution):
    return tour_length / best_known_solution[tsp_file]

def plot_tour(tour, tsp):
    """
    Plot the cities and the tour
    """
    cities = tsp["cities"]
    x = [cities[i][0] for i in tour]
    y = [cities[i][1] for i in tour]
    plt.figure()
    plt.plot(x, y, 'o')
    plt.plot(x + [x[0]], y + [y[0]], '-')
    plt.show()

# Test the procedures on the given TSP files
tsp_files = ["berlin52.tsp", "eil101.tsp", "lin318.tsp", "pr1002.tsp", "rl5934.tsp", "d18512.tsp"]
best_known_solution = {"berlin52.tsp": 7542, "eil101.tsp": 629, "lin318.tsp": 42029, "pr1002.tsp": 259045,
                       "rl5934.tsp": 118282, "d18512.tsp": 645238}

for tsp_file in tsp_files:
    print(f"\n\n***** Results for {tsp_file} *****")
    tsp = read_tsp_file(tsp_file)
    
    # Random Tour
    start_time = time.time()
    random_tour = generate_random_tour(tsp)
    random_tour_time = time.time() - start_time
    random_tour_length = evaluate_tour(random_tour, tsp)
    random_tour_relative_length = evaluate_relative_length(random_tour_length, tsp_file, best_known_solution)
    print(f"Random Tour Execution Time: {random_tour_time} seconds")
    print(f"Random Tour Length: {random_tour_length}")
    print(f"Random Tour Relative Length: {random_tour_relative_length}")
    plot_tour(random_tour, tsp)
    
    # Nearest Neighbor
    start_time = time.time()
    nearest_neighbor_tour, nearest_neighbor_time = nearest_neighbor(tsp)
    nearest_neighbor_length = evaluate_tour(nearest_neighbor_tour, tsp)
    nearest_neighbor_relative_length = evaluate_relative_length(nearest_neighbor_length, tsp_file, best_known_solution)
    print(f"Nearest Neighbor Execution Time: {nearest_neighbor_time} seconds")
    print(f"Nearest Neighbor Length: {nearest_neighbor_length}")
    print(f"Nearest Neighbor Relative Length: {nearest_neighbor_relative_length}")
    plot_tour(nearest_neighbor_tour, tsp)

