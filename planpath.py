import argparse as ap
import re
import platform
import time

######## RUNNING THE CODE ####################################################
#   You can run this code from terminal by executing the following command
#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag> <algorithm>
#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0 A
#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA
###############################################################################


################## YOUR CODE GOES HERE ########################################
class GraphData:
    """
        This class stores the map obtained from the input file as well as the
        starting and goal positions within the map.
        
        Bryan Mayson
        20.8.2019
    """
    def __init__(self,size):
        # the map of the problem
        self.table = [[] for i in range(size)]
        # the start position of the problem
        self.start = None
        # the goal state of the problem
        self.goal = None
    
    def setStart(self,start):
        """
            Function which sets the starting point of the problem
        """
        self.start = start
    
    def setGoal(self,goal):
        """
            Function which sets the goals point of the problem
        """
        self.goal = goal

class Node:
    # varibale which stores the number of nodes currently generated
    num = 0
    def __init__(self,prev_ord,action,position,prev_cost,g,h,depth):
        # ID of Node
        self.identifier = "N%d" % Node.num
        # Movement used from previous node to reach current node
        self.operator = action
        # All the path taken to reach the current node
        if action != None:
            self.path = prev_ord + "-" + action
        else:
            self.path = 'S'
        #The current posiiton of the node in the map
        self.position = position
        # A pointer to the parent node
        self.parent = None
        # The children of the current node
        self.child = []
        # The current depth of the node
        self.depth = depth
        #the order of expansion of the node
        self.expand_ord = 0
        #The cost of travelling to the current node
        self.cost = g
        # The total cost of reaching the current node
        self.total_cost = prev_cost + g
        # The heuristic estimate of the node to the goal
        self.heuristic = h
        # The f value of the node
        self.fvalue = self.total_cost + self.heuristic
        Node.num+=1
    
    def addChild(self,child):
        """
            A method of a Node class to be able to add a child into its children
            if and only if the child is not a parent.
        """
        # only allows child to be added if it is not a parent node
        if (self.hasParent(child) != True):
            child.parent = self
            self.child.append(child)
    
    def hasParent(self,current_node):
        """
             Recursive function to check whehter the child node in the parameter 
             exist as a parent in the current node
             
             Look through all the parent nodes until the root
             
             @param: current_node = the child node being checked if its a parent
             @return True when the node is a parent; False when the node is not a parent
        """
        if (self.parent == None):
            return False
        # return true if the current node in pointer is the instances parent
        if (self.parent.position == current_node.position):
            return True
        # target current_node.parent
        return self.parent.hasParent(current_node)
    
    def setExpansionOrd(self,value):
        """
            Sets the order of expansion of the node
            
            @param: value is the current order of expansion of the node
        """
        # variable to indicate the order of expansion of the node
        self.expand_ord = value
        
    def asStringChild(self):
        """
            returns the Nodes identifier and path taken as a string
        """
        return self.identifier+":"+self.path
    
    def asStringOpen(self):
        """
            returns the Nodes identifier,pathtaken, cost,heauristic and f value
        """
        return self.asStringChild() +"  " +str(self.cost) +" "+ str(self.heuristic) + " " + str(self.fvalue)
    
    def __str__(self):
        """
            returns the Nodes identifier,pathtaken,expansion order,cost,heauristic and f value
        """
        return self.asStringChild() + "  " + str(self.expand_ord)+" "+str(self.cost) +" "+ str(self.heuristic) + " " + str(self.fvalue)
        
def isMountain(value):
    """
        Function used to check whether or not the current position in a map is a mountain
        
        @param: value the value of the char in the current location of the map
    """
    return value == 'X'

def expand(current_node,data,h_include):
    """
         This functions adds all the possbile nodes the current node can travel to,
         to the child of the current_node based on the transition requirements.
         
         It does this by checking possible vertical and horizontal moves followed by the diagonal moves.
         
         As the diagonal moves are added in the end of the child as well as OPEN being sorted in descending order,
         extracting the last value of the OPEN where OPEN is sorted and contained equal values of f would always extract
         a diagonal path which has a lesser cost compared to the horizontal and vertical paths.
         
         @param: current_node represents the current node being expanded
         @param: data is the data structure containing the map of the problem as well as its start and goal
         @param: h_include is the flag which represent weather or not a heuristic value is required (also indicates if the search algorithm is using the A* algorithm)
         
    """
    
    # flags for diagonal transitions
    top_diag = False
    bottom_diag = False
    left_diag = False
    right_diag = False
    
    table = data.table
    size = len(table)

    
    curr_row = current_node.position[0]
    curr_col = current_node.position[1]
    
    # Checking right directional
    if (curr_col+1 >=0 and curr_col+1 < size):
        move_right = table[curr_row][curr_col+1]
        
        if not (isMountain(move_right)):
            #flag that allows for right diagonal movement
            curr_pos = [curr_row,curr_col+1]
            right_diag = True
            if h_include:
                h = heuristicFunction(curr_pos,data.goal)
            else:
                h = 0
            child_node = Node(current_node.path,'R',curr_pos,current_node.total_cost,2,h,current_node.depth+1)
            current_node.addChild(child_node)
                
    # Checking left directional
    if (curr_col-1 >=0 and curr_col -1 < size):
        move_left = table[curr_row][curr_col-1]
        
        if not (isMountain(move_left)):
            # flag that allows for left diagonal movement
            curr_pos = [curr_row,curr_col-1]
            left_diag = True
            if h_include:
                h = heuristicFunction(curr_pos,data.goal)
            else:
                h = 0
            child_node = Node(current_node.path,'L',curr_pos,current_node.total_cost,2,h,current_node.depth+1)
            current_node.addChild(child_node)
                
    # Checking bottom directional            
    if (curr_row+1 >=0 and curr_row+1 < size):
        move_down = table[curr_row+1][curr_col]
        
        if not (isMountain(move_down)):
            # flag that allows for top diagonal movement
            curr_pos =[curr_row+1,curr_col]
            bottom_diag = True
            if h_include:
                h = heuristicFunction(curr_pos,data.goal)
            else:
                h = 0
            child_node = Node(current_node.path,'D',curr_pos,current_node.total_cost,2,h,current_node.depth+1)
            current_node.addChild(child_node)
       
    # Checking top directional
    if (curr_row-1 >=0 and curr_row -1 < size):
        move_up = table[curr_row-1][curr_col]
        
        if not (isMountain(move_up)):
            # flag that allows for bottom diagonal movement
            curr_pos=[curr_row-1,curr_col]
            top_diag = True
            if h_include:
                h = heuristicFunction(curr_pos,data.goal)
            else:
                h = 0
            child_node = Node(current_node.path,'U',curr_pos,current_node.total_cost,2,h,current_node.depth+1)
            current_node.addChild(child_node)
    
    #Top right movement
    if (top_diag and right_diag):
        if (curr_row-1 >=0 and curr_row -1 < size) and (curr_row+1 >=0 and curr_row +1 < size):
            move = table[curr_row-1][curr_col+1]
            if not (isMountain(move)):
                curr_pos=[curr_row-1,curr_col+1]
                if h_include:
                    h = heuristicFunction(curr_pos,data.goal)
                else:
                    h = 0
                child_node = Node(current_node.path,'RU',curr_pos,current_node.total_cost,1,h,current_node.depth+1)
                current_node.addChild(child_node)
    
    #Top left movement
    if (top_diag and left_diag):
        if (curr_row-1 >=0 and curr_row -1 < size) and (curr_row-1 >=0 and curr_row-1 < size):
            move = table[curr_row-1][curr_col-1]
            if not (isMountain(move)):
                curr_pos=[curr_row-1,curr_col-1]
                if h_include:
                    h = heuristicFunction(curr_pos,data.goal)
                else:
                    h = 0
                child_node = Node(current_node.path,'LU',curr_pos,current_node.total_cost,1,h,current_node.depth+1)
                current_node.addChild(child_node)
                
    # Bottom right movement            
    if (bottom_diag and right_diag):
        if (curr_row+1 >=0 and curr_row +1 < size) and (curr_row+1 >=0 and curr_row +1 < size):
            move = table[curr_row+1][curr_col+1]
            if not (isMountain(move)):
                curr_pos=[curr_row+1,curr_col+1]
                if h_include:
                    h = heuristicFunction(curr_pos,data.goal)
                else:
                    h = 0
                child_node = Node(current_node.path,'RD',curr_pos,current_node.total_cost,1,h,current_node.depth+1)
                current_node.addChild(child_node)
                
    # Bottom left movement            
    if (bottom_diag and left_diag):
        if (curr_row+1 >=0 and curr_row +1 < size) and (curr_row-1 >=0 and curr_row -1 < size):
            move = table[curr_row+1][curr_col-1]
            if not (isMountain(move)):
                curr_pos = [curr_row+1,curr_col-1]
                if h_include:
                    h = heuristicFunction(curr_pos,data.goal)
                else:
                    h = 0
                child_node = Node(current_node.path,'LD',curr_pos,current_node.total_cost,1,h,current_node.depth+1)
                current_node.addChild(child_node)

def graphSearch_aux(data,depth_limit,flag,h_include):
    """
        Graphsearch function based on the graphsearch algorithm
        
        @param: data is the data structure which contains the map of the problem as well as its starting and goal position
        @param: depth_limit represents how deep the DLS function may expand to
        @param: flag represents the number of expansions wished to be printed 
        @param: h_include represents whether or not the algorithm is for DLS or A*
    """
    
    root = Node(None,None,data.start,0,0,0,0)
    # Arranges node in decreasing order of mertit (f value)
    OPEN = []
    CLOSED = []
    # Variable to keep track of the number of nodes exapanded
    num_of_exp = 0
    
    OPEN.append(root)
    
    while True:
        # when OPEN is empty there is no result
        if (len(OPEN) == 0):
            return "NO_PATH"
        # extracting the node to expande from OPEN
        n = OPEN.pop(len(OPEN)-1)
        # while the value is still within the limit
        CLOSED.append(n)
        if (h_include or n.depth <= depth_limit):
            if (n.position == data.goal):
                return n.path +"-G " + str(n.total_cost)
            
            # expansion of a node
            expand(n,data,h_include)
            num_of_exp +=1
            # set the order of expansion of the node
            n.setExpansionOrd(num_of_exp)
            OPEN = OPEN + n.child
            
            if (flag >= 1):
                printDiagnostic(n,OPEN,CLOSED)
                flag-=1
                
            # removes it from discovered if there is no more path
            if (len(n.child)==0):
                CLOSED.pop()
                
            if (h_include):
                insertion_sort(OPEN)

def heuristicFunction(start,goal):
    """
        Formula to estimate the travel distnace between current positon and goal
        position
        
        @param: start represents the current position of the node
        @param: goal represnets the targeted position to travel to
    """
    return abs(start[0]-goal[0]) + abs(start[1]- goal[1])

def printDiagnostic(node,OPEN,CLOSED):
    """
        Function used to print the details of the current expanison of the node
        
        @param: node represent the current node which was expanded
        @param: OPEN represents the list of OPEN/undiscovered
        @param: CLOSED represents the list of CLOSED/discovered
    """
    print (node)
    children = []
    open_nodes = []
    closed_nodes = []
    
    for child in node.child:
        children.append(child.asStringChild())
    print("Children:" + str(children))
    
    for node in OPEN:
        open_nodes.append(node.asStringOpen())
    print("OPEN:" + str(open_nodes))
    
    for node in CLOSED:
        closed_nodes.append(str(node))
    print("CLOSED:" + str(closed_nodes))
    
    print()
    
    
def insertion_sort(OPEN):
    """
        Basic insertion sort used to sort OPEN in the order of decreasing f value
        
        @param: OPEN the list to be sorted depending on its f value
    """
    for i in range(1,len(OPEN)):
        while i>0 and OPEN[i-1].fvalue < OPEN[i].fvalue:
            OPEN[i-1],OPEN[i] = OPEN[i],OPEN[i-1]
            i-=1
            
def graphsearch(map, flag, procedure_name):
    solution = ""
    #measure start time of algo
    start_time = time.time()
    if procedure_name == "D":
        bound = 20
        solution = graphSearch_aux(map,bound,flag,False)
    elif procedure_name == "A":
        solution = graphSearch_aux(map,None,flag,True)
    else:
        print("invalid procedure name")
        return ""
    # measure end time of algo
    end_time = time.time()
    #prints the time taken for the algo to be processed
    print(end_time-start_time)
    return solution

def read_from_file(file_name):
    # You can change the file reading function to suit the way
    # you want to parse the file
    """
        Reads throught the content of the input file and creates a matrix of the
        specified size to store its contents. Also keeps track of the position
        of start and goal.
        
        Map, Start and Goal is stored within the GraphData
        data structure
    """
    file_handle = open(file_name)
    size = int(file_handle.readline())
    map = GraphData(size)
    for i in range (size):
        text = file_handle.readline()
        for j in range(size):
            if text[j] == 'S':
                start = [i,j]
            if text[j] == 'G':
                goal = [i,j]
            map.table[i].append(text[j])
    map.setStart(start)
    map.setGoal(goal)
    return map


###############################################################################
########### DO NOT CHANGE ANYTHING BELOW ######################################
###############################################################################

def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')
    file_handle.write(solution)

def main():
    # create a parser object
    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline
    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)
    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)
    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)
    parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)


    # get all the arguments
    arguments = parser.parse_args()

##############################################################################
# these print statements are here to check if the arguments are correct.
#    print("The input_file_name is " + arguments.input_file_name)
#    print("The output_file_name is " + arguments.output_file_name)
#    print("The flag is " + str(arguments.flag))
#    print("The procedure_name is " + arguments.procedure_name)
##############################################################################

    # Extract the required arguments

    operating_system = platform.system()

    if operating_system == "Windows":
        input_file_name = arguments.input_file_name
        input_tokens = input_file_name.split("\\")
        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT\input#.txt")
            return -1

        output_file_name = arguments.output_file_name
        output_tokens = output_file_name.split("\\")
        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT\output#.txt")
            return -1
    else:
        input_file_name = arguments.input_file_name
        input_tokens = input_file_name.split("/")
        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT/input#.txt")
            return -1

        output_file_name = arguments.output_file_name
        output_tokens = output_file_name.split("/")
        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT/output#.txt")
            return -1

    flag = arguments.flag
    procedure_name = arguments.procedure_name


    try:
        map = read_from_file(input_file_name) # get the map
    except FileNotFoundError:
        print("input file is not present")
        return -1
    # print(map)
    solution_string = "" # contains solution
    write_flag = 0 # to control access to output file

    # take a decision based upon the procedure name
    if procedure_name == "D" or procedure_name == "A":
        solution_string = graphsearch(map, flag, procedure_name)
        write_flag = 1
    else:
        print("invalid procedure name")

    # call function write to file only in case we have a solution
    if write_flag == 1:
        write_to_file(output_file_name, solution_string)

if __name__ == "__main__":
    main()
