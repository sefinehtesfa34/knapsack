import numpy as np
from algorithms.nodes_generator import NodeGenerator
from simulated_annealing_tsp import SimulatedAnnealing

def file_reader(size):
    items=[]
    with open("graph.txt","r") as text_file:
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
weights_and_values=np.column_stack((weights,values))
def main():
    #set the simulated annealing algorithm params
    temp = 1000
    stopping_temp = 0.00000001
    alpha = 0.9995
    stopping_iter = 10000000
    #set the dimensions of the grid
    sa = SimulatedAnnealing(weights_and_values, temp, alpha, stopping_temp, stopping_iter)
    sa.anneal()

    #animate
    sa.animateSolutions()

    #show the improvement over time
    sa.plotLearning()


if __name__ == "__main__":
    main()