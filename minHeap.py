"""
  minHeap implementation
"""

class minHeap:
    def __init__(self):
        self.count = 0
        self.array = []
        
    def add(self,prev,current,value):
        item = [prev,current,value]
        self.array.append(item)
        self.rise(len(self.array)-1)
    
    def rise(self,index):
        while index > 1 and self.array[index//2][2] > self.array[index][2]:
            self.array[index],self.array[index//2]=self.array[index//2],self.array[index]
            index = index//2
    
    def sink(self,index):
        while 2*index < len(self.array)-1:
            child = self.get_child(index)
            if self.array[index] <= self.array[child]:
                break
            self.array[index],self.array[child] = self.array[child],self.array[index]
            index = child
    
    def get_child(self,index):
        if 2*index == len(self.array)-1 or self.array[2*index][2] < self.array[2*index+1][2]:
            return 2*index
        else:
            return 2*index + 1
    
    def serve(self):
        self.array[0],self.array[-1] = self.array[-1],self.array[0]
        value = self.array.pop()
        self.sink(0)
        return value
    
    def is_empty(self):
        return len(self.array) == 0
