from copy import copy
import random
import numpy
from collections import defaultdict

from pyrsistent import s 
class Graph:
    def __init__(self):
        self.graph=defaultdict(list)
    def graphBuilder(self,connection):
        self.graph[connection[0]].append((connection[1],connection[2]))
        self.graph[connection[1]].append((connection[0],connection[2]))
        
        
instance_of_graph=Graph()

with open('graph.txt','r') as text_file:
    connections=text_file.readlines()
    for connection in connections:
        instance_of_graph.graphBuilder(connection.strip().split(' '))
        
    
graph=instance_of_graph.graph

def Generate(width, height, count):
    
    
    cities = []
    for _ in range(count):
        position_x = numpy.random.randint(width)
        position_y = numpy.random.randint(height)
        cities.append((position_x, position_y))
    return cities

def Initialize(count):
    solution = numpy.arange(count)
    numpy.random.shuffle(solution)
    return solution

def Evaluate(cities, solution):
    distance = 0
    for i in range(len(cities)):
        index_a = solution[i]
        index_b = solution[i - 1]
        delta_x = cities[index_a][0] - cities[index_b][0]
        delta_y = cities[index_a][1] - cities[index_b][1]
        distance += (delta_x ** 2 + delta_y ** 2) ** 0.5
    return distance

def Modify(current):
    new = current.copy()
    index_a = numpy.random.randint(len(current))
    index_b = numpy.random.randint(len(current))
    while index_b == index_a:
        index_b = numpy.random.randint(len(current))
    new[index_a], new[index_b] = new[index_b], new[index_a]
    return new

    
WIDTH = 640
HEIGHT = 480
CITY_COUNT = 20
INITIAL_TEMPERATURE = 1000
STOPPING_TEMPERATURE = 1
TEMPERATURE_DECAY = 0.999
SIZE = 0.7

if __name__ == "__main__":
    cities = Generate(WIDTH, HEIGHT, CITY_COUNT)
    
    current_solution = Initialize(CITY_COUNT)
    
    # current_score = Evaluate(cities, current_solution)
    
    # best_score = worst_score = current_score
    # temperature = INITIAL_TEMPERATURE
    # while (temperature > STOPPING_TEMPERATURE):
    #     new_solution = Modify(current_solution)
    #     new_score = Evaluate(cities, new_solution)
    #     best_score = min(best_score, new_score)
    #     worst_score = max(worst_score, new_score)
    #     if new_score < current_score:
    #         current_solution = new_solution
    #         current_score = new_score
    #     else:
    #         delta = new_score - current_score
    #         probability = numpy.exp(-delta / temperature)
    #         if probability > numpy.random.uniform():
    #             current_solution = new_solution
    #             current_score = new_score
    #     temperature *= TEMPERATURE_DECAY
    #     infos = (temperature, current_score, best_score, worst_score)
    # # print(best_score)