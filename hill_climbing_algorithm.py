import random
import os
file_path = 'data.txt'
max_weight = random.randint(30,100)
    #Random graph generator
def generateProduct(size):
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

if os.path.exists(file_path):
    if os.stat(file_path).st_size == 0:
        generateProduct(20)
else:
    generateProduct(20)    

class HillClimbingAlgorith:
    def __init__(self,max_weight,items):
        self.max_weight=max_weight
        self.items=items 
        
    def heuristic(self,value,weight):
        return value/weight
    
    def uphill(self,current_weight):
        if current_weight<=self.max_weight:
            return True 
        return False 
    
    def candidate_evaluator(self):
        total_weight=0
        temp_weight=0
        initial_heuristic_value=0
        best_item=None 
        best_fit=[]
        while self.uphill(total_weight) and self.items:
            initial_heuristic_value=0
            best_item=None
            for node in self.items:
                value=node[2]
                weight=node[1]
                heuristic_value=self.heuristic(value,weight)
                if heuristic_value>initial_heuristic_value:
                    initial_heuristic_value=heuristic_value
                    best_item=node 
                    temp_weight=weight
            
            self.items.remove(best_item)
            total_weight+=temp_weight
            if not self.uphill(total_weight):break 
            best_fit.append(best_item)
        print("\nThe Optimal solution for knapsack problems according to Hill Climbing algorithm is as follows: \n")
        for item,weight,value in best_fit:
            print(item)
items=[]
with open("data.txt","r") as text_file:
    line_reader=text_file.readlines()
    for line in line_reader:
        line_list=line.strip().split(",")
        try:
            item=line_list[0]
            weight=int(line_list[1])
            value=int(line_list[2])
            items.append((line_list[0],weight,value))
        except:
            continue
instance=HillClimbingAlgorith(50,items)
instance.candidate_evaluator()
        
    



