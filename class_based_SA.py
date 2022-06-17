import random
import math
import os
def generateProduct(size,max_weight):
    with open('data.txt', 'a') as f:
        f.write(str(max_weight) + "\n")
        f.write("name, " + "weight, " + "value" + "\n")

    for i in range(size):
        weight = random.randint(1,25)
        value = random.randint(5,30)
        element1 = random.randint(65,90)
        element2 = random.randint(97,122)
        element3 = random.randint(97,122)
        element4 = random.randint(97,122)
        element5 = random.randint(97,122)
        element6 = random.randint(97,122)
        arr = [chr(element1), chr(element2), chr(element3), chr(element4), chr(element5), chr(element6)]
        name = "".join(arr)
        with open('data.txt', 'a') as f:
            f.write(name + "," + str(weight) + "," + str(value) + "\n" )

file_path="data.txt"
if os.path.exists(file_path):
    if os.stat(file_path).st_size == 0:
        generateProduct(20)
else:
    generateProduct(20)
    


class SimulatedAnnealingKnapsackProblem:
    def __init__(self,max_weight,number_of_items,weights,values) -> None:
        self.weights=weights 
        self.values=values
        self.max_capacity=max_weight
        self.number_of_items=number_of_items 
        self.temperature=200.0 
        self.annealing_rate =0.95
        self.time =10 
        self.balance = 100 
        self.best_solution=[0]*self.number_of_items 
        self.current_solution=[0]*self.number_of_items # best_solution records the global optimal solution current_solution records the current solution  
        
    def copy_the_current_arry_to_another_array(self,arrary_one,array_two,length): #The copy_the_current_arry_to_another_arrayy function assigns the value of the b array to the a array
        for index in range(length):
            arrary_one[index]=array_two[index]
    def calculate_the_value(self,best_solution): #calculate the value of the backpack
        self.sum_of_values=0
        self.sum_weights=0
        for index in range(self.number_of_items):
            
            self.sum_of_values += best_solution[index]*self.values[index] 
            self.sum_weights += best_solution[index]*self.weights[index]    
        return self.sum_of_values
    def random_solution_geberator(self): #mainially generate random solutions
        while True:
            for index in range(self.number_of_items):
                if(random.random() <0.5): self.current_solution[index]=1
                else: self.current_solution[index]=0
            self.calculate_the_value(self.current_solution)
            if(self.sum_weights <self.max_capacity): 
                break
        
        self.best=self.calculate_the_value(self.current_solution)
        self.copy_the_current_arry_to_another_array(self.best_solution,self.current_solution,self.number_of_items)

    def randomly_remove_item_from_knapsack(self,best_solution): #Randomly take out the items that already exist in the backpack
        while True:
            random_neighbor= random.randint(0,self.number_of_items-1)
            if(best_solution[random_neighbor]==1): 
                best_solution[random_neighbor]=0
                break
    def add_item_to_the_knapsack(self,best_solution): #Randomly put items that do not exist in the backpack
        while True:
            random_neighbor = random.randint(0,self.number_of_items-1)
            if(best_solution[random_neighbor]==0): 
                best_solution[random_neighbor]=1
                break       
    def compute_the_best_solution(self): 
        self.test=[0]*self.number_of_items
        current = 0 #Current backpack value
        for _ in range(self.balance):
            current = self.calculate_the_value(self.current_solution)
            self.copy_the_current_arry_to_another_array(self.test,self.current_solution,self.number_of_items)
            random_neighbor = random.randint(0,self.number_of_items-1) #Randomly select an item
            if(self.test[random_neighbor]==1): 
                self.add_item_to_the_knapsack(self.test)
                self.test[random_neighbor]=0 #Take it out in the backpack and add other items
            else: #If not in the backpack, directly add or replace the items in the backpack
                if(random.random()<0.5):
                    self.test[random_neighbor]=1 
                else: 
                    self.randomly_remove_item_from_knapsack(self.test)
                    self.test[random_neighbor]=1
            self.temp = self.calculate_the_value(self.test)
            if(self.sum_weights>self.max_capacity):
                continue # skip if illegal solution
            if(self.temp> self.best): 
                self.best=self.temp 
                self.copy_the_current_arry_to_another_array(self.best_solution,self.test,self.number_of_items) 
            if(self.temp> current): 
                self.copy_the_current_arry_to_another_array(self.current_solution,self.test,self.number_of_items) #accept the new solution directly 
            else:
                probability = 1.0*(self.temp-current)/self.temperature
                if(random.random() < math.exp(probability)): #Probability to accept inferior solutions
                    self.copy_the_current_arry_to_another_array(self.current_solution,self.test,self.number_of_items)    
    def main(self): #mainialization function
        self.best=-1
        self.random_solution_geberator() #random_solution_geberator initial solution
def file_reader(size):
    items=[]
    with open("data.txt","r") as text_file:
        line_reader=text_file.readlines()
        counter=0
        max_weight=int(line_reader[0])
        
        for line in line_reader:
            line_list=line.strip().split(",")
            try:
                item=line_list[0]
                weight=int(line_list[1])
                value=int(line_list[2])
                items.append((line_list[0],weight,value))
                if counter==size:
                    return max_weight,items
                counter+=1
            except:
                continue
            
    return max_weight,items
max_weight=50
size=int(input("Enter the items size below or equal to 20: \n"))
max_weight,items=file_reader(size)
weights=[weight for item,weight,value in items]
values=[value for item,weight,value in items] 
best_selected = False
instance=SimulatedAnnealingKnapsackProblem(max_weight,number_of_items=size, weights=weights,values=values)
instance.main() 
for _ in range(instance.time):      
    instance.compute_the_best_solution()
    temperature = instance.temperature*instance.annealing_rate #decrease the temprature
    if(instance.best==295):  
        best_selected = True 
        break #reach the optimal solution
        
print('The selected items are :',list(map(bool,instance.best_solution)))
total_value=0
total_weight=0
for index,is_selected in enumerate(instance.best_solution):
    if is_selected:
        total_weight+=weights[index]
        total_value+=values[index]
print(total_weight,total_value,instance.max_capacity)

 
