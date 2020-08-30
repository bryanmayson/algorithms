# Bryan Mayson 29259436
# Assignment 3 Task 2 Encoding
import sys
import math
from bitarray import bitarray

text_file= sys.argv[1]
W= sys.argv[2]
L= sys.argv[3]

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

def decimal_binary(val,binary_array): 
    """
        Converts the decimal values into an array of binary values
        
        Bryan Mayson 
        10.06.2020
    """
    if val > 1: 
        decimal_binary(val // 2,binary_array) 
    binary_array.append(str(val%2))

def char_binary_padding(binary_array):
    """
        Pads the current binary_array such that it would have a fixed length of 7
        
        Bryan Mayson 
        10.06.2020
    """
    binary_array = [0]*(7-len(binary_array)) + binary_array
    return binary_array

def elias_encoding(n,encoded_binary):
    """
        Elias Encoding
        
        Bryan Mayson 
        10.06.2020
    """
    bin_array = []
    decimal_binary(n,bin_array)
    encoded_binary = bin_array
    temp_binarray = bin_array
    
    while len(temp_binarray) > 1:
        length = len(temp_binarray)
        
        length_component = length -1
        li_array = []
        decimal_binary(length_component,li_array)
        li_array[0]= "0"
        encoded_binary = li_array+ encoded_binary
        temp_binarray = li_array
    
    return encoded_binary

class MinHeap:
    """
        MinHeap Datastructure used for Huffman Encoding
        
        Bryan Mayson 
        10.06.2020
    """
    def __init__(self):
        self.array = []
    
    def sink(self,i):
        if i == -1:
            return   
             
        left = 2*i+1
        right =2*i+2
        
        val_left = math.inf
        val_right = math.inf
        
        smallest_child = -1
        
        # obtain left child value
        if left < len(self.array):
            val_left = self.array[left][1]
         # obtain right child value
        if right < len(self.array):
            val_right = self.array[right][1]
        
        # compare the values to see which is smallest
        if val_left < val_right:
            smallest_child = left
        elif val_right > val_left:
            smallest_child = right
        else:
            # if they are equal ensure that they are not the default
            if val_right is not math.inf and val_left is not math.inf:
                # if not default then compare their height of the chars and select the least
                if len(self.array[left][0]) <= len(self.array[right][0]):
                    smallest_child = left
                else:
                    smallest_child = right
                    
        # When a child exist
        if smallest_child is not -1:
            # compare the value of the smallest child with the parent
            # if parent > child swap parent and child
            if self.array[i][1] > self.array[smallest_child][1]:
                self.array[i],self.array[smallest_child] = self.array[smallest_child],self.array[i]
                self.sink(smallest_child)
            # for cases if parent == child 
            elif self.array[i][1] == self.array[smallest_child][1]:
                # check if child char height is lesser then parent swap and sink again
                if len(self.array[smallest_child][0]) < len(self.array[i][0]):
                    self.array[i],self.array[smallest_child] = self.array[smallest_child],self.array[i]
                    self.sink(smallest_child)
                    
        self.sink(i-1)
    
    def heapify(self,array):
        self.array=array
        self.sink(len(array)//2-1)
        
    def serve(self):
        #swap root and last element
        self.array[0], self.array[len(self.array)-1]= self.array[len(self.array)-1],self.array[0]
        item = self.array[len(self.array)-1]
        # remove item from the current heap array
        self.array = self.array[:len(self.array)-1]
        # perform sink on root
        self.sink(0)
        return item
    
    def insert(self,item):
        self.array.append(item)
        i = len(self.array)-1
        self.rise(i)
    
    def rise(self,i):
        if i == 0:
            return
        parent = i//2
        if self.array[parent][1] > self.array[i][1] and len(self.array[parent][0]) <= len(self.array[i][0]):
            self.array[parent],self.array[i]= self.array[i],self.array[parent]
            self.rise(parent)
        else:
            return
        
def huffman_encoding(unique_array):
    """
        Creates a heap and generate the huffman encodings of the list of unique characters with its frequency
        
        Bryan Mayson 
        10.06.2020
    """
    heap = MinHeap()
    heap.heapify(unique_array)
    
    encodings = []
    
    # initialise array to store encodings of each char
    for _ in range(128):
        encodings.append([])     

    while len(heap.array) > 1:
        
        #obtain the least frequent values
        item_1 = heap.serve()
        item_2 = heap.serve()

        
        # preprend encoding values
        for i in range(len(item_1[0])):
            encodings[ord(item_1[0][i])] =["0"]+ encodings[ord(item_1[0][i])]    
        for i in range(len(item_2[0])):
            encodings[ord(item_2[0][i])] =["1"]+ encodings[ord(item_2[0][i])]
            
        item_3 = [item_1[0]+item_2[0],item_1[1]+item_2[1]]
        
        heap.insert(item_3)

    return encodings
    
def z_algorithm(string,w_pointer,l_pointer,l_length):
    """
        Implementation of Z algorithm with pointers
        
        Implementation plays around with pointers once the exceed a certain length in the z array
        
        :param: string: the string  used for the z_algo
        :param: w_pointer: starting index of window in the actual string
        :param: l_pointer: starting index of lookahead in the actual string
        :param: l_length: the length of the lookahead
        
        Bryan Mayson 
        10.06.2020
    """
    # Create an zarray of length = len(lookahead) + (len(window)+len(lookahead))
    zarray = [0]* ((l_pointer+l_length - w_pointer) + l_length)
    #print(len(zarray))
    r = 0
    l = 0
    
    # Pointer used to point to the character in the actuall string
    # We ignore the first letter of the prefix (lookahead) so we increment the pointer by one
    pointer = l_pointer + 1
    
    for i in range(1,len(zarray)):
        
        # Case 1: Create a new z box when the current character is not in range of any zbox
        if i > r:
            
            count = 0
            
            # Comparing current character with the character at the prefix
            # l_pointer represents the starting indedx of the lookahead (prefix)
            while pointer + count < l_pointer + l_length and string[l_pointer+count] == string[pointer+count]:
                count+=1
            
            zarray[i] = count
            
            if count > 0:
                l = i
                r = i + count -1
        
        else:
            
            prev = i-l
            remain = r-i+1
            
            # If the current character is within the prev zbox
            if zarray[prev]< remain:
                zarray[i] = zarray[prev]
            
            # If the value is exactly within the z box
            elif zarray[prev] == remain:
                
                extend = r+1
                
                while extend + w_pointer - l_length < l_pointer+l_length:
                    # Readjusting the pointers if necessary
                    if extend < l_length:
                        pointer_1 = l_pointer+extend
                    else:
                        pointer_1 = extend + w_pointer - l_length
                    
                    if extend - i <l_length:
                        pointer_2 = l_pointer + (extend-i)
                    else:
                        pointer_2 = pointer_1 - i

                    if string[pointer_1] == string[pointer_2]:
                        extend += 1
                    else:
                        break
                    
                zarray[i] = extend - i
                l = i
                r = extend - 1
                
            else:
                zarray[i] = remain
        
        # Offset the values of the pointer such that once the pointer exceeds the length of lookahead (prefix)
        # It would look at the start of the window (suffix)
        if pointer+1 >= l_pointer + l_length:
            pointer = w_pointer
        else:
            pointer+=1

            
    return zarray


def lzss(string,huffman_code):
    
    string+="$"
    
    encoded = []
    # The lookahed length and window length of the algorithm
    max_lookahead_length = int(L)
    max_window_length = int(W)
    
    seperator = 0
    w_start = 0
    
    # add the first letter of the string into the huffman code
    encoded.append("1"+"".join(huffman_code[ord(string[seperator])]))
    
    while seperator < len(string)-2:
        
        if seperator - w_start + 1 >max_window_length:
            w_start = seperator - (max_window_length-1)
        
        # Readjusting the lookahead length when nearing the end of the string
        if seperator + max_lookahead_length < len(string):
            lookahead_length = max_lookahead_length
        else:
            lookahead_length = len(string) - seperator -1 
        
        # Process the z values of the string
        z_array = z_algorithm(string,w_start,seperator+1,lookahead_length)
        #print(z_array)
        
        pointer = lookahead_length
        maxvalue = 0
        offset = None
        
        # skip the z values of the prefix and start obtaing the max value possible
        for _ in range(w_start,seperator+1):
            if z_array[pointer] > maxvalue:
                maxvalue = z_array[pointer]
                offset = pointer - lookahead_length
            pointer+=1
          
        if maxvalue >= 3:  
            # Calulating the actual distance form the index of pattern with greatest length from the seperator
            actual_index = w_start + offset
            diff = seperator-actual_index+1
            
            offset_elias = "".join(elias_encoding(diff,[]))
            length_elias = "".join(elias_encoding(maxvalue,[]))
            encoded.append("0"+offset_elias+length_elias)
            seperator+=maxvalue
        else:
            encoded.append("1"+"".join(huffman_code[ord(string[seperator+1])]))
            seperator+=1
    
    # obtain the number of encodings genererated by the lzss encoded with the elias encoding
    elias_num_of_encoded = "".join(elias_encoding(len(encoded),[]))
    
    # Store all the data and pass return it
    encoded_data = elias_num_of_encoded + "".join(encoded)
    
    return encoded_data

def main():
    string = read_strfile(text_file)
    encoded_data = "" # stores the encoded string
    char_freq = [0]*128
    
    # Encoding Header
    #-------------------------------
    # stores the frequency of each possible character in the string
    for i in range(len(string)):
        char_freq[ord(string[i])]+=1  
    
    unique = []
    # obtains the frequency of each unique char in the string
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            unique.append([chr(i),char_freq[i]])
     
    # Obtain the Elias Encoding of the number of unique characters and add to the string      
    n_unique_encoded = elias_encoding(len(unique),[])
    encoded_data+= "".join(n_unique_encoded)
    
    # returns encodings for 127 different chars
    char_encodings = huffman_encoding(unique)
    
    # Go through the encodings available
    for i in range(len(char_encodings)):
        if len(char_encodings[i])>0:
            encode_huffman = ""
            
            # Binary Represenation of current character
            binary_char=[]
            decimal_binary(i,binary_char)
            encode_huffman+="".join(binary_char)
            
            # Elias encoding of the length of the current huffman code
            encode_huffman+="".join(elias_encoding(len(char_encodings[i]),[]))
            
            # The huffman code itself
            encode_huffman+="".join(char_encodings[i])
            
            encoded_data+=encode_huffman
    
    # Encoding the data 
    #----------------------------------
    encoded_data += lzss(string,char_encodings)
    
    # Padding the data if required
    #----------------------------------
    n_bytes_fit = len(encoded_data)//8
    excess_bit = len(encoded_data)-(n_bytes_fit*8)
    
    if excess_bit > 0:
        padding_required = 8 - excess_bit
        for _ in range(padding_required):
            encoded_data += "0"

    # Coveriting data into bits and writing it into a bin file
    bits = bitarray(encoded_data)
    with open('output_encoder_lzss.bin','wb') as file:
        bits.tofile(file)

if __name__ == '__main__': 
    main() 