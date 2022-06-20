import numpy as np 
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt 
class SalesmanSimulatedAnnealing:
    def __init__(self) -> None:
        self.position_city_lookup_table={}
    def distance_finder(self,latitude_one, longitude_one, latitude_two, longitude_two):        
        latitude_one, \
        longitude_one, \
        latitude_two, \
        longitude_two \
        = map(radians, [latitude_one, longitude_one, latitude_two, longitude_two])
        longitude_difference = longitude_two - longitude_one 
        latitude_difference = latitude_two - latitude_one 
        distance = sin(latitude_difference/2)**2 \
            + cos(latitude_one) \
            * cos(latitude_two) \
            * sin(longitude_difference/2)**2
        distance= 2 * asin(sqrt(distance)) 
        distance_in_km = 6371* distance
        return distance_in_km
    def generate(self,city_size):
        cities = []
        with open('files/graph.txt','r') as text_file:
            connections=text_file.readlines()
            count=0
            for connection in connections:
                connection=connection.strip().split(',')
                latitude=connection[1].strip()
                longitude=connection[2].strip()
                self.position_city_lookup_table[(float(latitude),float(longitude))]=connection[0].strip()
                cities.append((float(latitude),float(longitude)))
                count+=1
                if count==city_size:
                    return cities
        return cities
    def initialize(self,count):
        solution = np.arange(count)
        return solution
    def evaluate(self,cities, solution):
        distance = 0
        for index in range(len(cities)):
            latitude_longitude_pair_for_city_one = cities[solution[index]]
            latitude_longitude_pair_for_city_two = cities[solution[index - 1]]
            latitude_one, \
            longitude_one,\
            latitude_two, \
            longitude_two \
            = map(radians, [latitude_longitude_pair_for_city_one[0], \
                            latitude_longitude_pair_for_city_one[1], \
                            latitude_longitude_pair_for_city_two[0], \
                            latitude_longitude_pair_for_city_one[1]])
            
            longitude_difference = longitude_two - longitude_one 
            latitude_difference = latitude_two - latitude_one 
            distance = sin(latitude_difference/2)**2 \
                + cos(latitude_one) \
                * cos(latitude_two) \
                * sin(longitude_difference/2)**2
            distance= 2 * asin(sqrt(distance)) 
            distance_in_km = 6371* distance
            distance+=distance_in_km
        return distance
    def modify(self,current):
        new = current.copy()
        latitude_longitude_pair_for_city_one = np.random.randint(len(current))
        latitude_longitude_pair_for_city_two = np.random.randint(len(current))
        while latitude_longitude_pair_for_city_two == latitude_longitude_pair_for_city_one:
            latitude_longitude_pair_for_city_two = np.random.randint(len(current))
        new[latitude_longitude_pair_for_city_one], new[latitude_longitude_pair_for_city_two] = new[latitude_longitude_pair_for_city_two], new[latitude_longitude_pair_for_city_one]
        return new
instance=SalesmanSimulatedAnnealing()
if __name__ == "__main__":
    best_solutions=[]
    total_cost=[]
    INITIAL_TEMPERATURE = 1000
    STOPPING_TEMPERATURE = 1
    TEMPERATURE_DECAY = 0.999
    SIZE = 0.7
    for city_size in [10,15,20]:
        CITY_COUNT = city_size
        cities = instance.generate(city_size=CITY_COUNT)    
        current_solution = instance.initialize(CITY_COUNT)
        current_score = instance.evaluate(cities, current_solution)
        best_score = worst_score = current_score
        temperature = INITIAL_TEMPERATURE
        while (temperature > STOPPING_TEMPERATURE):
            new_solution = instance.modify(current_solution)
            new_score = instance.evaluate(cities, new_solution)
            best_score = min(best_score, new_score)
            worst_score = max(worst_score, new_score)
            if new_score < current_score:
                current_solution = new_solution
                current_score = new_score
            else:
                delta = new_score - current_score
                probability = np.exp(-delta / temperature)
                if probability > np.random.uniform():
                    current_solution = new_solution
                    current_score = new_score
            temperature *= TEMPERATURE_DECAY
            infos = (temperature, current_score, best_score, worst_score)
        solution=[]        
        cost=0
        for index_i,index in enumerate(current_solution):
            solution.append((instance.position_city_lookup_table[cities[index]]))
            latitude_one=cities[index_i-1][0]
            longitude_one=cities[index_i-1][1]
            latitude_two=cities[index_i][0]
            longitude_two=cities[index_i][1]
            cost+=instance.distance_finder(latitude_one,longitude_one,latitude_two,longitude_two)
        best_solutions.append(solution)
        total_cost.append(cost)
    city_size=10
    index=0
    for solution in best_solutions:
        print(f"Best solution for {city_size } city size\n",solution)
        city_size+=5
        print(total_cost[index])
        index+=1
    left = [total_cost[0], total_cost[1], total_cost[2]]
    height = [10, 15, 20]
    tick_label = ['10 cities ', '15 cities ', '20 cities']
    plt.bar(height, left,  tick_label = tick_label,
            width = 0.8, color = ['red', 'green', 'yellow'])
    plt.ylabel('optimal cost')
    plt.xlabel("Number of cities")
    plt.title("Salesman problem using Simulated annealing algorithm")    
    plt.show()
