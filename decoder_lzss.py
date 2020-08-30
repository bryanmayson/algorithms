# Bryan Mayson 29259436
# Assigment 3 Task 2 Decoding
import sys
import math
from bitarray import bitarray

bin_file = sys.argv[1]

class Node:
    """
        Node objects are used to construct Tree for huffman decoding
        
        Bryan Mayson 
        10.06.2020
    """
    def __init__(self,char= None):
        self.char = char
        self.zero = None
        self.one = None
        
    def traverse(self,string,pointer):
        """
            Traverse through the tree unitl a leaf node and returns the [number of bits of the encoding,charcter found in the leaf]
       
            Bryan Mayson 
            10.06.2020
        """
        current_node = self
        offset = 0
        while current_node.one != None and current_node.zero != None:
            if string[pointer+offset] == "1":
                current_node = current_node.one
            else:
                current_node = current_node.zero
            offset+=1
            
        return [offset,current_node.char]

def binary_decimal(string,start,end):
    """
        Reads a bit from start up to end and computes their decimal value
        
        Bryan Mayson 
        10.06.2020
    """
    
    pointer = end
    counter = 0
    decimal_val = 0
    
    while pointer >= start:
        if string[pointer] == "1":
            decimal_val += math.pow(2,counter)
        pointer-=1
        counter+=1
        
    return int(decimal_val)

def decode_elias(string,start,decode_vals,bit_length=1,offset=0):
    """
       Recursive funciton which decodes Elias Encoding and returns the entire [offset,decimal_value] of the bits of the elias encoding
       
       Bryan Mayson 
       10.06.2020
    """

    if string[start] == "0":
        string[start]="1"
        decimal_val = binary_decimal(string,start,start+bit_length-1)
        decode_elias(string,start+bit_length,decode_vals,decimal_val+1,offset+bit_length)
        
    elif string[start] =="1":
        decimal_val = binary_decimal(string,start,start+bit_length-1)
        decode_vals.append(offset+bit_length) 
        decode_vals.append(decimal_val)
    
    return decode_vals

def write_output(output_vals):
    """
        writes the data computed by main into a text file
        
        Bryan Mayson 
        22.04.2020
    """
    file = open("output_decoder_lzss.txt","w+")
    file.writelines(output_vals+"\n")
    file.close()
    
def main():
    
    # Read the bin file and obtain the bit data
    bits = bitarray()
    with open(bin_file,'rb') as file:
        bits.fromfile(file)
    # Represent the data into a string of 0's and 1's
    encoded_string = bits.to01()
    lst_encoded = []
    
    # Convert the data into a list to allow for mutation later on in elias decoding
    for i in range(len(encoded_string)):
        lst_encoded.append(encoded_string[i])
    
    # Pointer reprensting which postion of the bit is currently being processed
    pointer = 0
    
    # Process Header Information
    #-----------------------------------------------------------------------------
    # Look at the first header information(Number of unique characters in encdoing)
    first_decode = decode_elias(lst_encoded,pointer,[])
    
    pointer+=first_decode[0]
    n_of_unique = first_decode[1]
    
    # Tree for the huffman encoding
    root = Node()
    
    # For each unique character within the encoding perform the following
    for _ in range(n_of_unique):
        
        # Read the first 7 bits which represents the character
        current_char = chr(binary_decimal(lst_encoded,pointer,pointer+6))
        # Offset the pointer after reading the first 7 bits
        pointer+=7
        
        # Read elias encoding of the length of the huffman code
        elias_decoded = decode_elias(lst_encoded,pointer,[])  
        # Offset the pointer based on the elias code length
        pointer+= elias_decoded[0]
        
        huffman_codelength = elias_decoded[1]    
        current_node = root
        
        # Go through huffman encodings and create a tree for decoding later on
        for i in range(pointer,pointer+huffman_codelength):
            
            if lst_encoded[i] == "1":
                if current_node.one is None:
                    # If there is currently no path and it should be a leaf create a leaf with the current char value
                    if i-pointer+1 == huffman_codelength :
                        current_node.one = Node(current_char)
                    # If there is no path and it is not a leaf create a node an traverse to that node
                    else:
                        current_node.one = Node()
                        current_node = current_node.one
                else:
                    current_node = current_node.one
            else:
                if current_node.zero is None:
                    # If there is currently no path and it should be a leaf create a leaf with the current char value
                    if i-pointer+1 == huffman_codelength :
                        current_node.zero = Node(current_char)
                    # If there is no path and it is not a leaf create a node an traverse to that node
                    else:
                        current_node.zero = Node()
                        current_node = current_node.zero
                else:
                    current_node = current_node.zero
        
        # Offset the pointer based on the huffman code length
        pointer+= huffman_codelength
    
    # Process Data Information
    #-----------------------------------------------------------------------------
    
    decoded_string = ""
    
    # Look at the first data information ( Number of Format-0/1 Fields)
    first_decode = decode_elias(lst_encoded,pointer,[])
    
    pointer += first_decode[0]
    n_of_formats = first_decode[1]
    
    for _ in range(n_of_formats):
        
        # Reads the format filed to determine which action to perform then increment the pointer
        code = lst_encoded[pointer]
        pointer+=1
        
        if code == "1":
            # Traverse till a leaf node
            traversal_data = root.traverse(lst_encoded,pointer)
            pointer += traversal_data[0]
            # add the character into the decoded_string
            decoded_string+= traversal_data[1]
        # else if code == 0
        else:
            text_offset = decode_elias(lst_encoded,pointer,[])
            # Increment the pointer by the number of bits found wihtin the elias code
            pointer+=text_offset[0]
            text_offset_val = text_offset[1]
            
            # Obtain the length of repetition
            length_data = decode_elias(lst_encoded,pointer,[])
            pointer+= length_data[0]
            length_val = length_data[1]
            
            # Obtain the repeating text to be added into the decoded string
            new_text = ""
            text_pointer = len(decoded_string)-text_offset_val
            while length_val > 0:
                
                # Re adjust pointer when the current text pointer exceeds the length currently within the encoded string
                if text_pointer > len(decoded_string)-1:
                    text_pointer = len(decoded_string)-text_offset_val
                    
                new_text+=decoded_string[text_pointer]
                
                text_pointer+=1
                length_val -=1
            
            # add the repetition into the decoded string
            decoded_string+= new_text
            
    write_output(decoded_string)
    
    
if __name__ == '__main__': 
    main()   
        