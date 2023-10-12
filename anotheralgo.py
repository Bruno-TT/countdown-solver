# from itertools import permutations
# from math import log2
from math import inf
import random
# from queue import PriorityQueue
# from dataclasses import dataclass, field

numbers = [23, 52, 104, 13, 4, 9]
target = 422
solutions=[]

class NodePriorityQueue:
    def __init__(self):
        self.queue=[]
    def sort(self):
        self.queue.sort(key=lambda node:node.getHeuristic())
    def put(self,item):
        self.queue.append(item)
    def get(self):
        self.sort()
        x=self.queue[0]
        self.queue=self.queue[1:]
        return x
    def empty(self):
        return self.queue==[]
    def getLen(self):
        return len(self.queue)



class Node:
    def __init__(self, sum, remaining):
        self.sum=sum
        self.remaining=remaining
        self.heuristic=None
        self.value=None
        self.nOps=None
        self.nNums=None
        self.sumstring=None
        self.discover()

    def getVal(self):
        if self.value==None:
            sumiter=iter(self.sum)
            val=next(sumiter)
            self.nNums=1
            self.nOps=0
            try:
                while 1:
                    opname,op=next(sumiter)
                    x=next(sumiter)
                    val=op(val,x)
                    if val==None:
                        return None
                    self.nNums+=1
                    self.nOps+=1
            except StopIteration:pass
            self.value=val
        return self.value


    def discover(self):
        global closest
        v=self.getVal()
        if v==target and self.sum not in solutions:
            print(self.getString()+f"={target}")
            closest=self.getHeuristic()
            solutions.append(self.sum)
        elif v!=None:
            frontier.put(self)
            if self.getHeuristic()<closest:
                closest=self.getHeuristic()
                print(self.getString()+f"={v}")

        discovered.add((self.sum, self.remaining))

    def getString(self):
        if self.sumstring==None:
            sumiter=iter(self.sum)
            s=str(next(sumiter))
            try:
                while 1:
                    opname,op=next(sumiter)
                    s+=opname
                    s+=str(next(sumiter))
            except StopIteration:pass
            self.sumstring=s
        return self.sumstring

    def getRemovalNeighbours(self):
        for pairIndex in range(len(self.sum)-1):
            yield (self.sum[:pairIndex]+self.sum[pairIndex+2:],self.remaining+tuple(x for x in self.sum[pairIndex:pairIndex+2] if type(x)==int))
    
    def getAdditionNeighbours(self):
        for numIndex,num in enumerate(self.remaining):
            for op in operations:
                for insertionIndex in range(len(self.sum)+1):
                    if (insertionIndex%2)==0:
                        yield (self.sum[:insertionIndex]+(num,op)+self.sum[insertionIndex:],self.remaining[:numIndex]+self.remaining[numIndex+1:])
                    else:
                        yield (self.sum[:insertionIndex]+(op,num)+self.sum[insertionIndex:],self.remaining[:numIndex]+self.remaining[numIndex+1:])
    
    def expand(self):
        for sum,remaining in self.getRemovalNeighbours():
            if (sum,remaining) not in discovered:
                Node(sum,remaining)
        for sum,remaining in self.getAdditionNeighbours():
            if (sum,remaining) not in discovered:
                Node(sum,remaining)

        # expanded.add((self.value, self.remaining))
            
    # maybe come up with a better distance heuristic?
    def getHeuristic(self):
        if self.heuristic:
            return self.heuristic
        else:
            self.heuristic=abs(self.value-target)
            # alttargets=[op(target, x) for x in self.remaining for (opname, op) in operations]
            # alttargets=[x for x in alttargets if x!=None and x>=0]
            # self.heuristic=min([abs(self.value-alttarget) for alttarget in [target]+alttargets])
        return self.heuristic

# expanded = set()
closest = inf
discovered = set()
frontier = NodePriorityQueue()
operations = (("+",lambda x,y:x+y),("*",lambda x,y:x*y),("-",lambda x,y:x-y),("/",lambda x,y:x/y if x/y==int(x/y) else None))


# randomly generate start states
while frontier.getLen()<10000:
    random.shuffle(numbers)
    start_ops=[random.choice(operations) for i in numbers[1:]]
    start_seq=(numbers[0],)
    for n,x in enumerate(numbers[1:]):
        start_seq+=(start_ops[n],x)

    Node(start_seq, ())

while not frontier.empty():
    nextnode = frontier.get()
    nextnode.expand()

print("done")
