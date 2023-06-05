#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

def crossover(parent1, parent2):
    """
    Perform crossover between two parent tours to generate a child tour
    """
    n = len(parent1)
    start_index = random.randint(0, n - 1)
    end_index = random.randint(start_index + 1, n)
    child = parent1[start_index:end_index]
    remaining_cities = [city for city in parent2 if city not in child]
    child += remaining_cities
    return child

def mutate(tour):
    """
    Perform mutation on a tour by swapping two cities
    """
    n = len(tour)
    index1, index2 = random.sample(range(n), 2)
    tour[index1], tour[index2] = tour[index2], tour[index1]
    return tour

def create_initial_population(tsp, population_size):
    """
    Create an initial population of tours
    """
    population = []
    for _ in range(population_size):
        tour = generate_random_tour(tsp)
        population.append(tour)
    return population

def select_parents(population, num_parents):
    """
    Select the parents for reproduction
    """
    parents = random.sample(population, num_parents)
    parents.sort(key=lambda x: evaluate_tour(x, tsp))
    return parents

def breed_population(parents, population_size):
    """
    Breed the parents to create the next generation population
    """
    population = parents.copy()
    while len(population) < population_size:
        parent1, parent2 = random.sample(parents, 2)
        child = crossover(parent1, parent2)
        population.append(child)
    return population

def mutate_population(population, mutation_rate):
    """
    Mutate the population by applying the mutation operation
    """
    for i in range(len(population)):
        if random.random() < mutation_rate:
            population[i] = mutate(population[i])
    return population

def run_genetic_algorithm(tsp, population_size, num_generations, mutation_rate):
    population = create_initial_population(tsp, population_size)
    best_tour = population[0]
    best_distance = evaluate_tour(best_tour, tsp)
    for _ in range(num_generations):
        parents = select_parents(population, population_size // 2)
        population = breed_population(parents, population_size)
        population = mutate_population(population, mutation_rate)
        for tour in population:
            tour_distance = evaluate_tour(tour, tsp)
            if tour_distance < best_distance:
                best_tour = tour
                best_distance = tour_distance
    return best_tour, best_distance

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

# Test the Genetic Algorithm on the given TSP files
tsp_files = ["berlin52.tsp", "eil101.tsp", "lin318.tsp", "pr1002.tsp", "rl5934.tsp", "d18512.tsp"]
best_known_solution = {"berlin52.tsp": 7542, "eil101.tsp": 629, "lin318.tsp": 42029, "pr1002.tsp": 259045,
                       "rl5934.tsp": 118282, "d18512.tsp": 645238}

population_size = 100
num_generations = 1000
mutation_rate = 0.01

for tsp_file in tsp_files:
    print(f"\n\n***** Results for {tsp_file} *****")
    tsp = read_tsp_file(tsp_file)
    start_time = time.time()
    best_tour, best_distance = run_genetic_algorithm(tsp, population_size, num_generations, mutation_rate)
    execution_time = time.time() - start_time
    print(f"Execution Time: {execution_time} seconds")
    print(f"Best Distance: {best_distance}")
    print(f"Average Relative Length: {evaluate_relative_length(best_distance, tsp_file, best_known_solution)}")
    plot_tour(best_tour, tsp)

