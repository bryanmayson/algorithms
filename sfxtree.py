# Bryan Mayson 
# Ukkonen Suffix Tree Algorithm
#----------------------------------------------------------
# The range of charcaters the Ukonens Algorithm can accept
lowest_ascii = ord("$")
greatest_ascii = ord("~")

class Node:
    def __init__(self,start=None,end = None):
        self.link = None
        self.start = start
        self.end = end
        self.branch = [None]*(greatest_ascii-lowest_ascii + 1)

    def set_path (self,Node,char):
        self.branch[ord(char)-lowest_ascii] = Node

    def find_path(self,char):
        return self.branch[ord(char)-lowest_ascii]

class GlobalEnd:
    """
        A global endpointer
    """
    def __init__(self):
        self.val = -1

    def increment(self):
        self.val +=1

class EndValue: 
    """
         Wrapper to ensure the endpts of each edge are in the same format

         Bryan Mayson
         19.05.2020
    """
    def __init__(self,val):
        self.val = val

class ActivePoint:
    def __init__(self,node,edge=None,length=0,remainder=0):
        self.node = node
        self.edge = edge
        self.length = length
        self.remainder = remainder
        
def test_print_root(root):
    """
        prints the edges
    """
    for edges in root.branch:
        if edges is not None:
            print(edges.start,edges.end.val)

def traverse(text,i,j,active_point):
    """
        Takes the previous active point data and use them to compute the active point values at the current i and j
        
        Bryan Mayson
        21.05.2020
    """
    #Active point variables
    curr_node = active_point.node
    curr_edge = active_point.edge
    curr_length = active_point.length
    curr_remainder = active_point.remainder

    if curr_edge is None:
        curr_edge = text[j+curr_remainder]

    curr_path = curr_node.find_path(curr_edge)
    
    if curr_path is not None:
        
        edge_length = curr_path.end.val - curr_path.start + 1
        pattern_length = i-j+1 - curr_remainder
        
       # print(edge_length,pattern_length)
        # If the patternn exceeds the bound
        # Change the active points edge address
        if pattern_length > edge_length:
            curr_node = curr_path
            curr_edge = None
            curr_length = 0
            curr_remainder = edge_length
        else:
            # If withinin bound compare the character and increment them if they are the same
            if text[curr_path.start + curr_length] == text[j+curr_remainder]:
                # if the current char matching is at the end of the edge update the current activepoint to connect to the end
                if curr_path.start + curr_length == curr_path.end.val:
                    curr_length=0
                    curr_edge = None
                    curr_remainder+=1
                    curr_node = curr_path
                else:
                    curr_length+=1
                    curr_remainder+=1
    else:
        curr_edge = None
        
    new_active_point= ActivePoint(curr_node,curr_edge,curr_length,curr_remainder)
    
    return new_active_point

def split (text,j,i,active_point,end):
    
    """
        Split the targeted edge  of an active node based on the active length
        
        Bryan Mayson
        21.05.2020
    """
    # Branching
    #-----------------------------  
    target_edge = active_point.node.find_path(active_point.edge)
    # Update the edge where the branch is located
    target_edge.end = EndValue(target_edge.start + active_point.length -1)
    # Add in the remainin into the current branch
    target_edge.set_path(Node(target_edge.start + active_point.length,end),text[target_edge.start + active_point.length])
    # Insert new path for text[i]
    target_edge.set_path(Node(i,end),text[i])
        
    #print("branch")
        
    return target_edge


def ukkonen (text):
    """
        Ukkonen Implementation
        
        Bryan Mayson
        21.05.2020
    """
    root = Node()
    end = GlobalEnd()
    

    text+="$"
    
    i=0
    j=0
    
    # Store active  point variables
    active_point = ActivePoint(root)
    
    while i < len(text):
        
        previous_internal = None  #stores the previous internal node made after branching (used for suffix link)
        
        while j < i:
            
            # Obtain the active point values at current j,i
            active_point = traverse(text,i,j,active_point)
            #print(j,i,active_point.edge,active_point.length,active_point.remainder)
            
            # Skipcount condtions
            if active_point.edge is None:
                if active_point.node.find_path(text[i]) is not None:
                    break
            else:
                if (text[active_point.node.find_path(active_point.edge).start + active_point.length] == text[i]):
                    break
                
            # Branching conditions
            if active_point.length > 0:
                
                new_internal = split(text,j,i,active_point,end)
                #print("branch")
                if previous_internal is not None:
                    previous_internal.link =  new_internal
                previous_internal = new_internal
                
                # Using suffix links to branch the others with similar values
                if active_point.node.link is not None:
                    while active_point.node.link is not None:
                        active_point.node = active_point.node.link
                        active_point.remainder -=1
                        new_internal = split(text,i,j,active_point,end)
                        
                        if previous_internal is not None:
                            previous_internal.link =  new_internal
                        previous_internal = new_internal
                        j+=1
                    active_point.remainder-=1
                else:
                    if active_point.node is root:
                        active_point = ActivePoint(root)
                    else:
                        active_point.remainder-=1
                
            # Extending
            if active_point.length == 0:
                if active_point.node.find_path(text[i]) is None:
                    active_point.node.set_path(Node(i,end),text[i])
                #print("extend")
            
            
                
            j+=1
    
        #If character is unique add to root
        if root.find_path(text[i]) is None:
            root.set_path(Node(i,end),text[i])
            j+=1
        
        # Reset the activepoint values before goin to a next pahse
        if i ==j:
            active_point = ActivePoint(root)
        end.increment()
        
        i+=1
        
    return root

#----------------------------------------------------------
    
#root = ukkonen("abcabxabcy")
#test_print_root(root)
