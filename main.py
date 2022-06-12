from itertools import permutations
from math import log2
# from queue import PriorityQueue
# from dataclasses import dataclass, field

numbers = (25,75,3,10,8,1)
target = 669


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
        if self.value==target:
            print("".join([str(x) for x in self.path]))
        if (self.value, self.remaining) not in discovered:
            discovered.add((self.value, self.remaining))
            frontier.put(self)
    def expand(self):
        # print("expanding")
        if (self.value, self.remaining) not in expanded:
            if self.remaining:
                for (opname, op) in operations:
                    newval = op(self.value, self.remaining[0])
                    if newval != None:
                        node = Node(self.path+(opname,self.remaining[0]),newval,self.remaining[1:])
            expanded.add((self.value, self.remaining))
            
    # maybe come up with a better distance heuristic?
    def getHeuristic(self):
        return abs(self.value-target)#+abs(log2(self.value/target))

expanded = set()
discovered = set()
frontier = NodePriorityQueue()
operations = (("+",lambda x,y:x+y),("*",lambda x,y:x*y),("-",lambda x,y:x-y),("/",lambda x,y:x/y if x/y==int(x/y) else None))


for order in permutations(numbers):
    Node((order[0],), order[0], order[1:])
    
while not frontier.empty():
    nextnode = frontier.get()
    nextnode.expand()

print("done")