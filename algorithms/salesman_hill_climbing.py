import random
import matplotlib.pyplot as plt 
from math import radians,sin,cos,asin,sqrt
from hill_climbing_helper import SalesmanHillClimbing
def distance_finder(latitude_one, longitude_one, latitude_two, longitude_two):        
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
class CityClass:
    def __init__(self, index: int, distance: int):
        self.index = index
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance
def get_random_solution(matrix=[], home=0, city_indexes=[], size=0):
    cities = city_indexes.copy()
    cities.pop(home)
    population = []
    for _ in range(size):
        random.shuffle(cities)
        state = SalesmanHillClimbing(cities[:])
        state.update_distance(matrix, home)
        population.append(state)
    population.sort()
    return population[0]


def mutate_the_solution(matrix,home,state,mutation_rate = 0.01):
    mutated_state = state.deepcopy()
    for index in range(len(mutated_state.route)):
        if random.random() < mutation_rate:
            random_route = int(random.random() * len(state.route))
            city_1 = mutated_state.route[index]
            city_2 = mutated_state.route[random_route]
            mutated_state.route[index] = city_2
            mutated_state.route[random_route] = city_1
    mutated_state.update_distance(matrix, home)
    return mutated_state


def hill_climbing(matrix,home,initial_state,max_iterations,mutation_rate = 0.01):
    best_state = initial_state
    iterator = 0
    while True:
        neighbor = mutate_the_solution(matrix, home, best_state, mutation_rate)
        if neighbor.distance >= best_state.distance:
            iterator += 1
            if iterator > max_iterations:
                break
        if neighbor.distance < best_state.distance:
            best_state = neighbor
    return best_state
def main():
    city_sizes=[10,15,20]
    total_cost_list=[]
    for city_size in city_sizes:    
        cities_position={}
        cities_with_their_location={}
        with open('files/graph.txt','r') as text_file:
                connections=text_file.readlines()
                count=0
                for connection in connections:
                    connection=connection.strip().split(',')
                    latitude=float(connection[1].strip())
                    longitude=float(connection[2].strip())
                    city=connection[0].strip()
                    cities_position[city]=(latitude,longitude)
                    cities_with_their_location[city]=(latitude,longitude)
                    count+=1
                    if count==city_size:
                        break 
                    
                
        cities_coordinates={}
        index_to_cities_lookup={}
        index=0
        for key,value in cities_position.items():
            cities_coordinates[index]=value
            index_to_cities_lookup[index]=key 
            index+=1
        distance = []
        for _, target_coordinates in cities_coordinates.items():
            distances = []
            for _, coordinates in cities_coordinates.copy().items():
                distances.append(distance_finder(target_coordinates[0],target_coordinates[1], coordinates[0],coordinates[1]))
            distance.append(distances)

        home = 0
        max_iterations = 10000
        cities = list(cities_coordinates.keys())
        city_indexes = [index - 1 for index in cities]
        best_solution=[]
        state = get_random_solution(distance, home, city_indexes, 100)
        state = hill_climbing(distance, home, state, max_iterations, 0.1)
        print("-- Hill climbing solution --")
        print(index_to_cities_lookup[cities[home]], end="")
        best_solution.append(index_to_cities_lookup[cities[home]])
        for i in range(0, len(state.route)):
            city_index=cities[state.route[i]]
            best_solution.append(index_to_cities_lookup[city_index])
            print(" -> " + index_to_cities_lookup[city_index], end="")

        print(" -> " + str(cities[home]), end="")
        print("\n\nTotal distance: {0} miles".format(state.distance))
        print()
        total_cost=0
        for index in range(len(best_solution)):
            city_one=best_solution[index-1]
            city_two=best_solution[index]
            latitude_one=cities_with_their_location[city_one][0]
            longitude_one=cities_with_their_location[city_one][1]
            latitude_two=cities_with_their_location[city_two][0]
            longitude_two=cities_with_their_location[city_two][1]
            
            total_cost+=distance_finder(latitude_one,longitude_one,latitude_two,longitude_two)
        total_cost_list.append(total_cost)
    left = [total_cost_list[0], total_cost_list[1], total_cost_list[2]]
    height = [10, 15, 20]
    tick_label = ['10 cities ', '15 cities ', '20 cities']
    plt.bar(height, left,  tick_label = tick_label,
            width = 0.8, color = ['red', 'green', 'yellow'])
    plt.ylabel('optimal cost')
    plt.xlabel("Number of cities")
    plt.title("Salesman problem using hill climbing algorithm")    
    plt.show()
if __name__ == "__main__":
    main()