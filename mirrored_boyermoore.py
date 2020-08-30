import sys

text_file = sys.argv[1]
pattern_file = sys.argv[2]

def lr_mismatch(text,pattern,curr_shift,start_skip,end_skip):
    """
        Performs left to right char comparision up to a point of mismatch with Galil's Optimization
        
        start_skip and end_skip represents the region of pattern where a comparisons would not be performed
        
        :return: [pat_index,txt_index] ]= the indexes where pattern and text mismatch
        :return: None = occurs only when the text completely matches
        
        Bryan Mayson 
        17.04.2020
        
    """
    m = len(pattern)
    n = len(text)
    for i in range(start_skip):
        if pattern[i] != text[n-m-curr_shift+i]:
            return [i,n-m-curr_shift]
        
    for i in range(end_skip+1,m):
        if pattern[i] != text[n-m-curr_shift+i]:
            return [i,n-m-curr_shift]
     
    return None
    

def create_jtable(pattern):
    """
        Create a table which stores the data of what char is present in which position for pattern
        
        :return: dim_array = represent the char present within the pattern in form of 0's and 1's
            
        Bryan Mayson 
        17.04.2020
        
    """
    dim_array = []
    for i in range(len(pattern)):
        char_array=[0]*94
        char_array[ord(pattern[i]) -ord(' ')] = 1
        dim_array.append(char_array)
    return dim_array

def lookup_jtable(jtable,index_of_mismatch,char_of_mismatch):
    """
        Searches through the generate jtable from right to left to obtain the right most occurence of a char
    
        :return: ptr =  the right most position of the mismatch char of text within the current pattern 
        :return: -1 (if there is no same char of mismatch within the pat)
        
        Bryan Mayson 
        17.04.2020
    """
    i = ord(char_of_mismatch)-ord(' ')
    ptr = len(jtable)-1
    while ptr > index_of_mismatch:
        if jtable[ptr][i] == 1:
            return ptr
        ptr-=1
    return -1


def badchar_shift(jtable,index_of_mismatch,char_of_mismatch):
    """
       Determines the shift amount by the bad char shift rule 
       
       Bryan Mayson 
       17.04.2020
    """
    rightmost =lookup_jtable(jtable,index_of_mismatch,char_of_mismatch)
    return max(1,rightmost-index_of_mismatch)

def calculate_zval(pattern,i):
    """
        Calculates the maximum legnth of a substring starting at index i which matches the prefix
        
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
        
        Bryan Mayson 
        17.04.2020
    """
    z_array = []
    for i in range(len(pattern)):
        z_array.append(calculate_zval(pattern,i))
    return z_array
        
def generate_gparray(z_val_array):
    """
        Computes the reverse of goodsuffix
        
        Bryan Mayson 
        17.04.2020
    """
    gp_array = []
    for i in range(len(z_val_array)+1):
        gp_array.append(-1)
    
    ptr = len(z_val_array)-2
    
    while ptr >= 0:
        j = (len(z_val_array)-1) - z_val_array[ptr] + 1
        gp_array[j] =ptr
        ptr-=1
    
    return gp_array

def generate_matchedprefix(z_val_array):
    """
        A reversed computation of matchedprefix
        
        Bryan Mayson 
        17.04.2020
    """
    m = len(z_val_array)
    mp_array=[0]* m
    mp_array[m-1] = z_val_array[m-1]
    for i in range(1,len(z_val_array)):
        mp_array[m-1-i] = max(z_val_array[m-1-i],mp_array[m-i])
    return mp_array

def goodsuffix_shift(index_of_mismatch,gp_array,mp_array):
    """
        Computes the shift value obtainable by the good suffix rule in reverse
        
        Bryan Mayson 
        17.04.2020
    """
    if index_of_mismatch == -1:
        return len(mp_array) - mp_array[1]
    if gp_array[index_of_mismatch-1] > -1:
        return (len(mp_array)-1) - gp_array[index_of_mismatch-1]
    else:
        return len(mp_array) - mp_array[index_of_mismatch-1]

def mirrored_boyer(text,pattern):
    """
        Applies a Mirrored Boyer Moore algorithm to the pattern and text
        
        Bryan Mayson 
        17.04.2020
    """
    
    #preprocess
    jtable = create_jtable(pattern)
    zarray = generate_zarray(pattern)
    gp_array = generate_gparray(zarray)
    mp_array = generate_matchedprefix(zarray)
    shift = 0
    
    matching_positions = []
    
    #the region of pattern we would skip pattern matching based on prev info
    start_skip = len(pattern)
    end_skip = len(pattern)-1
    
    while shift + len(pattern) <= len(text):
        
        mismatch_indexes = lr_mismatch(text,pattern,shift,start_skip,end_skip)

        #Indicates that the pattern and text match
        if mismatch_indexes == None:
            pat_mismatch = -1
            txt_mismatch = -1
            badchar_sval = 1
            
            # computes the position of where the index match in text and stores the info
            match_pos = len(text) - len(pattern) - shift + 1
            matching_positions = [str(match_pos)] + matching_positions
        else:
            pat_mismatch = mismatch_indexes[0]
            txt_mismatch = mismatch_indexes[1]
            #obtain the badchar shift value
            badchar_sval = badchar_shift(jtable,pat_mismatch,text[txt_mismatch])
            
        gs_sval = goodsuffix_shift(pat_mismatch,gp_array,mp_array)
        
        pos_shift = max(gs_sval,badchar_sval)
        
        if shift + pos_shift + len(pattern) > len(text):
            pos_shift = 1
            badchar_sval = 1
            gs_sval = 0
        
        # Galil's Optimisation
        # When pattern matches text
        if mismatch_indexes == None:

            start_skip = len(pattern) - (mp_array[1] + 1)
            end_skip = len(pattern)-1
            
        # Else when mismatch
        else:
            # Area of pattern to skip is determined based on the shift rule used
            #If badchar rule would be used
            if badchar_sval > gs_sval:
                # we would have to compare each pattern with text again as we cant ensure the same pattern occured before the mismatch
                start_skip = len(pattern)
                end_skip = len(pattern)-1
            # If good suffix rule would be used
            else:
                
                end_skip = mismatch_indexes[0] -1
                matching_length = mismatch_indexes[1] - (len(text)-len(pattern)-shift) - 1
                start_skip = end_skip - matching_length
        
        # set the shift as the max between good suffix and bad char rule
        shift += pos_shift
        

    
    return matching_positions
       
def read_strfile(file_name):
    """
        Reads the contents of a text file a returns it contents
        
        Bryan Mayson 
        17.04.2020
    """
    file = open(file_name,"r")
    str_content = file.readline().strip("\n")
    file.close
    return str_content

def write_output(output_vals):
    """
        writes the data computed by mirrored_boyer into a text file
        
        Bryan Mayson 
        17.04.2020
    """
    file = open("output_mirrored_boyermoore.txt","w+")
    for i in output_vals:
        file.writelines(i+"\n")
    file.close()

def main():
    text = read_strfile(text_file)
    pattern = read_strfile(pattern_file)
    output_vals = mirrored_boyer(text,pattern)
    write_output(output_vals)
    
if __name__ == '__main__': 
    main() 