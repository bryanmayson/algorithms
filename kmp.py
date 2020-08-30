"""
  Implementation of KMP Algorithm
"""

def calculate_zval(pattern,i):
    """
        Calculates the maximum legnth of a substring starting at index i which matches the prefix
        -- From q1 --
        
        Bryan Mayson 
        17.04.2020
    """
    counter = 0
    increments = 0
    while i + increments < len(pattern):
        if pattern[increments] != pattern[i+increments]:
            return counter
        else:
            counter+=1
        increments +=1
    return counter
 
def generate_zarray(pattern):
    """
        Generate the array containing the zvalues within each index of pattern
        -- From q1 --
        
        Bryan Mayson 
        17.04.2020
    """
    z_array = []
    for i in range(len(pattern)):
        z_array.append(calculate_zval(pattern,i))
    return z_array

def lr_mismatch(text,pattern,curr_shift):
    """
        Performs left to right char comparision up to a point of mismatch
        
        :return: i= the index where the mismatch occur
        
        Bryan Mayson 
        20.04.2020
        
    """
    for i in range(len(pattern)):
        if pattern[i] != text[i+curr_shift]:
            return i
     
    return None

def generate_spvalues(pattern,zarray):
    """
        Creates an SP Matrix which stores the same values as a normal SP but only for a specific character
        
        :return: sp_matrix = a matrix containing the sp_values
        
        Bryan Mayson 
        20.04.2020
    """
    
    sp_matrix = []
    for _ in range(len(zarray)):
        sp_matrix.append([0]*94)
    
    j=len(zarray)-1
    while j >0:
        i = j + zarray[j] -1
        x = pattern[zarray[j]]
        x_index = ord(x) - ord(" ")
        sp_matrix[i][x_index] = zarray[j]
        j-=1 
    return sp_matrix

def lookup_sp(sp_matrix,i,x):
    """
        Looks up the sp matrix for the sp value aat the given i and x values
        
        :return: the sp_value[i][x]
        
        Bryan Mayson 
        20.04.2020
    """
    x_index = ord(x)- ord(" ")
    return sp_matrix[i][x_index]
    
def kmp_algo(text,pattern):
    """
        KMP Algorithm with modifed SP(x) function
        
        :return: match_index = a list containg the indexes where the pattern match the text
        
        Bryan Mayson 
        20.04.2020
    """
    
    zarray = generate_zarray(pattern)
    sp=generate_spvalues(pattern,zarray)
    
    match_index = []
    shift = 0
    
    while len(pattern)+ shift <= len(text):
        r = lr_mismatch(text,pattern,shift)
        # When a mismatch occurs
        if r != None:
            # add one to a shift to exclude the point of mismatch
            shift += lookup_sp(sp,r-1,text[r+shift]) + 1
        #When there is a match
        else:
            match_index.append(str(shift+1))
            shift += len(pattern)-lookup_sp(sp,len(pattern)-1,pattern[len(pattern)-2])
    
    return match_index
