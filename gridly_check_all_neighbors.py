from collections import defaultdict
class HillClimbingAlgorith:
    def __init__(self,max_weight,items):
        self.max_weight=max_weight
        self.items=items 
        self.candidate_items=defaultdict(list)
        self.filtered=0
        self.filtered_items=[]
        self.grouped_items={}
    def generate_children(self,parent):
        
        return [item for item in self.items if not self.grouped_items.get(False) and item[0]!=parent]
    
    def heuristic(self,value,weight):
        return value/weight
    
    def uphill(self,current_weight):
        if current_weight<=self.max_weight:
            return True 
        return False 
    
    def candidate_evaluator(self):
        
        for node in self.items:
            self.weight={node[0]:node[1] for node in self.items}
            self.values={node[0]:node[2] for node in self.items}
    
            value=self.values[node[0]]
            weight=self.weight[node[0]]
            neighbors=self.generate_children(node[0])
            best=node[0]
            
            while neighbors:
                selected=None
                for neighor in neighbors:
                    current_weight=self.weight[best] + neighor[1]
                    current_value=self.values[best] + neighor[2]                
                    if self.uphill(current_weight) and current_value>value:
                        value=current_value
                        selected=neighor[0]
                        weight=current_weight
                if not selected:
                    break
                best=selected
                self.values[best]=value 
                self.weight[best]= weight 
                self.candidate_items[node[0]].append(selected) 
                neighbors=self.generate_children(selected)
                self.grouped_items[(node[0],selected)]=True
                self.grouped_items[(selected,node[0])]=True 
            if self.values[best]>self.filtered:
                self.filtered=self.values[best]
                self.filtered_items=([node[0]]+self.candidate_items[node[0]]).copy()

        print(list(set(self.filtered_items)))
                 
             
items=[("A",10,30),("B",40,30),("C",40,10),("D",10,25),("E",5,18)]

instance=HillClimbingAlgorith(50,items)
instance.candidate_evaluator()




