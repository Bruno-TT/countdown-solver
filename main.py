from itertools import permutations
from math import log2
# from queue import PriorityQueue
# from dataclasses import dataclass, field

numbers = (25, 100, 4, 6, 5, 3)
target = 473
solutions=[]

class NodePriorityQueue:
    def __init__(self):
        self.queue=[]
    def sort(self):
        self.queue.sort(key=lambda node:node.getHeuristic())
    def put(self,item):
        self.queue.append(item)
        self.sort()
    def get(self):
        x=self.queue[0]
        self.queue=self.queue[1:]
        return x
    def empty(self):
        return self.queue==[]



class Node:
    def __init__(self, path, value, remaining):
        self.path=path
        self.value=value
        self.remaining=remaining
        self.heuristic=None
        self.discover()
    def discover(self):
        if self.value==target and self.path not in solutions:
            print("".join([str(x) for x in self.path])+f"={target}")
            solutions.append(self.path)
        # if (self.value, self.remaining) not in discovered:
            # discovered.add((self.value, self.remaining))
        frontier.put(self)
    def expand(self):
        # print("expanding")
        # if (self.value, self.remaining) not in expanded:
        if self.remaining:
            for opname, op in operations:
                for n,x in enumerate(self.remaining):
                    newval = op(self.value, x)
                    if newval != None:
                        Node(self.path+(opname,x),newval,self.remaining[:n]+self.remaining[n+1:])
            # expanded.add((self.value, self.remaining))
            
    # maybe come up with a better distance heuristic?
    def getHeuristic(self):
        if self.heuristic:
            return self.heuristic
        else:
        # return abs(self.value-target)
            alttargets=[op(target, x) for x in self.remaining for (opname, op) in operations]
            alttargets=[x for x in alttargets if x!=None and x>=0]
            self.heuristic=min([abs(self.value-alttarget) for alttarget in [target]+alttargets])
            return self.heuristic

# expanded = set()
# discovered = set()
frontier = NodePriorityQueue()
operations = (("+",lambda x,y:x+y),("*",lambda x,y:x*y),("-",lambda x,y:x-y),("/",lambda x,y:x/y if x/y==int(x/y) else None))


for n,x in enumerate(numbers):
    Node((x,), x, numbers[:n]+numbers[n+1:])
    
while not frontier.empty():
    nextnode = frontier.get()
    nextnode.expand()

print("done")