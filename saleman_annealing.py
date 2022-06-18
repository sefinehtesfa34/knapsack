import numpy as np 
position_city_lookup_table={}
def Generate():
    cities = []
    with open('graph.txt','r') as text_file:
        connections=text_file.readlines()
        for connection in connections:
            connection=connection.strip().split(',')
            latitude=connection[1].strip()
            longitude=connection[2].strip()
            position_city_lookup_table[(float(latitude),float(longitude))]=connection[0].strip()
            cities.append((float(latitude),float(longitude)))
    return cities
def Initialize(count):
    solution = np.arange(count)
    np.random.shuffle(solution)
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
    index_a = np.random.randint(len(current))
    index_b = np.random.randint(len(current))
    while index_b == index_a:
        index_b = np.random.randint(len(current))
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
    cities = Generate()    
    current_solution = Initialize(CITY_COUNT)
    
    current_score = Evaluate(cities, current_solution)
    
    best_score = worst_score = current_score
    temperature = INITIAL_TEMPERATURE
    while (temperature > STOPPING_TEMPERATURE):
        new_solution = Modify(current_solution)
        new_score = Evaluate(cities, new_solution)
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
    print("\nCities path")
    for index in current_solution:
        print(position_city_lookup_table[cities[index]],end="=>")