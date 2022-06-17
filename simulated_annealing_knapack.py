import random
import math
max_capacity=0 # m items, backpack capacity C
# time iteration number, balance balance number
 #best record the global optimal T temperature af annealing rate
number_of_items=10 
temperature=200.0 
annealing_rate =0.95
time =10 
balance = 100 
best_solution=[0]*number_of_items 
current_solution=[0]*number_of_items # best_solution records the global optimal solution current_solution records the current solution  
weight=[95, 4, 60, 32, 23, 72, 80, 62,65, 46] 
value=[55, 10, 47, 5, 4, 50, 8, 61,85, 87]

def copy_the_current_arry_to_another_array(arrary_one,array_two,length): #The copy_the_current_arry_to_another_arrayy function assigns the value of the b array to the a array
    for index in range(length):
        arrary_one[index]=array_two[index]
def calculate_the_value(x): #calculate the value of the backpack
    global max_capacity,sum_weights
    sum_of_values=0
    sum_weights=0
    for index in range(number_of_items):
        sum_of_values += x[index]*value[index] 
        sum_weights += x[index]*weight[index]    
    return sum_of_values
def random_solution_geberator(): #mainially generate random solutions
    while True:
        for index in range(number_of_items):
            if(random.random() <0.5): current_solution[index]=1
            else: current_solution[index]=0
        calculate_the_value(current_solution)
        if(sum_weights <max_capacity): 
            break
    global best
    best=calculate_the_value(current_solution)
    copy_the_current_arry_to_another_array(best_solution,current_solution,number_of_items)

def get(best_solution): #Randomly take out the items that already exist in the backpack
    while(1>0):
        random_neighbor= random.randint(0,number_of_items-1)
        if(best_solution[random_neighbor]==1): 
            best_solution[random_neighbor]=0
            break
def put(best_solution): #Randomly put items that do not exist in the backpack
    while True:
        random_neighbor = random.randint(0,number_of_items-1)
        if(best_solution[random_neighbor]==0): 
            best_solution[random_neighbor]=1
            break       
def compute_the_best_solut(): 
    global best,temperature,balance
    test=[0]*number_of_items
    current = 0 #Current backpack value
    for _ in range(balance):
        current = calculate_the_value(current_solution)
        copy_the_current_arry_to_another_array(test,current_solution,number_of_items)
        random_neighbor = random.randint(0,number_of_items-1) #Randomly select an item
        if(test[random_neighbor]==1): 
            put(test)
            test[random_neighbor]=0 #Take it out in the backpack and add other items
        else: #If not in the backpack, directly add or replace the items in the backpack
            if(random.random()<0.5):
                test[random_neighbor]=1 
            else: 
                get(test)
                test[random_neighbor]=1
        temp = calculate_the_value(test)
        if(sum_weights>max_capacity):
            continue # skip if illegal solution
        if(temp> best): 
            best=temp 
            copy_the_current_arry_to_another_array(best_solution,test,number_of_items) 
        if(temp> current): 
            copy_the_current_arry_to_another_array(current_solution,test,number_of_items) #accept the new solution directly 
        else:
            g = 1.0*(temp-current)/temperature
            if(random.random() <math.exp(g)): #Probability to accept inferior solutions
                copy_the_current_arry_to_another_array(current_solution,test,number_of_items)    
def main(): #mainialization function
    global max_capacity,best,temperature
    max_capacity = 269
    best=-1
    random_solution_geberator() #random_solution_geberator initial solution

main()
best_selected = False 
for i in range(time):      
    compute_the_best_solut()
    temperature = temperature*annealing_rate #decrease the temprature
    if(best==295):  
        best_selected = True 
        break #reach the optimal solution
        
if(best_selected == False): 
    print(best)
print('The selected items are :',list(map(bool,best_solution)))
val=0
weigh=0
for index,is_selected in enumerate(best_solution):
    if is_selected:
        weigh+=weight[index]
        val+=value[index]
print(weigh,val,max_capacity)