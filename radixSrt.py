class Node:
    def __init__(self,data=None):
        self.data = data
        # self.links is a list which represent the possible characters which comes next after that node
        self.links = 27*[None]
        
class Trie:
    def __init__(self):
        self.root = Node()
    
    def add_word(self,word):
        self.add_word_aux(self.root,word,0)
    
    def add_word_aux(self,current,word,counter):
        # when the counter is equal to the length of the word
        if counter == len(word):
            # check if there already exist an end Node
            if current.links[0] is None:
                current.links[0] = Node()
        else:
            # current char of the word based on the counter
            current_char = word[counter]
            #index value of the char
            index = ord(current_char) -  96
            # if there does not exist a for the char
            if current.links[index] is None:
                # add a new node into the trie
                current.links[index]= Node()
            # dive deeper through the trie
            self.add_word_aux(current.links[index],word,counter+1)
    
    def search_word(self,word):
        return self.search_word_aux(self.root,word,0)
    
    def search_word_aux(self,current,word,counter):
        # when the length of the counter is == length of the word
        if counter == len(word):
            # check if the final node exist
            if current.links[0] is not None:
                return True
            # else if it doesnt
            else:
                return False
        # obtain the current char of the word based on counter
        current_char = word[counter]
        # index value of the char
        index = ord(current_char) -  96
        # if the link to that current character does not exist
        if current.links[index] is None:
            return False
        return self.search_word_aux(current.links[index],word,counter+1)

def countSort(alist,index=0):
    """
        sorts alist based on one char
        
        Bryan Mayson
        9.8.2018
        
        :param: alist: can be alist or a string which would undergo countSort
        :return: temp_a: a list containing a sorted alist
        :precondition: not an int value
        :postcondition: temp_a would contain the sorted version of alist
        :worse case:
            time complexity = O(N) in which N represents the size of the list
            space complexity = O(N) in which N represents the size of the list and k representing the alphabets
    """
    count_a = [0] * 26
    temp_a = []

    for i in range(len(count_a)):
        count_a[i] = []
     
    # appending at proper index
    for i in range(len(alist)):
        position = ord(alist[i][index])-97
        if position < 0:
            position = 0
        count_a[position].append(alist[i])

    for i in range(len(count_a)):
        temp_a += count_a[i]
        
    return temp_a

def radixSort(alist):
    maximum = len(alist[0])
    while maximum > 0:
        alist = countSort(alist,maximum-1)
        maximum-=1
    return alist
