import math
import random
import matplotlib.pyplot as plt
import animated_visualizer
import numpy as np 

class SimulatedAnnealing:
    def __init__(self, coords, temp, alpha, stopping_temp, stopping_iter):
        self.coords = coords
        self.sample_size = len(coords)
        self.temp = temp
        self.alpha = alpha
        self.stopping_temp = stopping_temp
        self.stopping_iter = stopping_iter
        self.iteration = 1
        self.dist_matrix = self.vectorToDistMatrix(coords)
        self.curr_solution = self.nearestNeighbourSolution(self.dist_matrix)
        self.best_solution = self.curr_solution
        self.solution_history = [self.curr_solution]
        self.curr_weight = self.weight(self.curr_solution)
        self.initial_weight = self.curr_weight
        self.min_weight = self.curr_weight
        self.weight_list = [self.curr_weight]
        print('Intial weight: ', self.curr_weight)
    
    def vectorToDistMatrix(self,coords):
    # Create the distance matrix
        return np.sqrt((np.square(coords[:, np.newaxis] - coords).sum(axis=2)))


    def nearestNeighbourSolution(self,dist_matrix):
        #Computes the initial solution (nearest neighbour strategy)
        node = random.randrange(len(dist_matrix))
        result = [node]
        nodes_to_visit = list(range(len(dist_matrix)))
        nodes_to_visit.remove(node)
        while nodes_to_visit:
            nearest_node = min([(dist_matrix[node][index], index) for index in nodes_to_visit], key=lambda x: x[0])
            node = nearest_node[1]
            nodes_to_visit.remove(node)
            result.append(node)
        return result
    
    def weight(self, sol):
        return sum([self.dist_matrix[index_i, index_j] for index_i, index_j in zip(sol, sol[1:] + [sol[0]])])


    def acceptance_probability(self, candidate_weight):
        return math.exp(-abs(candidate_weight - self.curr_weight) / self.temp)

    def accept(self, candidate):
        candidate_weight = self.weight(candidate)
        if candidate_weight < self.curr_weight:
            self.curr_weight = candidate_weight
            self.curr_solution = candidate
            if candidate_weight < self.min_weight:
                self.min_weight = candidate_weight
                self.best_solution = candidate

        else:
            if random.random() < self.acceptance_probability(candidate_weight):
                self.curr_weight = candidate_weight
                self.curr_solution = candidate

    def anneal(self):
        while self.temp >= self.stopping_temp and self.iteration < self.stopping_iter:
            candidate = list(self.curr_solution)
            l = random.randint(2, self.sample_size - 1)
            i = random.randint(0, self.sample_size - l)

            candidate[i: (i + l)] = reversed(candidate[i: (i + l)])

            self.accept(candidate)
            self.temp *= self.alpha
            self.iteration += 1
            self.weight_list.append(self.curr_weight)
            self.solution_history.append(self.curr_solution)

        print('Minimum weight: ', self.min_weight)
        print('Improvement: ',
              round((self.initial_weight - self.min_weight) / (self.initial_weight), 4) * 100, '%')

    def animateSolutions(self):
        animated_visualizer.animateTSP(self.solution_history, self.coords)

    def plotLearning(self):
        plt.plot([i for i in range(len(self.weight_list))], self.weight_list)
        line_init = plt.axhline(y=self.initial_weight, color='r', linestyle='--')
        line_min = plt.axhline(y=self.min_weight, color='g', linestyle='--')
        plt.legend([line_init, line_min], ['Initial weight', 'Optimized weight'])
        plt.ylabel('Weight')
        plt.xlabel('Iteration')
        plt.show()
